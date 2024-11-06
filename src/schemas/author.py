from pydantic import BaseModel, ConfigDict


class AuthorBaseSchema(BaseModel):
    name: str
    country: str


class AuthorCreateSchema(AuthorBaseSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)
