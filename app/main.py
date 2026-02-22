from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import organizations, buildings

app = FastAPI(
    title="Справочник организаций API",
    description="REST API для справочника организаций, зданий и видов деятельности.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(organizations.router)
app.include_router(buildings.router)

@app.get("/health")
def health():
    return {"status": "ok"}
