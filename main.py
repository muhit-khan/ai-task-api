from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.api import router as api_router
from app.settings import settings

app = FastAPI(
    title="AI Task API",
    description="An API for handling various AI tasks including Q&A, image generation, and content creation",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Mount frontend files
frontend_path = os.path.join(os.path.dirname(__file__), "app", "frontend")
if os.path.exists(frontend_path):
    app.mount("/frontend", StaticFiles(directory=frontend_path), name="frontend")

app.include_router(api_router)

# Serve the main page
@app.get("/")
async def root():
    return {"message": "AI Task API is running. Visit /frontend/index.html for the web interface."}

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Task API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)