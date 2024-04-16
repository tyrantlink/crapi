from app.dependencies import DB,BASE_URL,api_key_validator,TokenData
from fastapi import APIRouter,HTTPException,Security,UploadFile,File
from app.utils.tyrantlib import encode_b66,decode_b66,base66chars
from app.utils.db.documents.ext.enums import AutoResponseType
from fastapi.responses import FileResponse,JSONResponse
from app.utils.db.documents.ext.flags import APIFlags
from app.utils.db.documents import AutoResponse
from app.docs import auto_responses_docs
from app.openapi_tags import insert_tag
from re import fullmatch,escape,match
from beanie import PydanticObjectId
from os.path import exists
from typing import Literal
from pathlib import Path


insert_tag(3,{'name':'auto responses'})
router = APIRouter(prefix='/au',tags=['auto responses'])

async def _base_get_checks(au_id:str,token:TokenData) -> AutoResponse:
	if not (
		token.has_perm(APIFlags.BOT) or
		au_id in (await DB.user(token.user_id)).data.auto_responses.found
	):
		raise HTTPException(403,'you do not have permission to access this auto response!')
	au = await DB.auto_response(au_id)
	if au is None:
		raise HTTPException(404,'auto response not found!')
	return au

def new_au_type(au:AutoResponse) -> Literal['b','u','c','m','p','s']:
	if au.type == AutoResponseType.script:
		return 's'
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

async def new_au_id(au_type:Literal['b','u','c','m','p','s']) -> str:
	docs = DB._client.auto_responses.find(
		filter={'_id':{'$regex':f'^{au_type}\d+$'}},
		projection={'_id':True})
	new_id = sorted([int(doc['_id'][1:]) async for doc in docs])[-1]+1
	return f'{au_type}{new_id}'

def file_au_path(au:AutoResponse) -> str:
	match au.id[0]:
		case 'b': return f'./data/au/base/{au.response}'
		case 'u': return f'./data/au/unique/{au.data.guild}/{au.response}'
		case 'c': return f'./data/au/custom/{au.data.guild}/{au.response}'
		case 'm': return f'./data/au/mention/{au.trigger}/{au.response}'
		case 'p': return f'./data/au/personal/{au.data.user}/{au.response}'
		case 's': return f'./data/au/scripted/{au.response}'
	return HTTPException(500,'invalid auto response category!')

@router.get('/{au_id}',
	summary = 'get the data of an auto response',
	description = 'get the data of an auto response, user must be a bot, or have found the auto response',
	responses = auto_responses_docs.responses.get__au_id)
async def get__au_id(au_id:str,token:TokenData=Security(api_key_validator)) -> AutoResponse:
	au = await _base_get_checks(au_id,token)
	return au.model_dump(mode='json')

@router.get('/{au_id}/file',
	summary = 'get the file of an auto response',
	description = 'get the file of an auto response, user must be a bot, or have found the auto response',
	response_class=FileResponse,
	responses = auto_responses_docs.responses.get__au_id__file)
async def get__au_id__file(au_id:str,token:TokenData=Security(api_key_validator)) -> FileResponse:
	au = await _base_get_checks(au_id,token)
	if au.type != AutoResponseType.file:
		raise HTTPException(400,'auto response is not a file!')
	return FileResponse(file_au_path(au))

@router.get('/file/{masked_url}',
	summary = 'get the file of an auto response by it\'s masked url',
	description = 'get the file of an auto response by it\'s masked url, used as auto response response',
	responses = auto_responses_docs.responses.get__file__masked_url)
async def get__file__masked_url(masked_url:str) -> FileResponse:
	masked_url = (masked_url
		).removesuffix('.png'
		).removesuffix('.mp4'
		).removesuffix('.gif'
		).removesuffix('.webm')
	if not fullmatch(rf'[{escape(base66chars)}]+',masked_url):
		raise HTTPException(400,'invalid masked url!')
	mask = await DB.au_mask(PydanticObjectId(hex(decode_b66(masked_url))[2:]))
	if mask is None or ((au:=await DB.auto_response(mask.au)) is None):
		raise HTTPException(404,'auto response not found!')
	if au.type == AutoResponseType.deleted:
		return FileResponse('./data/au/deleted.png')
	return FileResponse(file_au_path(au))

@router.post('/{au_id}/masked_url',
	summary = 'create a masked url for an auto response',
	description = 'create a masked url for an auto response, user must be a bot',
	responses = auto_responses_docs.responses.post__au_id__masked_url)
async def post__au_id__masked_url(au_id:str,token:TokenData=Security(api_key_validator)) -> str:
	au = await _base_get_checks(au_id,token)
	mask = DB.new.au_mask(au.id)
	await mask.insert()
	path = encode_b66(int(str(mask.id),16))
	return f'{BASE_URL}/au/file/{path}.{au.response.split(".")[-1]}'

@router.post('/',
	summary = 'create a new auto response',
	description = 'create a new auto response, user must be a bot',
	responses = auto_responses_docs.responses.post__)
async def post__(au:AutoResponse,token:TokenData=Security(api_key_validator)) -> AutoResponse:
	if not token.has_perm(APIFlags.BOT):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	if au.id != 'unset':
		raise HTTPException(400,'auto response id must be "unset"!')
	au_type = new_au_type(au)
	au.id = await new_au_id(au_type)
	await au.insert()
	return au.model_dump(mode='json')

@router.post('/{au_id}/file',
	summary = 'upload a file to an auto response',
	description = 'upload a file to an auto response, user must be a bot',
	responses = auto_responses_docs.responses.post__au_id__file)
async def post__au_id__file(
	au_id:str,
	replace:bool|None=None,
	file:UploadFile=File(...),token:TokenData=Security(api_key_validator)
) -> JSONResponse:
	if not token.has_perm(APIFlags.BOT):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	au = await _base_get_checks(au_id,token)
	if au.type == AutoResponseType.deleted:
		raise HTTPException(400,'you cannot upload a file to a deleted auto response!')

	path = '/'.join(file_au_path(au).split('/')[:-1])

	if (
			file.filename is not None and 
			not fullmatch(r'^.*\.(png|mp4|gif|webm)$',file.filename)
	):
		raise HTTPException(400,'file must be a png, mp4, gif or webm!')

	Path(path).mkdir(parents=True,exist_ok=True)
	if not replace and exists(f'{path}/{au.response}'):
		raise HTTPException(400,'file already exists!')
	with open(f'{path}/{au.response}','wb') as f:
		f.write(await file.read())
	return JSONResponse({'success':True})

@router.delete('/{au_id}',
	summary = 'delete an auto response',
	description = 'delete an auto response, user must be a bot',
	responses = auto_responses_docs.responses.delete__au_id)
async def delete__au_id(au_id:str,token:TokenData=Security(api_key_validator)) -> JSONResponse:
	if not token.has_perm(APIFlags.BOT):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	au = await _base_get_checks(au_id,token)
	au.type = AutoResponseType.deleted
	await au.save_changes()
	return JSONResponse({'success':True})

@router.patch('/{au_id}',
	summary = 'update an auto response',
	description = 'update an auto response, user must be a bot',
	responses = auto_responses_docs.responses.patch__au_id)
async def patch__au_id(
	au_id:str,
	updates:dict,
	token:TokenData=Security(api_key_validator)
) -> AutoResponse:
	if not token.has_perm(APIFlags.BOT):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	au = await _base_get_checks(au_id,token)
	au = au.with_overrides(updates)
	await au.save()
	return au.model_dump(mode='json')