from app.dependencies import DB,inc_user_api_usage
from contextlib import asynccontextmanager
from .routers import auto_responses,user
from fastapi import FastAPI,Request
from asyncio import create_task
from typing import Callable


@asynccontextmanager
async def lifespan(app:FastAPI):
	await DB.connect()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(auto_responses)
app.include_router(user)

@app.middleware('http')
async def log_api_usage(request:Request,call_next:Callable):
	create_task(inc_user_api_usage(request))
	return await call_next(request)

@app.get('/')
async def root():
	return 'crab api, for use with /reg/nal and /reg/nal derivatives.'