"""api/v1/routes/cooperatives.py"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.cooperative import Cooperative
from app.core.rbac import require_water_access
from app.models.user import Utilisateur as User

router = APIRouter()


@router.get("/")
async def list_cooperatives(
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    return db.query(Cooperative).all()


@router.get("/{coop_id}")
async def get_cooperative(
    coop_id: int,
    current_user: User = Depends(require_water_access),
    db: Session = Depends(get_db),
):
    coop = db.query(Cooperative).filter(Cooperative.id == coop_id).first()
    if not coop:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Cooperative not found.")
    return coop
