from app.utils.crapi.models import Response
from fastapi import WebSocket
from asyncio import Event
from time import time


class GatewayClient:
	def __init__(self,identifier:str,ws:WebSocket) -> None:
		self.__ws = ws
		self.__identifier = identifier
		self.seq = 0
		self.last_heartbeat = time()
		self.pending_responses:dict[int,Event] = dict()
		self.recent_responses:dict[int,Response] = dict()
	
	@property
	def identifier(self) -> str:
		return self.__identifier
	
	async def send(self,data:str) -> None:
		await self.__ws.send_text(data)
	
	async def disconnect(self,reason:str) -> None:
		await self.__ws.close(reason=reason)