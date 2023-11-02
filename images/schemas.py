from pydantic import BaseModel


class PostImage(BaseModel):
    path: str


class Image(BaseModel):
    id: int

    class Config:
        from_attributes = True