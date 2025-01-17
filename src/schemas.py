from pydantic import BaseModel


class NotFoundScheme(BaseModel):
    """Схема 404 NotFound."""
    message: str = 'NotFound'
    description: str = 'Объект не найден'
