from pathlib import Path

from PIL import Image
from ultralytics import YOLO

from app.models.schemas import BoundingBox, Ingredient

DEFAULT_MODEL = "yolov8s.pt"
DEFAULT_CONFIDENCE = 0.5


class VisionService:
    def __init__(self):
        self.model: YOLO | None = None
        self.model_path: str = DEFAULT_MODEL

    def load_model(self, model_path: str | None = None):
        self.model_path = model_path or DEFAULT_MODEL

        custom_weights = Path("data/weights/best.pt")
        if custom_weights.exists():
            self.model_path = str(custom_weights)

        self.model = YOLO(self.model_path)

    def detect_ingredients(
        self, image: Image.Image, confidence: float = DEFAULT_CONFIDENCE
    ) -> list[Ingredient]:
        if self.model is None:
            raise RuntimeError("Vision model not loaded — call load_model() first")

        results = self.model(image, conf=confidence, verbose=False)
        ingredients: list[Ingredient] = []

        for result in results:
            boxes = result.boxes
            if boxes is None:
                continue
            for box in boxes:
                cls_id = int(box.cls[0])
                name = result.names[cls_id]
                conf = float(box.conf[0])
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                ingredients.append(
                    Ingredient(
                        name=name,
                        confidence=round(conf, 3),
                        bbox=BoundingBox(x1=x1, y1=y1, x2=x2, y2=y2),
                    )
                )

        return ingredients


vision_service = VisionService()
