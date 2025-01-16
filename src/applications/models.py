from sqlalchemy.orm import Mapped

from src.database import Base
from src.utils.database_types import created_at, str_256

class Application(Base):
    username: Mapped[str_256]
    description: Mapped[str]
    created_at: Mapped[created_at]
