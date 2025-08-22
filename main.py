from fastapi import FastAPI
from app.api import router as api_router

app = FastAPI(
    title="AI Task API",
    description="An API for handling various AI tasks including Q&A, image generation, and content creation",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Task API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)