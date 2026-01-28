from pydantic import BaseModel

class SuggestRequest(BaseModel):
    id:str
    title: str
    category: str
    brand: str
    condition: str
    age_months: str
    asking_price: str
    location: str


class SuggestResponse(BaseModel):
    fair_price_range: str
    reasoning: str
    is_fraud: bool


class ModerationRequest(BaseModel):
    incoming_message: str


class ModerationResponse(BaseModel):
    status: str
    reason: str
