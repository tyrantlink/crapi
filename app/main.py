from app.dependencies import DB,inc_user_api_usage,api_key_validator
from app.utils.version_checker import get_semantic_version
from app.utils.db.documents.ext.flags import APIFlags
from app.gateway import manager as gateway_manager
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from app.openapi_tags import insert_tag
from app.limiter import RateLimiter
from fastapi import FastAPI,Request
from app.docs import general_docs
from asyncio import create_task
from typing import Callable
from time import time


@asynccontextmanager
async def lifespan(app:FastAPI):
	global VERSION
	await DB.connect()
	from .routers import auto_responses,user,internal
	app.include_router(auto_responses)
	app.include_router(internal)
	app.include_router(user)
	openapi_tags = insert_tag(0,{'name':'general'})
	app.openapi_tags = openapi_tags
	VERSION = await get_semantic_version()
	app.version = VERSION
	create_task(gateway_manager.heartbeat_loop())
	yield


app = FastAPI(
	title='crAPI',
	lifespan=lifespan)
limiter = RateLimiter(5,180,420)

@app.middleware('http')
async def root_middleware(request:Request,call_next:Callable):
	t = time()
	ip = request.headers.get('CF-Connecting-IP',None)
	token = request.headers.get('token',None)
	if token is not None:
		try: token_data = await api_key_validator(token)
		except: token_data = None
		if token_data is not None and token_data.has_perm(APIFlags.BOT):
			ip = 'bypass_ratelimit'
	limiter.request(ip,t)
	if ip not in {None,'bypass_ratelimit'}:
		request.scope['client'] = (request.headers['CF-Connecting-IP'],request.scope['client'][1])
	if not limiter.check(ip,t):
		return limiter.error(ip,t)
	create_task(inc_user_api_usage(request))
	return await call_next(request)

@app.get('/',
	tags = ['general'],
	summary = 'root endpoint',
	description = 'simple root endpoint,',
	responses = general_docs.get__)
async def root(request:Request):
	user_agent = request.headers.get('user-agent','')
	if 'Mozilla' in user_agent:
		return RedirectResponse('/docs',308)
	return 'crab api, for use with /reg/nal and /reg/nal derivatives.'

@app.get('/version',
	tags = ['general'],
	summary = 'get the version of the api',
	description = 'get the version of the api',
	responses = general_docs.get__version)
async def version(request:Request):
	return VERSION