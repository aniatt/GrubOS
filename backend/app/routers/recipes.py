from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from app.models.schemas import RecipeRequest
from app.services.llm import llm_service

router = APIRouter()


@router.post("/recipes")
async def generate_recipes(request: RecipeRequest):
    prefs = request.preferences
    stream = llm_service.generate_recipes_stream(
        ingredients=request.ingredients,
        num_recipes=prefs.num_recipes,
        cuisine=prefs.cuisine,
        dietary_restrictions=prefs.dietary_restrictions,
        max_cooking_minutes=prefs.max_cooking_minutes,
    )
    return StreamingResponse(stream, media_type="text/plain")
