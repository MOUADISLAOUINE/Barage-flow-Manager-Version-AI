from fastapi import APIRouter

from app.api.v1.routes import auth, users

router = APIRouter()

router.include_router(auth.router, prefix="/auth", tags=["Auth"])
router.include_router(users.router, prefix="/users", tags=["Users"])
# Add other routers here as they are created
# router.include_router(dams.router, prefix="/dams", tags=["Dams"])
