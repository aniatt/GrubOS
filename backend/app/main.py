from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import detect, recipes
from app.services.vision import vision_service


@asynccontextmanager
async def lifespan(app: FastAPI):
    vision_service.load_model()
    yield


app = FastAPI(
    title="GrubOS",
    description="Identify ingredients from photos and generate recipes",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(detect.router, prefix="/api")
app.include_router(recipes.router, prefix="/api")


@app.get("/api/health")
async def health_check():
    from app.services.llm import llm_service

    return {
        "status": "ok",
        "vision_model_loaded": vision_service.model is not None,
        "ollama_reachable": await llm_service.check_connection(),
    }
