from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.schemas import PaymentsListSchema
from app.models import Payment
from app.db import get_db


router = APIRouter()


@router.post("/payments/", status_code=status.HTTP_200_OK, response_model=PaymentsListSchema)
async def get_payments(db: AsyncSession = Depends(get_db),) -> PaymentsListSchema:
    payments = await Payment.all(db)
    response = PaymentsListSchema.parse_obj({"payments": payments})
    return response
