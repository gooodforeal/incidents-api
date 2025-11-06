from fastapi import FastAPI
from app.incidents.router import router as incidents_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="API для управления инцидентами",
    version=settings.app_version,
)

app.include_router(incidents_router)


@app.get("/")
async def root():
    return {"message": settings.app_name}

