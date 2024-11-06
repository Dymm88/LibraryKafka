from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from data import db_handler
from kafka.validate_headers import ValidateMessage
from schemas import BookCreateSchema, TagCreateSchema, AuthorCreateSchema


async def data_update(message: list[dict], session: AsyncSession = Depends(db_handler.get_db)):
    headers = message[0].keys()
    if "book" in headers:
        book_data = message[0]["book"]
        await ValidateMessage(session).update_schema(table_id=book_data["id"],
                                                     table=BookCreateSchema(**book_data))
    if "author" in headers:
        author_data = message[0]["author"]
        await ValidateMessage(session).update_schema(table_id=author_data["id"],
                                                     table=AuthorCreateSchema(**author_data))
    if "tag" in headers:
        tag_data = message[0]["tag"]
        await ValidateMessage(session).update_schema(table_id=tag_data["id"],
                                                     table=TagCreateSchema(**tag_data))
