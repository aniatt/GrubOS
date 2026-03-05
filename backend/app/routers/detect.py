from io import BytesIO

from fastapi import APIRouter, File, UploadFile
from PIL import Image

from app.models.schemas import DetectionResponse
from app.services.vision import vision_service

router = APIRouter()


@router.post("/detect", response_model=DetectionResponse)
async def detect_ingredients(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(BytesIO(contents)).convert("RGB")
    ingredients = vision_service.detect_ingredients(image)

    return DetectionResponse(
        ingredients=ingredients,
        image_width=image.width,
        image_height=image.height,
    )
