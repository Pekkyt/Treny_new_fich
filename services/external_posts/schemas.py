from pydantic import BaseModel


class ExternalPostRead(BaseModel):
    userId: int
    id: int
    title: str
    body: str
