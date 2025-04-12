import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from conferences.src.repository.rest_controller import router
from conferences.src.streaming.signal_server import ConnectionManager
import uvicorn

app = FastAPI()

app.include_router(router)

manager = ConnectionManager()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Подключение пользователей к комнате
# WebSocket конечная точка для обмена сообщениями в реальном времени
@app.websocket("/ws/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str):
    await manager.connect(websocket, room_id)

    try:
        while True:
            # Получение данных от клиента
            data = await websocket.receive_bytes() # Используется метод для получения бинарных данных
            logging.info(f"Получено {len(data)} байт из комнаты {room_id}")
            await manager.broadcast(room_id, data) # Широковещательная передача данных в комнату

    except WebSocketDisconnect:
        logging.info(f"Клиент отключился от комнаты {room_id}")
        manager.disconnect(websocket, room_id)

    except Exception as e:
        logging.error(f"Ошибка WebSocket: {e}")
        manager.disconnect(websocket, room_id)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level = "info")