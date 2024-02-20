from app.dependencies import DB,BASE_URL,api_key_validator,TokenData
from app.utils.tyrantlib import encode_b66,decode_b66,base66chars
from app.utils.db.documents.ext.enums import AutoResponseType
from app.utils.db.documents.ext.flags import APIFlags
from fastapi import APIRouter,HTTPException,Security
from app.utils.db.documents import AutoResponse
from fastapi.responses import FileResponse
from beanie import PydanticObjectId
from re import fullmatch,escape


router = APIRouter(prefix='/au')

async def _base_get_checks(au_id:str,token:TokenData) -> AutoResponse:
	if not ((
		token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT) or
		au_id in (await DB.user(token.user_id)).data.auto_responses.found
	):
		raise HTTPException(403,'you do not have permission to access this auto response!')
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