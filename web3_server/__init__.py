from fastapi import FastAPI, WebSocket
from loguru import logger
from web3_server.ws_client import ws_client
from web3_server.types import ContractCall
from web3_server import abi_temp, address_temp
import uuid

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, uri: str):
    await websocket.accept()
    client_id = str(uuid.uuid4())
    w3ok = await ws_client.init_w3(client_id, uri)
    if not w3ok:
        await websocket.send_text('connect fail')
        await websocket.close()
    ws_client.connect(client_id, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            await ws_client.receive(client_id, data)
    except Exception as e:
        logger.error(e)
        await websocket.close()
