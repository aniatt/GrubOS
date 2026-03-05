from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Ingredient(BaseModel):
    name: str
    confidence: float = Field(ge=0.0, le=1.0)
    bbox: BoundingBox


class DetectionResponse(BaseModel):
    ingredients: list[Ingredient]
    image_width: int
    image_height: int


class RecipePreferences(BaseModel):
    cuisine: str | None = None
    dietary_restrictions: list[str] = Field(default_factory=list)
    max_cooking_minutes: int | None = None
    num_recipes: int = Field(default=2, ge=1, le=5)


class RecipeRequest(BaseModel):
    ingredients: list[str]
    preferences: RecipePreferences = Field(default_factory=RecipePreferences)


class HealthResponse(BaseModel):
    status: str
    vision_model_loaded: bool
    ollama_reachable: bool
