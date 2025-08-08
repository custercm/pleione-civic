from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from .api.routes import router as chat_router

app = FastAPI(title="Pleione AI Assistant", version="1.0.0")

# Include API routes
app.include_router(chat_router, prefix="/api")

# Serve frontend static files
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Root endpoint redirect to frontend
@app.get("/")
async def root():
    return {"message": "Pleione AI Assistant API", "frontend": "/frontend/index.html"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)