from app.dependencies import DB,inc_user_api_usage,api_key_validator
from app.utils.version_checker import get_semantic_version
from app.utils.db.documents.ext.flags import APIFlags
from contextlib import asynccontextmanager
from .routers import auto_responses,user
from fastapi import FastAPI,Request
from app.limiter import RateLimiter
from asyncio import create_task
from typing import Callable
from time import time


@asynccontextmanager
async def lifespan(app:FastAPI):
	global VERSION
	await DB.connect()
	VERSION = await get_semantic_version()
	yield

app = FastAPI(lifespan=lifespan)
limiter = RateLimiter(5,180,420)
app.include_router(auto_responses)
app.include_router(user)

@app.middleware('http')
async def root_middleware(request:Request,call_next:Callable):
	t = time()
	ip = request.headers.get('CF-Connecting-IP',None)
	token = request.headers.get('token',None)
	if token is not None:
		try: token_data = await api_key_validator(token)
		except: token_data = None
		if token_data is not None and token_data.permissions & APIFlags.ADMIN+APIFlags.BOT:
			ip = 'bypass_ratelimit'
	limiter.request(ip,t)
	if ip not in {None,'bypass_ratelimit'}:
		request.scope['client'] = (request.headers['CF-Connecting-IP'],request.scope['client'][1])
	if not limiter.check(ip,t):
		return limiter.error(ip,t)
	create_task(inc_user_api_usage(request))
	return await call_next(request)

@app.get('/')
async def root(request:Request):
	return 'crab api, for use with /reg/nal and /reg/nal derivatives.'

@app.get('/version')
async def version(request:Request):
	return VERSION