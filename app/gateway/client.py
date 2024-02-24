from fastapi import WebSocket
from time import time


class GatewayClient:
	def __init__(self,identifier:str,ws:WebSocket) -> None:
		self.__ws = ws
		self.__identifier = identifier
		self.seq = 0
		self.last_heartbeat = time()
		self.pending_responses = set()
	
	@property
	def identifier(self) -> str:
		return self.__identifier
	
	async def send(self,data:str) -> None:
		await self.__ws.send_text(data)
	
	async def disconnect(self,reason:str) -> None:
		await self.__ws.close(reason=reason)