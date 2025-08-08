from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from .api.routes import router as chat_router

app = FastAPI(title="Pleione AI Assistant", version="1.0.0")

# Include API routes
app.include_router(chat_router, prefix="/api")

# Serve frontend static files at root
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Root endpoint serves index.html directly
@app.get("/")
async def root():
    return FileResponse('frontend/index.html')

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)