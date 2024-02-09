from app.dependencies import DB,inc_user_api_usage,ratelimit_key
from slowapi import Limiter, _rate_limit_exceeded_handler
from app.utils.version_checker import get_semantic_version
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from .routers import auto_responses,user
from fastapi import FastAPI,Request
from asyncio import create_task
from typing import Callable

@asynccontextmanager
async def lifespan(app:FastAPI):
	global VERSION
	await DB.connect()
	VERSION = await get_semantic_version()
	yield

limiter = Limiter(key_func=ratelimit_key,default_limits=['3/second','120/minute'])
app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.state.ratelimit_exempt = set()

app.include_router(auto_responses)
app.include_router(user)

@app.middleware('http')
async def root_middleware(request:Request,call_next:Callable):
	create_task(inc_user_api_usage(request))
	if request.headers.get('CF-Connecting-IP',False):
		request.scope['client'] = (request.headers['CF-Connecting-IP'],request.scope['client'][1])
	return await call_next(request)

@app.get('/')
async def root(request:Request):
	return 'crab api, for use with /reg/nal and /reg/nal derivatives.'

@app.get('/version')
async def version(request:Request):
	return VERSION