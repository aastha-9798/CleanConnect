from fastapi import APIRouter, HTTPException , Depends
from backend.database import get_db
from backend.authentication.dependencies import get_current_user
from backend.drives.models import Participation


from sqlalchemy.orm import Session 

router=APIRouter()

@router.get("/me/drives")
def get_my_drives(
    db: Session= Depends(get_db),
    curr_user= Depends(get_current_user)
):
    participations = db.query(Participation).filter( Participation.user_id==curr_user.id).all()
    