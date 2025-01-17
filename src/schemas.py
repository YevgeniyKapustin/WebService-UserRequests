from pydantic import BaseModel

class OkScheme(BaseModel):
    """Scheme 200 OK."""
    message: str = 'OK'
    description: str = 'Выполнено'


class CreateScheme(BaseModel):
    """Scheme 201 Create."""
    message: str = 'Create'
    description: str = 'Создано'


class NotFoundScheme(BaseModel):
    """Scheme 404 NotFound."""
    message: str = 'NotFound'
    description: str = 'Объект не найден'
