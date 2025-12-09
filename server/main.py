import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# 1. Load environment variables
load_dotenv()

# 2. Import the router in a way that works whether this file is executed
# as a module (`python -m server.main`) or as a script (`python main.py`).
try:
    # Preferred when running as a module
    from .api.routes import router as api_router
except Exception:
    # Fallback when running as a script: make the `api` package importable
    import sys
    from pathlib import Path
    # Ensure the project root is on sys.path so `server` is importable
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from server.api.routes import router as api_router

app = FastAPI(title="Safahomes SDXL FastAPI")

# 3. CORS Configuration (Allows your React frontend to talk to this backend)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 4. Include the routes
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"status": "ok", "service": "Safahomes Backend Running"}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    # host="0.0.0.0" makes it accessible on the network
    # Prefer running uvicorn with an import string so reload works.
    try:
        uvicorn.run("server.main:app", host="0.0.0.0", port=port, reload=True)
    except Exception:
        # Fallback: run the app object without reload (works when run as script)
        uvicorn.run(app, host="0.0.0.0", port=port, reload=False)