from fastapi import WebSocket


class GatewayClient:
	def __init__(self,identifier:str,ws:WebSocket) -> None:
		self.__ws = ws
		self.__identifier = identifier
		self.seq = 0
	
	@property
	def identifier(self) -> str:
		return self.__identifier
	
	async def send(self,data:dict) -> None:
		await self.__ws.send_json(data)
	
	async def disconnect(self,reason:str) -> None:
		await self.__ws.close(reason=reason)