from app.dependencies import DB,api_key_validator,TokenData
from app.utils.db.documents.ext.flags import APIFlags
from fastapi import APIRouter,HTTPException,Security
from app.utils.tyrantlib import generate_token
from app.utils.db.documents import User
from app.openapi_tags import insert_tag
from bcrypt import hashpw,gensalt
from app.docs import user_docs


insert_tag(1,{'name':'users'})
router = APIRouter(prefix='/user',tags=['users'])

@router.get('/{user_id}',
	summary = 'get user data',
	description = 'get user data, requires bot permissions or the user\'s own token',
	responses = user_docs.get__user_id)
async def get__user_id(user_id:int,token:TokenData=Security(api_key_validator)) -> User:
	if not token.has_perm(APIFlags.BOT) or user_id == token.user_id:
		raise HTTPException(403,'you do not have permission to access this user!')
	user = await DB.user(user_id)
	if user is None:
		raise HTTPException(404,'user not found!')
	return user.model_dump(mode='json')

@router.post('/{user_id}/reset_token',
	summary = 'reset a user\'s token',
	description = 'reset a user\'s token, requires bot permissions or the user\'s own token',
	responses = user_docs.post__user_id__reset_token)
async def post__user_id__reset_token(user_id:int,token:TokenData=Security(api_key_validator)) -> str:
	if not token.has_perm(APIFlags.BOT) or user_id == token.user_id:
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	user = await DB.user(user_id)
	if user is None:
		raise HTTPException(404,'user not found!')
	user_token = generate_token(user_id)
	user.data.api.token = hashpw(user_token.encode(),gensalt()).decode()
	await user.save_changes()
	return user_token