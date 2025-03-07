from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from app.api.router import api_router
from app.config import settings

app = FastAPI(
    title="LawGPT API",
    description="A legal chatbot API using RAG architecture",
    version="1.0.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# Define path to the React app build directory
REACT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "lawgpt-frontend/dist")

# Mount the static files from the React app
if os.path.exists(REACT_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(REACT_DIR, "assets")), name="assets")

@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    """Serve the React app for any path not matched by other routes."""
    if full_path.startswith("api/"):
        # This shouldn't happen since the API router is included first
        raise HTTPException(status_code=404, detail="API route not found")
    
    # For all other paths, serve the React app's index.html
    index_path = os.path.join(REACT_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {"message": "React frontend not found. Make sure to build it first."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)