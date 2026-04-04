from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class CreateDriveRequest(BaseModel):
    report_id:int
    description:str
    scheduled_at:datetime

class ParticipantInfo(BaseModel):
    user_id: str
    username: str
    joined_at: datetime

    model_config = {
        "from_attributes": True
    }

class DriveResponse(BaseModel):
    id: str
    report_id: int
    user_id: str
    creator_username: Optional[str] = None
    description: str
    scheduled_at: datetime
    latitude: float
    longitude: float
    status: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }

class DriveDetailResponse(BaseModel):
    id: str
    report_id: int
    user_id: str
    creator_username: str
    description: str
    scheduled_at: datetime
    latitude: float
    longitude: float
    status: str
    created_at: datetime
    participants: List[ParticipantInfo] = []

    model_config = {
        "from_attributes": True
    }