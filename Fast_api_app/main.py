from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import SessionLocal, engine
from db.base import Base
from routers import user_router

# Create FastAPI app instance
app = FastAPI()

# CORS middleware setup (allowing requests from any origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # In production, specify your frontend URL here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables on startup
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(user_router.router, prefix="/users", tags=["Users"])
# app.include_router(product_router.router, prefix="/products", tags=["Products"])

# Default route
@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


# Dependency for getting the DB session (to be used in endpoints)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

