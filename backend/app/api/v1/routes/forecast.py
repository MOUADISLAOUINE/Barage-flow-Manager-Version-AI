"""api/v1/routes/forecast.py"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.forecast import ForecastResult
from app.core.rbac import require_water_access
from app.models.user import Utilisateur as User

router = APIRouter()


@router.get("/latest")
async def get_latest_forecast(
    dam_id: int = 1,
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    forecast = (
        db.query(ForecastResult)
        .filter(ForecastResult.dam_id == dam_id)
        .order_by(ForecastResult.generated_at.desc())
        .first()
    )
    if not forecast:
        raise HTTPException(status_code=404, detail="No forecast available yet.")
    return forecast
