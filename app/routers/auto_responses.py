from app.dependencies import DB,BASE_URL,api_key_validator,TokenData
from fastapi import APIRouter,HTTPException,Security,UploadFile,File
from app.utils.tyrantlib import encode_b66,decode_b66,base66chars
from app.utils.db.documents.ext.enums import AutoResponseType
from fastapi.responses import FileResponse,JSONResponse
from app.utils.db.documents.ext.flags import APIFlags
from app.utils.db.documents import AutoResponse
from re import fullmatch,escape,match
from typing import Literal,Annotated
from beanie import PydanticObjectId
from os.path import exists
from pathlib import Path


router = APIRouter(prefix='/au')

async def _base_get_checks(au_id:str,token:TokenData) -> AutoResponse:
	if not ((
		token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT) or
		au_id in (await DB.user(token.user_id)).data.auto_responses.found
	):
		raise HTTPException(401,'you do not have permission to access this auto response!')
	au = await DB.auto_response(au_id)
	if au is None:
		raise HTTPException(404,'auto response not found!')
	return au

@router.get('/{au_id}/file')
async def get_file(au_id:str,token:TokenData=Security(api_key_validator)):
	au = await _base_get_checks(au_id,token)
	if au.type == AutoResponseType.deleted:
		return FileResponse('./data/au/deleted.png')
	match au.id[0]:
		case 'b': return FileResponse(f'./data/au/base/{au.response}')
		case 'u': return FileResponse(f'./data/au/unique/{au.data.guild}/{au.response}')
		case 'c': return FileResponse(f'./data/au/custom/{au.data.guild}/{au.response}')
		case 'm': return FileResponse(f'./data/au/mention/{au.data.user}/{au.response}')
		case 'p': return FileResponse(f'./data/au/personal/{au.data.user}/{au.response}')
		case _: pass
	return HTTPException(500,'invalid auto response type!')

@router.get('/file/{masked_url}')
async def get_masked_file(masked_url:str):
	if not fullmatch(rf'[{escape(base66chars)}]+',masked_url):
		raise HTTPException(400,'invalid masked url!')
	mask = await DB.au_mask(PydanticObjectId(hex(decode_b66(masked_url))[2:]))
	if mask is None or ((au:=await DB.auto_response(mask.au)) is None):
		raise HTTPException(404,'auto response not found!')
	match au.id[0]:
		case 'b': return FileResponse(f'./data/au/base/{au.response}')
		case 'u': return FileResponse(f'./data/au/unique/{au.data.guild}/{au.response}')
		case 'c': return FileResponse(f'./data/au/custom/{au.data.guild}/{au.response}')
		case 'm': return FileResponse(f'./data/au/mention/{au.trigger}/{au.response}')
		case 'p': return FileResponse(f'./data/au/personal/{au.data.user}/{au.response}')
		case _: pass
	return HTTPException(500,'invalid auto response type!')

@router.post('/{au_id}/masked_url')
async def post_masked_url(au_id:str,token:TokenData=Security(api_key_validator)) -> str:
	if not ((token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT)):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	mask = DB.new.au_mask(au_id)
	await mask.insert()
	path = encode_b66(int(str(mask.id),16))
	return f'{BASE_URL}/au/file/{path}'

@router.get('/{au_id}')
async def get_au(au_id:str,token:TokenData=Security(api_key_validator)) -> AutoResponse:
	au = await _base_get_checks(au_id,token)
	return au.model_dump(mode='json')

def get_new_au_type(au:AutoResponse) -> Literal['b','u','c','m','p']:
	if ( #? custom
		au.data.custom and 
		au.data.guild is not None
	): return 'c'
	if au.data.custom: raise HTTPException(400,'custom auto responses must have a guild!')
	if ( #? unique 
		au.data.guild is not None
	): return 'u'
	if ( #? personal
		au.data.user is not None
	): return 'p'
	if ( #? mention
		match(r'^\d+$',au.trigger)
	): return 'm'
	return 'b'

async def get_new_au_id(au_type:Literal['b','u','c','m','p']) -> str:
	docs = DB._client.auto_responses.find(
		filter={'_id':{'$regex':f'^{au_type}\d+$'}},
		projection={'_id':True})
	new_id = sorted([int(doc['_id'][1:]) async for doc in docs])[-1]+1
	return f'{au_type}{new_id}'

@router.post('/')
async def post_au(au:AutoResponse,token:TokenData=Security(api_key_validator)) -> AutoResponse:
	if not ((token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT)):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	if au.id != 'unset':
		raise HTTPException(400,'auto response id must be "unset"!')
	au_type = get_new_au_type(au)
	au.id = await get_new_au_id(au_type)
	await au.insert()
	return au.model_dump(mode='json')

@router.post('/{au_id}/file') # file upload, only allow png, mp4, gif and webm
async def post_au_file(
	au_id:str,
	replace:bool|None=None,
	file:UploadFile=File(...),token:TokenData=Security(api_key_validator)
) -> JSONResponse:
	au = await _base_get_checks(au_id,token)
	if au.type == AutoResponseType.deleted:
		raise HTTPException(400,'you cannot upload a file to a deleted auto response!')
	match au.id[0]:
		case 'b':
			path = f'./data/au/base'
		case 'u':
			path = f'./data/au/unique/{au.data.guild}'
		case 'c':
			path = f'./data/au/custom/{au.data.guild}'
		case 'm':
			path = f'./data/au/mention/{au.data.user}'
		case 'p':
			path = f'./data/au/personal/{au.data.user}'
		case _: raise HTTPException(500,f'invalid auto response id! `{au_id}`')

	if (not replace and 
			file.filename is not None and 
			not fullmatch(r'^.*\.(png|mp4|gif|webm)$',file.filename)
	):
		raise HTTPException(400,'file must be a png, mp4, gif or webm!')

	Path(path).mkdir(parents=True,exist_ok=True)
	if exists(f'{path}/{au.response}'):
		raise HTTPException(400,'file already exists!')
	with open(f'{path}/{au.response}','wb') as f:
		f.write(await file.read())
	return JSONResponse({'success':True})

@router.delete('/{au_id}')
async def delete_au(au_id:str,token:TokenData=Security(api_key_validator)) -> JSONResponse:
	if not ((token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT)):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	au = await _base_get_checks(au_id,token)
	au.type = AutoResponseType.deleted
	await au.save_changes()
	return JSONResponse({'success':True})

@router.patch('/{au_id}')
async def patch_au(
	au_id:str,
	mods:Annotated[dict,"test"],
	token:TokenData=Security(api_key_validator)
) -> AutoResponse:
	if not ((token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT)):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	au = await _base_get_checks(au_id,token)
	if au.id != au_id:
		raise HTTPException(400,'auto response id must match the id in the url!')
	au = au.with_overrides(mods)
	await au.save()
	return au.model_dump(mode='json')