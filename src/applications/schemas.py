from datetime import datetime

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime

class ApplicationCreateSchema(BaseModel):
    user_name: str
    description: str
