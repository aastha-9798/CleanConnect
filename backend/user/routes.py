from fastapi import APIRouter, HTTPException , Depends , Request
from backend.database import get_db
from backend.authentication.dependencies import get_current_user
from backend.drives.models import Participation , Drive
from backend.reports.models import Report


from sqlalchemy.orm import Session 

router=APIRouter()

@router.get("/me/reports")
def get_my_reports(
    request:Request,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user),
):
    reports = db.query(Report).filter(Report.user_id == curr_user.id).all()
    result = []
    for report in reports:
        image_url = str(request.base_url) + report.image_path.replace("\\", "/")
        result.append({
            "id": report.id,
            "username": curr_user.username,
            "image_url": image_url,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "description": report.description,
            "status": report.status,
            "created_at": report.created_at
        })
    return result



@router.get("/me/drives")
def get_my_drives(
    request: Request,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    participations = db.query(Participation).filter(Participation.user_id == curr_user.id).all()

    drives_data = []

    for p in participations:
        drive = db.query(Drive).filter(Drive.id == p.drive_id).first()

        if not drive:
            continue

        report = db.query(Report).filter(Report.id == drive.report_id).first()

        if not report:
            continue

        participant_count = db.query(Participation).filter(Participation.drive_id == drive.id).count()

        image_url = str(request.base_url) + report.image_path.replace("\\", "/")

        drives_data.append({
            "drive_id": drive.id,
            "description": drive.description,
            "scheduled_at": drive.scheduled_at,
            "status": drive.status,
            "participant_count": participant_count,
            "latitude": report.latitude,
            "longitude": report.longitude,
            "image": image_url,
            "report": {
                "id": report.id,
                "description": report.description
            },
            "joined_at": p.joined_at
        })

    return {
        "drives": drives_data
    }

@router.get("/me/organized-drives")
def get_organized_drives(
    request: Request,
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    """Get all drives organized by the current user"""
    drives = db.query(Drive).filter(Drive.user_id == curr_user.id).all()
    
    drives_data = []
    for drive in drives:
        report = db.query(Report).filter(Report.id == drive.report_id).first()
        participant_count = db.query(Participation).filter(Participation.drive_id == drive.id).count()
        
        image_url = ""
        if report:
            image_url = str(request.base_url) + report.image_path.replace("\\", "/")
        
        drives_data.append({
            "drive_id": drive.id,
            "description": drive.description,
            "scheduled_at": drive.scheduled_at,
            "status": drive.status,
            "participant_count": participant_count,
            "latitude": drive.latitude,
            "longitude": drive.longitude,
            "image": image_url,
            "created_at": drive.created_at,
            "report": {
                "id": drive.report_id,
                "description": report.description if report else ""
            }
        })
    
    return {
        "drives": drives_data
    }

@router.get("/me/stats")
def get_user_stats(
    db: Session = Depends(get_db),
    curr_user = Depends(get_current_user)
):
    """Get user's activity statistics"""
    # Count reports submitted
    reports_count = db.query(Report).filter(Report.user_id == curr_user.id).count()
    
    # Count drives organized
    drives_organized = db.query(Drive).filter(Drive.user_id == curr_user.id).count()
    
    # Count drives participated in
    drives_participated = db.query(Participation).filter(Participation.user_id == curr_user.id).count()
    
    # Count total participants in organized drives
    total_participants = 0
    organized_drives = db.query(Drive).filter(Drive.user_id == curr_user.id).all()
    for drive in organized_drives:
        count = db.query(Participation).filter(Participation.drive_id == drive.id).count()
        total_participants += count
    
    return {
        "reports_submitted": reports_count,
        "drives_organized": drives_organized,
        "drives_participated": drives_participated,
        "total_participants_in_drives": total_participants
    }