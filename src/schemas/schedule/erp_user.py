from pydantic import BaseModel


class ErpUserSchema(BaseModel):
    token: str
    cabinet_id: int
