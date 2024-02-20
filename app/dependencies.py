from fastapi.security import APIKeyHeader# as DumbKeyHeader
from app.utils.tyrantlib import decode_b66,base66chars
from app.utils.db.documents.ext.flags import APIFlags
from fastapi import Security,HTTPException,Request
from app.utils.db import MongoDatabase
from typing import NamedTuple
from secrets import token_hex
from re import match,escape
from bcrypt import checkpw
from tomllib import loads


with open('project.toml') as f:
	_project = loads(f.read())

BASE_URL = _project['base_url']
DB = MongoDatabase(_project['mongo_uri'])
TOKEN_MATCH_PATTERN = ''.join([
	f'^([{escape(base66chars)}])',r'{1,16}\.',
	f'([{escape(base66chars)}])',r'{5,8}\.',
	f'([{escape(base66chars)}])',r'{20,27}$'])

# class APIKeyHeader(DumbKeyHeader):
# 	async def __call__(self,request):
# 		api_key = request.headers.get(self.model.name)
# 		if not api_key:
# 			if self.auto_error: raise HTTPException(status_code=401, detail="Not authenticated")
# 			else: return None
# 		return api_key

API_KEY = APIKeyHeader(name='token')

class TokenData(NamedTuple):
	user_id: int
	timestamp: int
	key: int
	permissions: int

async def api_key_validator(api_key:str = Security(API_KEY)) -> TokenData:
	regex = match(TOKEN_MATCH_PATTERN,api_key)
	if regex is None:
		raise HTTPException(400,'api key not in correct format!')
	user_id=decode_b66(regex.group(1))
	user = await DB.user(user_id)
	if user is None:
		raise HTTPException(400,'api key not found!')
	if not checkpw(api_key.encode(),user.data.api.token.encode()):
		raise HTTPException(400,'api key invalid!')
	return TokenData(
		user_id=decode_b66(regex.group(1)),
		timestamp=decode_b66(regex.group(2)),
		key=decode_b66(regex.group(3)),
		permissions=user.data.api.permissions)

async def inc_user_api_usage(request:Request):
	token = request.headers.get('token',None)
	if token is None: return
	try: token_data = await api_key_validator(token)
	except HTTPException: return

	# putting this here because dumb
	if (token_data.permissions & APIFlags.ADMIN)|(token_data.permissions & APIFlags.BOT):
		request.app.state.ratelimit_exempt.add(token)

	user = await DB.user(token_data.user_id)
	user.data.statistics.api_usage += 1
	await user.save_changes()

def ratelimit_key(request:Request):

	token = request.headers.get('token',None)
	if token is None or token in request.app.state.ratelimit_exempt:
		return token_hex(32)

	return token