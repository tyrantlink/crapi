from app.utils.crapi.models import BaseGatewayMessage,Ack,Heartbeat,Request,Response
from app.utils.crapi.enums import GatewayOpCode as Op
from app.gateway.client import GatewayClient
from fastapi import WebSocket
from asyncio import sleep,gather,create_task,wait_for,Event
from time import time

class GatewayManager:
	def __init__(self):
		self.__clients:dict[str,GatewayClient] = dict()
	
	def client(self,identifier:str) -> GatewayClient:
		return self.__clients[identifier]
	
	async def heartbeat_loop(self):
		while True:
			for client in self.__clients.values():
				if client.last_heartbeat+60 < time():
					await client.disconnect('heartbeat timeout')
			await sleep(1)
	
	def inc_seq(self,identifier:str) -> None:
		self.client(identifier).seq += 1
		if self.client(identifier).seq == 8192:
			self.client(identifier).seq = 0

	async def connect(self,identifier:str,ws:WebSocket) -> None:
		await ws.accept()
		self.__clients[identifier] = GatewayClient(identifier,ws)

	async def disconnect(self,identifier:str,reason:str|None=None,close:bool=True) -> None:
		client = self.__clients.pop(identifier,None)
		if client is not None and close:
			await client.disconnect(reason)
	
	async def wait_for_response(self,identifier:str,seq:int) -> None:
		event = self.client(identifier).pending_responses.get(seq,None)
		if event is None:
			return
		try: await wait_for(event.wait(),5)
		except TimeoutError:
			raise TimeoutError('client did not respond to request')
		del self.client(identifier).pending_responses[seq]
		await self.send(identifier,Ack())

	async def send(self,
		identifier:str,
		message:BaseGatewayMessage,
		require_response:bool=False
	) -> int:
		self.inc_seq(identifier)
		message.seq = self.client(identifier).seq
		await self.client(identifier).send(message.model_dump_json())
		if require_response:
			self.client(identifier).pending_responses[message.seq+1] = Event()
		return message.seq

	async def broadcast(self,
		message:BaseGatewayMessage,
		required_response:bool=False
	) -> list[GatewayClient]:
		messages:list[int]  = []
		clients:list[GatewayClient] = []
		sequences:list[int] = []
		for client in self.__clients.values():
			messages.append(self.send(client.identifier,message))
			if not required_response:
				clients.append(client)
				sequences.append(client.seq+2)
		await gather(*messages)
		if not required_response:
			return clients

		missing = clients.copy()
		for _ in range(5):
			await sleep(1)
			for client,sequence in zip(clients,sequences):
				if sequence in client.pending_responses:
					missing.remove(client)
			if missing: continue
			break
		else:
			raise TimeoutError('not all clients responded')
		return clients

	async def handle_message(self,identifier:str,message:dict) -> None:
		pending_resp = self.client(identifier).pending_responses.pop(message['seq'],None)
		if pending_resp is not None: pending_resp.set()
		self.client(identifier).recent_responses[message['seq']] = message
		self.inc_seq(identifier)
		match Op(message['op']):
			case Op.ACK: await self.handle_ack(identifier,Ack.model_validate(message))
			case Op.HEARTBEAT: await self.handle_heartbeat(identifier,Heartbeat.model_validate(message))
			case Op.REQUEST: await self.handle_request(identifier,Request.model_validate(message))
			case Op.RESPONSE: await self.handle_response(identifier,Response.model_validate(message))
			case _: raise ValueError(f'unknown op code `{message["op"]}`')

	async def handle_ack(self,identifier:str,message:Ack) -> None:
		await self.disconnect(identifier,'ack received by server')

	async def handle_heartbeat(self,identifier:str,message:Heartbeat) -> None:
		if message.seq != self.client(identifier).seq:
			await self.disconnect(identifier,f'sequence mismatch; expected {self.client(identifier).seq} got {message.seq}')
			return
		self.client(identifier).last_heartbeat = time()
		await self.send(identifier,Ack())

	async def handle_request(self,identifier:str,message:Request) -> None:
		if message.forward is None:
			await self.disconnect(identifier,'request received by server without forward')
			return
		seq = await self.send(message.forward,message,True)
		create_task(self.wait_for_response(identifier,seq))

	async def handle_response(self,identifier:str,message:Response):
		... #! implement this when it's needed
		#! also make the entire request/response system less complete doo doo
		#! probably have a to field in the response, which is the request seq

manager = GatewayManager()