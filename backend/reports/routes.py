from urllib import request

from fastapi import APIRouter, HTTPException, UploadFile, File , Form , Depends #depends used to use dependencies
from fastapi import Form
from fastapi import Request
from backend.database import get_db
from sqlalchemy.orm import Session #to type hint the database session
from backend.authentication.dependencies import get_current_user
from backend.reports.models import Report
from backend.reports.schemas import ReportResponse
import uuid
import os

router = APIRouter()

@router.post("/upload", response_model=ReportResponse)
async def get_data(
    request : Request,
    image: UploadFile= File(...), # ... means this field is required
    latitude: float= Form(...),
    longitude: float= Form(...),
    description: str= Form(None), # none means this field is optional
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    if latitude < -90 or latitude > 90:
        raise HTTPException(status_code=400, detail="Invalid latitude value")
    if longitude < -180 or longitude > 180:
        raise HTTPException(status_code=400, detail="Invalid longitude value")  
    if not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only images are allowed.")

    #size check
    contents= await image.read()
    if len(contents) > 5*1024*1024:
        raise HTTPException(status_code=400, detail="File size exceeds the limit of 5MB.")
    
    name, ext = os.path.splitext(image.filename)
    new_filename= str(uuid.uuid4()) + ext
    file_path=os.path.join("uploads", new_filename)
    with open(file_path, "wb") as f:
        f.write(contents)
    
    report = Report(
        user_id= curr_user.id,
        image_path=file_path,
        latitude=latitude,
        longitude=longitude,
        description=description
    )
    db.add(report)
    db.commit()
    db.refresh(report)
    print("Report created with ID:", report.id , "by user:", curr_user.username)

    #building image url to send in response
    image_url = str(request.base_url) + report.image_path.replace("\\", "/")
    return {
        "id": report.id,
        "username": report.user.username,
        "image_url": image_url,
        "latitude": report.latitude,
        "longitude": report.longitude,
        "description": report.description,
        "status": report.status,
        "created_at": report.created_at
    }

@router.get("/my-reports")
def get_my_reports(
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    reports = db.query(Report).filter(Report.user_id == curr_user.id).all()
    result = []
    for report in reports:
        image_url = f"/{report.image_path.replace('\\', '/')}"
        result.append({
            "id": report.id,
            "image_url": image_url,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "description": report.description,
            "status": report.status,
            "created_at": report.created_at
        })
    return result

@router.get("/feed")
def get_feed(
    db: Session = Depends(get_db),
    limit: int = 20,
):
    # Return the most recent reports across all users
    reports = (
        db.query(Report)
        .order_by(Report.created_at.desc())
        .limit(limit)
        .all()
    )

    result = []
    for report in reports:
        image_url = f"/{report.image_path.replace('\\', '/')}"
        result.append({
            "id": report.id,
            "username": report.user.username,
            "image_url": image_url,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "description": report.description,
            "status": report.status,
            "created_at": report.created_at,
        })
    return result