from fastapi import Security,HTTPException,Request,WebSocket
from fastapi.security import APIKeyHeader as DumbKeyHeader
from app.utils.tyrantlib import decode_b66,base66chars
from asyncio import sleep,create_task,get_event_loop
from concurrent.futures import ThreadPoolExecutor
from app.utils.db import MongoDatabase
from typing import NamedTuple
from re import match,escape
from bcrypt import checkpw
from hashlib import sha256
from tomllib import loads


with open('project.toml') as f:
	_project = loads(f.read())

BASE_URL = _project['base_url']
DB = MongoDatabase(_project['mongo_uri'])
TOKEN_MATCH_PATTERN = ''.join([
	f'^([{escape(base66chars)}]',r'{1,16})\.',
	f'([{escape(base66chars)}]',r'{5,8})\.',
	f'([{escape(base66chars)}]',r'{20,27})$'])

class APIKeyHeader(DumbKeyHeader):
	async def __call__(self,request:Request=None,websocket:WebSocket=None):
		return await super().__call__(request or websocket)

		# api_key = request.headers.get(self.model.name)
		# if not api_key:
		# 	if self.auto_error: raise HTTPException(status_code=401, detail="Not authenticated")
		# 	else: return None
		# return api_key

API_KEY = APIKeyHeader(name='token')

class ValidatedTokens:
	def __init__(self):
		self.__tokens = set()

	async def add(self,token:str):
		self.__tokens.add(sha256(token.encode()).hexdigest())
		create_task(self.remove(token,86400))

	async def remove(self,token:str,after:int=None):
		await sleep(after if after is not None else 0)
		self.__tokens.remove(token)

	def __contains__(self,token:str):
		return sha256(token.encode()).hexdigest() in self.__tokens

VALID_TOKENS = ValidatedTokens()

class TokenData(NamedTuple):
	user_id: int
	timestamp: int
	key: int
	permissions: int

async def acheckpw(password:str,hashed:str) -> bool:
	with ThreadPoolExecutor() as executor:
		result = await get_event_loop().run_in_executor(executor,lambda: checkpw(password.encode(),hashed.encode()))
	return result

async def api_key_validator(api_key:str = Security(API_KEY)) -> TokenData:
	regex = match(TOKEN_MATCH_PATTERN,api_key)
	if regex is None:
		raise HTTPException(400,'api key not in correct format!')
	user_id = decode_b66(regex.group(1))
	user = await DB.user(user_id)
	if user is None or user.data.api.token is None:
		raise HTTPException(400,'api key not found!')
	if not user.data.api.token in VALID_TOKENS:
		if not await acheckpw(api_key,user.data.api.token):
			raise HTTPException(400,'api key invalid!')
		await VALID_TOKENS.add(user.data.api.token)
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

	user = await DB.user(token_data.user_id)
	user.data.statistics.api_usage += 1
	await user.save_changes()