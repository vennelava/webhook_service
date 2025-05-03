from pydantic import BaseModel, HttpUrl

class SubscriptionCreate(BaseModel):
    url: HttpUrl
    secret: str
    event_type: str

class SubscriptionOut(SubscriptionCreate):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
