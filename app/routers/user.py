from app.dependencies import DB,api_key_validator,TokenData
from app.utils.db.documents.ext.flags import APIFlags
from fastapi import APIRouter,HTTPException,Security
from app.utils.tyrantlib import generate_token


router = APIRouter(prefix='/user')

@router.get('/{user_id}')
async def get_user(user_id:int,token:TokenData=Security(api_key_validator)) -> dict:
	if not ((token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT)
				 or user_id == token.user_id):
		raise HTTPException(403,'you do not have permission to access this user!')
	user = await DB.user(user_id)
	if user is None:
		raise HTTPException(404,'user not found!')
	return user.model_dump(mode='json')

@router.post('/{user_id}/reset_token')
async def post_reset_token(user_id:int,token:TokenData=Security(api_key_validator)) -> str:
	if not ((token.permissions & APIFlags.ADMIN)|(token.permissions & APIFlags.BOT)
				 or user_id == token.user_id):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	user = await DB.user(user_id)
	if user is None:
		raise HTTPException(404,'user not found!')
	user.data.api.token = generate_token(user_id)
	await user.save_changes()
	return user.data.api.token