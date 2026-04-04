from urllib import request

from fastapi import APIRouter, HTTPException, UploadFile, File , Form , Depends #depends used to use dependencies
from fastapi import Form, Query
from fastapi import Request
from backend.database import get_db
from sqlalchemy.orm import Session #to type hint the database session
from backend.authentication.dependencies import get_current_user
from backend.reports.models import Report
from backend.reports.schemas import ReportResponse
import uuid
import os
import math

router = APIRouter()

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates in kilometers"""
    R = 6371  # Earth's radius in kilometers
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    
    return R * c

@router.get("/nearby", response_model=list[ReportResponse])
async def get_nearby_reports(
    request: Request,
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10.0),
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    """Get all reports within a specified radius (default 10km) from given coordinates"""
    all_reports = db.query(Report).all()
    
    nearby_reports = []
    for report in all_reports:
        distance = haversine_distance(latitude, longitude, report.latitude, report.longitude)
        if distance <= radius_km:
            try:
                image_url = str(request.base_url) + report.image_path.replace("\\", "/")
                nearby_reports.append(ReportResponse(
                    id=report.id,
                    username=report.user.username if report.user else "Unknown",
                    image_url=image_url,
                    latitude=report.latitude,
                    longitude=report.longitude,
                    description=report.description,
                    status=report.status,
                    created_at=report.created_at
                ))
            except Exception as e:
                print(f"Error building nearby report response: {e}")
                continue
    
    return nearby_reports

@router.get("/feed", response_model=list[ReportResponse])
async def get_all_reports(
    request: Request,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    """Get all reports (community feed)"""
    all_reports = db.query(Report).order_by(Report.created_at.desc()).all()
    
    # Build response with image URLs
    response_list = []
    for report in all_reports:
        try:
            image_url = str(request.base_url) + report.image_path.replace("\\", "/")
            response_list.append(ReportResponse(
                id=report.id,
                username=report.user.username if report.user else "Unknown",
                image_url=image_url,
                latitude=report.latitude,
                longitude=report.longitude,
                description=report.description,
                status=report.status,
                created_at=report.created_at
            ))
        except Exception as e:
            print(f"Error building report response: {e}")
            continue
    
    return response_list

@router.get("/my-reports", response_model=list[ReportResponse])
async def get_user_reports(
    request: Request,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    """Get all reports submitted by the current user"""
    reports = db.query(Report).filter(Report.user_id == curr_user.id).all()
    
    # Build response with image URLs
    response_list = []
    for report in reports:
        try:
            image_url = str(request.base_url) + report.image_path.replace("\\", "/")
            response_list.append(ReportResponse(
                id=report.id,
                username=report.user.username if report.user else "Unknown",
                image_url=image_url,
                latitude=report.latitude,
                longitude=report.longitude,
                description=report.description,
                status=report.status,
                created_at=report.created_at
            ))
        except Exception as e:
            print(f"Error building user report response: {e}")
            continue
    
    return response_list

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

@router.delete("/{report_id}")
async def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    """Delete a report by ID (only the owner can delete)"""
    report = db.query(Report).filter(Report.id == report_id).first()
    
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Check if the report belongs to the current user
    if report.user_id != curr_user.id:
        raise HTTPException(status_code=403, detail="You can only delete your own reports")
    
    # Delete the image file from the filesystem
    if os.path.exists(report.image_path):
        try:
            os.remove(report.image_path)
        except Exception as e:
            print(f"Error deleting image file: {e}")
    
    # Delete the report from the database
    db.delete(report)
    db.commit()
    
    print(f"Report {report_id} deleted by user {curr_user.username}")
    return {"message": "Report deleted successfully"}


