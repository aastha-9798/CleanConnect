from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from backend.database import engine, Base
from backend.authentication.routes import router as auth_router
from backend.reports.routes import router as reports_router
import os

app = FastAPI()

os.makedirs("uploads", exist_ok=True)

#mount uploads directory to serve images
app.mount("/uploads", StaticFiles(directory="uploads"))

# Create tables
Base.metadata.create_all(bind=engine)

# Include authentication routes
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(reports_router, prefix="/reports", tags=["Reports"]) 

@app.get("/")
def root():
    return {"message": "Clean Connect backend running"}

