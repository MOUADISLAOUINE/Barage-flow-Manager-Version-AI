from app.api.v1.routes import sensors

app.include_router(sensors.router)