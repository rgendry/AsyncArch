from pydantic import BaseModel
from typing import Optional, List


class PaymentSchema(BaseModel):
    amount: int
    type: str
    user_id: str

    class Config:
        orm_mode = True


class PaymentsListSchema(BaseModel):
    payments: Optional[List[PaymentSchema]]

    class Config:
        orm_mode = True
