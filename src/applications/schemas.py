from datetime import datetime

from pydantic import BaseModel


class Application(BaseModel):
    id: int
    user_name: str
    description: str
    created_at: datetime
