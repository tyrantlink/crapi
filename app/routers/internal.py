from fastapi import APIRouter,HTTPException,Security,WebSocket,WebSocketDisconnect
from app.utils.crapi.enums import GatewayRequestType as Req
from app.dependencies import api_key_validator,TokenData
from app.utils.db.documents.ext.flags import APIFlags
from app.utils.crapi.models import Request
from fastapi.responses import JSONResponse
from app.openapi_tags import insert_tag
from app.gateway import manager
from app.docs import internal_docs


insert_tag(4,{'name':'internal',
	'description':'endpoints only for use by bots'})
router = APIRouter(prefix='/i',tags=['internal'])

@router.websocket('/gateway')
async def websocket__gateway(ws:WebSocket,token:TokenData=Security(api_key_validator)):
	if not token.has_perm(APIFlags.BOT):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	await manager.connect(str(token.user_id),ws)
	try:
		while True:
			await manager.handle_message(str(token.user_id),await ws.receive_json())
	except (WebSocketDisconnect,RuntimeError):
		await manager.disconnect(str(token.user_id),close=False)
	except Exception as e:
		await manager.disconnect(str(token.user_id))
		raise e

@router.post('/reload_au',
	summary = 'signal all clients to reload auto response cache',
	description = 'reload auto responses, requires bot permissions',
	responses = internal_docs.post__reload_au)
async def post__reload_au(token:TokenData=Security(api_key_validator)) -> JSONResponse:
	if not token.has_perm(APIFlags.BOT):
		raise HTTPException(403,'you do not have permission to use this endpoint!')
	try: await manager.broadcast(Request(req=Req.RELOAD_AU),True)
	except TimeoutError: raise HTTPException(503,'not all clients responded!')
	return JSONResponse({'success':True})