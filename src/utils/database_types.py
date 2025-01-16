from datetime import datetime
from typing import Annotated
 
from sqlalchemy import String, text
from sqlalchemy.orm import mapped_column


type_annotation_map = {
    'str_256': String(256)
}


str_256 = Annotated[str, 256]
created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
