from datetime import datetime

from pydantic import BaseModel


class ApplicationSchema(BaseModel):
    id: int
    username: str
    description: str
    created_at: str

class ApplicationCreateSchema(BaseModel):
    username: str
    description: str
