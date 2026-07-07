from fastapi import FastAPI

from backend.core import settings

from backend.database.init_db import init_db

from backend.api.auth_routes import router as auth_router

from backend.api.customer_routes import router as customer_router

from backend.api.transaction_routes import router as transaction_router

from backend.api.analytics_routes import router as analytics_router

app = FastAPI(
    title=settings.app.app_name,
    version=settings.app.app_version,
)

@app.on_event("startup")
def startup():

    init_db()


@app.get("/")
def home():
 
    return {
        "project": settings.app.app_name,
        "version": settings.app.app_version,
        "status": "Running"
    }

app.include_router(auth_router)

app.include_router(customer_router)

app.include_router(transaction_router)

app.include_router(analytics_router)