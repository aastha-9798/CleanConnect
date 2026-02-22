from fastapi import FastAPI
from backend.database import engine, Base
from backend.authentication.routes import router as auth_router

app = FastAPI()

# Create tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])

@app.get("/")
def root():
    return {"message": "Clean Connect backend running"}
