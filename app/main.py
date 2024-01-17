from app.dependencies import DB,inc_user_api_usage,ratelimit_key
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager
from .routers import auto_responses,user
from fastapi import FastAPI,Request
from asyncio import create_task
from typing import Callable

@asynccontextmanager
async def lifespan(app:FastAPI):
	await DB.connect()
	yield

limiter = Limiter(key_func=ratelimit_key,default_limits=['5/second','120/minute'])
app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded,_rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.state.ratelimit_exempt = set()

app.include_router(auto_responses)
app.include_router(user)

@app.middleware('http')
async def log_api_usage(request:Request,call_next:Callable):
	create_task(inc_user_api_usage(request))
	return await call_next(request)

# @app.get('/')
@limiter.limit('5/second')
async def root(request:Request):
	return 'crab api, for use with /reg/nal and /reg/nal derivatives.'