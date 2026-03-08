from fastapi import APIRouter
from app.api.v1.routes import auth, dam, sensors, cooperatives, release_orders, forecast, admin

api_router = APIRouter()

api_router.include_router(auth.router,          prefix="/auth",          tags=["Authentication"])
api_router.include_router(dam.router,           prefix="/dam",           tags=["Dam Status"])
api_router.include_router(sensors.router,       prefix="/sensors",       tags=["Sensors"])
api_router.include_router(cooperatives.router,  prefix="/cooperatives",  tags=["Cooperatives"])
api_router.include_router(release_orders.router,prefix="/release-orders",tags=["Release Orders"])
api_router.include_router(forecast.router,      prefix="/forecast",      tags=["Forecast & AI"])
api_router.include_router(admin.router,         prefix="/admin",         tags=["Administration"])
