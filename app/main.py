from contextlib import asynccontextmanager
from .routers import auto_responses,user
from app.dependencies import DB
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app:FastAPI):
	await DB.connect()
	yield

app = FastAPI(lifespan=lifespan)

app.include_router(auto_responses)
app.include_router(user)

@app.get('/')
async def root():
	return 'crab api, for use with /reg/nal and /reg/nal derivatives.'