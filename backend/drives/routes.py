from fastapi import APIRouter, Depends, HTTPException
from backend.database import get_db #actual session provider
from sqlalchemy.orm import Session #session type hint
from datetime import datetime , timezone

from backend.authentication.dependencies import get_current_user
from backend.reports.models import Report
from backend.drives.models import Drive , Participation
from backend.drives.schemas import CreateDriveRequest

router = APIRouter()

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