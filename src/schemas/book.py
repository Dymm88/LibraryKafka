from pydantic import BaseModel, ConfigDict


class BookBaseSchema(BaseModel):
    title: str
    created_at: int
    genre: str
    author_id: int


class BookCreateSchema(BookBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
