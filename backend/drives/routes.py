from fastapi import APIRouter, Depends, HTTPException , Request, Query
from backend.database import get_db #actual session provider
from sqlalchemy.orm import Session #session type hint
from datetime import datetime , timezone
import math

from backend.authentication.dependencies import get_current_user
from backend.reports.models import Report
from backend.drives.models import Drive , Participation
from backend.drives.schemas import CreateDriveRequest, DriveResponse

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

@router.get("/nearby", response_model=list[DriveResponse])
async def get_nearby_drives(
    request: Request,
    latitude: float = Query(...),
    longitude: float = Query(...),
    radius_km: float = Query(10.0),
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    """Get all drives within a specified radius (default 10km) from given coordinates"""
    from backend.authentication.models import User
    
    all_drives = db.query(Drive).filter(Drive.status == "planned").all()
    
    nearby_drives = []
    for drive in all_drives:
        distance = haversine_distance(latitude, longitude, drive.latitude, drive.longitude)
        if distance <= radius_km:
            # Get creator username
            creator = db.query(User).filter(User.id == drive.user_id).first()
            creator_username = creator.username if creator else "Unknown"
            
            nearby_drives.append({
                "id": drive.id,
                "report_id": drive.report_id,
                "user_id": drive.user_id,
                "creator_username": creator_username,
                "description": drive.description,
                "scheduled_at": drive.scheduled_at,
                "latitude": drive.latitude,
                "longitude": drive.longitude,
                "status": drive.status,
                "created_at": drive.created_at
            })
    
    # Sort by scheduled date (nearest date first)
    nearby_drives.sort(key=lambda x: x["scheduled_at"])
    return nearby_drives

@router.get("/joined/my-drives")
async def get_user_joined_drives(
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    """Get list of drive IDs that the current user has joined"""
    participations = db.query(Participation).filter(Participation.user_id == curr_user.id).all()
    drive_ids = [p.drive_id for p in participations]
    return {"joined_drive_ids": drive_ids}

@router.get("/has-drive/{report_id}")
async def has_drive_for_report(
    report_id: int,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    """Check if a report already has an existing planned drive"""
    drive = db.query(Drive).filter(
        (Drive.report_id == report_id) & 
        (Drive.status == "planned")
    ).first()
    return {"has_drive": drive is not None, "drive_id": drive.id if drive else None}

@router.post("/")
def create_drive(
    drive_data: CreateDriveRequest,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    report= db.query(Report).filter(Report.id== drive_data.report_id).first()
    if not report:
        raise HTTPException(status_code=404 , detail="Report does not exist")
    
    existing_drive= db.query(Drive).filter((Drive.report_id== drive_data.report_id) & (Drive.status=="planned")).first()
    if existing_drive:
        raise HTTPException(status_code=409 , detail="Drive already exists")
    
    if drive_data.scheduled_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400 , detail="Invalid time ")
    
    new_drive = Drive(
        report_id= drive_data.report_id,
        user_id=curr_user.id,
        description= drive_data.description,
        scheduled_at=drive_data.scheduled_at,
        latitude=report.latitude,
        longitude=report.longitude
    )
    db.add(new_drive)
    db.commit()
    db.refresh(new_drive)
    print("Drive created with ID:", new_drive.id , "by user:", curr_user.username)

    return{
        "id": new_drive.id,
        "report_id": new_drive.report_id,
        "latitude": new_drive.latitude,
        "longitude": new_drive.longitude,
        "description": new_drive.description,
        "status": new_drive.status,
        "created_at": new_drive.created_at,
        "scheduled_at": new_drive.scheduled_at
    }

@router.post("/{drive_id}/join")
def join_drive(
    drive_id:str,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    drive= db.query(Drive).filter(Drive.id== drive_id).first()
    if not drive :
        raise HTTPException(status_code=404 , detail="drive does not exist")
    
    existing_participation = db.query(Participation).filter((Participation.user_id==curr_user.id) & (Participation.drive_id== drive.id)).first()
    if existing_participation:
        raise HTTPException(status_code=400 , detail="User already participated in this drive")

    new_participation=Participation(
        user_id= curr_user.id,
        drive_id= drive.id
    )
    db.add(new_participation)
    db.commit()
    db.refresh(new_participation)

    return {
        "message": "participated successfully",
        "drive_id": new_participation.drive_id
    }

@router.delete("/{drive_id}/leave")
def leave_drive(
    drive_id:str,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    drive= db.query(Drive).filter(Drive.id== drive_id).first()
    if not drive :
        raise HTTPException(status_code=404 , detail="drive does not exist")
    
    participation = db.query(Participation).filter((Participation.drive_id==drive_id) & (Participation.user_id==curr_user.id)).first()
    if not participation:
        raise HTTPException(status_code=404 , detail="participation does not exist")
    db.delete(participation)
    db.commit()
    return {
        "message": "participation removed successfully"
    }

@router.get("/{drive_id}")
async def get_drive_details(
    drive_id: str,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    """Get drive details including participants"""
    from backend.authentication.models import User
    
    drive = db.query(Drive).filter(Drive.id == drive_id).first()
    if not drive:
        raise HTTPException(status_code=404, detail="Drive does not exist")
    
    # Get creator username
    creator = db.query(User).filter(User.id == drive.user_id).first()
    creator_username = creator.username if creator else "Unknown"
    
    # Get participants with their usernames
    participants = db.query(Participation).filter(Participation.drive_id == drive_id).all()
    participant_list = []
    for p in participants:
        user = db.query(User).filter(User.id == p.user_id).first()
        if user:
            participant_list.append({
                "user_id": p.user_id,
                "username": user.username,
                "joined_at": p.joined_at
            })
    
    return {
        "id": drive.id,
        "report_id": drive.report_id,
        "user_id": drive.user_id,
        "creator_username": creator_username,
        "description": drive.description,
        "scheduled_at": drive.scheduled_at,
        "latitude": drive.latitude,
        "longitude": drive.longitude,
        "status": drive.status,
        "created_at": drive.created_at,
        "participants": participant_list
    }

@router.get("/feed")
def get_feed(
    request: Request,
    db: Session = Depends(get_db)
):
    reports = db.query(Report).all()

    with_drives = []
    without_drives = []

    for report in reports:
        drive = db.query(Drive).filter((Drive.report_id == report.id) &(Drive.status == "planned")).first()

        if drive:
            count = db.query(Participation).filter(Participation.drive_id == drive.id).count()

            image_url =  str(request.base_url) + report.image_path.replace("\\", "/")

            with_drives.append({
                "drive_id": drive.id,
                "description": drive.description,
                "scheduled_at": drive.scheduled_at,
                "participant_count": count,
                "latitude": report.latitude,
                "longitude": report.longitude,
                "image": image_url,
                "report": {
                    "id": report.id,
                    "description": report.description
                }
            })

        else:
            image_url = str(request.base_url) + report.image_path.replace("\\", "/")

            without_drives.append({
                "id": report.id,
                "description": report.description,
                "latitude": report.latitude,
                "longitude": report.longitude,
                "image": image_url
            })

    return {
        "drives": with_drives,
        "reports": without_drives
    }



#  REST mapping
# POST → create
# GET → read
# PUT/PATCH → update
# DELETE → remove