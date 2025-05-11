from fastapi import FastAPI, WebSocket
import websockets
import json
from app.inference import run_inference

app = FastAPI()


@app.websocket("/predict")
async def predict(websocket: WebSocket):
    await websocket.accept()
    print("Conexión WebSocket iniciada con el cliente.")

    try:
        while True:
            frame_bytes = await websocket.receive_bytes()
            labels_and_boxes = run_inference(frame_bytes)
            response = {"detections": labels_and_boxes}
            await websocket.send_text(json.dumps(response))
    except websockets.exceptions.ConnectionClosed:
        print("Conexión WebSocket cerrada.")
    except Exception as e:
        print(f"Error al procesar los frames: {e}")


