from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.api.routers import upload_routes, assessment_routes, dashboard_routes

app = FastAPI(
    title="Catalyst Backend API",
    description="Multi-Agent Pipeline for Skill Assessment",
    version="1.0.0"
)

# Configure CORS for local development (Frontend running on typical Streamlit port 8501)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount the routers
app.include_router(upload_routes.router, prefix="/api/v1/ingest", tags=["Ingestion"])
app.include_router(assessment_routes.router, prefix="/api/v1/assessment", tags=["Interview"])
app.include_router(dashboard_routes.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

@app.get("/health")
async def health_check():
    """Simple check to ensure the server is running."""
    return {"status": "online", "system": "Catalyst Core"}