import cv2
import numpy as np
from ultralytics import YOLO
from typing import List

model = YOLO('weights/best_1.pt')

def run_inference(image_bytes: bytes) -> List[dict]:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    original_height, original_width = img.shape[:2]
    img_resized = cv2.resize(img, (640, 640))

    results = model.predict(source=img_resized, conf=0.5, verbose=False)

    detections = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            confidence = box.conf[0]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x1 = int(x1 * original_width / 640)
            y1 = int(y1 * original_height / 640)
            x2 = int(x2 * original_width / 640)
            y2 = int(y2 * original_height / 640)

            detections.append({
                "label": label,
                "box": [x1, y1, x2, y2],
                "confidence": round(confidence.item(), 2)
            })

    return detections
