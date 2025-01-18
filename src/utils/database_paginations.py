from sqlalchemy import Select


def paginate_query(
        query: Select, 
        page: int | None = None, 
        size: int | None = None
    ) -> Select:
    if size:
        query = query.limit(size)
        if page:
            query = query.offset((page - 1) * size)
    return query
