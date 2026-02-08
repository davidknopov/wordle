from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import games_router

app = FastAPI(
    title="Wordle API",
    description="A full-stack Wordle clone with configurable word lengths",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(games_router)


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
