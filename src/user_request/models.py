from sqlalchemy.orm import Mapped

from src.database import Base, str_256
from src.utils.database_types import created_at

class UserRequest(Base):
    username: Mapped[str_256]
    description: Mapped[str]
    created_at: Mapped[created_at]
