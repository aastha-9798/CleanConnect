from pydantic import BaseModel
from datetime import datetime

class CreateDriveRequest(BaseModel):
    report_id:int
    description:str
    scheduled_at:datetime