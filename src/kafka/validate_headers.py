from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from schemas import AuthorCreateSchema, BookCreateSchema, TagCreateSchema


class ValidateMessage:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def update_schema(self, table_id: int, table: AuthorCreateSchema | BookCreateSchema | TagCreateSchema):
        result = await self.session.execute(select(table).where(table.id == table_id))
        data = result.scalar_one_or_none()
        if data:
            for k, v in table.model_dump(exclude_unset=True).items():
                setattr(data, k, v)
            self.session.add(data)
            await self.session.commit()
            await self.session.refresh(data)
            return data
        return None
