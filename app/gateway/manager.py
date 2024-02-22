from app.utils.crapi.models import BaseGatewayMessage,Ack,Heartbeat,Request,Response
from app.utils.crapi.enums import GatewayRequestType as Req,GatewayOpCode as Op
from app.gateway.client import GatewayClient
from fastapi import WebSocket

class GatewayManager:
	def __init__(self):
		self.__clients:dict[str,GatewayClient] = dict()
	
	async def connect(self,identifier:str,ws:WebSocket):
		await ws.accept()
		self.__clients[identifier] = GatewayClient(identifier,ws)

	async def disconnect(self,identifier:str,reason:str|None=None,close:bool=True):
		client = self.__clients.pop(identifier,None)
		if client is not None and close:
			await client.disconnect(reason)

	async def send(self,identifier:str,message:BaseGatewayMessage):
		message.seq = self.__clients[identifier].seq+1
		await self.__clients[identifier].send(message.model_dump())

	async def broadcast(self,message:BaseGatewayMessage):
		for client in self.__clients.values():
			await self.send(client.identifier,message)

	async def handle_message(self,identifier:str,message:dict):
		self.__clients[identifier].seq += 1
		match message['op']:
			case Op.ACK: return self.handle_ack(identifier,Ack.model_validate(message))
			case Op.HEARTBEAT: return self.handle_heartbeat(identifier,Heartbeat.model_validate(message))
			case Op.REQUEST: return self.handle_request(identifier,Request.model_validate(message))
			case Op.RESPONSE: return self.handle_response(identifier,Response.model_validate(message))
			case _: raise ValueError(f'unknown op code `{message["op"]}`')

	async def handle_ack(self,identifier:str,message:Ack):
		await self.disconnect(identifier,'ack received by server')

	async def handle_heartbeat(self,identifier:str,message:Heartbeat):
		if message.seq != self.__clients[identifier].seq:
			await self.disconnect(identifier,'sequence mismatch')
			return
		await self.send(identifier,Ack())

	async def handle_request(self,identifier:str,message:Request):
		await self.disconnect(identifier,'request received by server')

	async def handle_response(self,identifier:str,message:Response):
		... #! implement this when it's needed

manager = GatewayManager()