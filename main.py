from fastapi import FastAPI
from app.routes.admins import router as admin_router
from app.routes.providers import router as provider_router
from app.routes.requesters import router as requester_router
from app.routes.requests import router as request_router
from app.database.config import database, sqlalchemy_engine
from app.database.models import Base
from fastapi.openapi.utils import get_openapi

# app instance of FastAPI
app = FastAPI()

# Function to personalize the API
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Follow Them",
        version="1.0.0",
        description="This API was created to follow and accomplish the purchase requests "
        "made by user at Laboratorios ROWE.",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://blog.electroica.com/wp-content/uploads/2020/10/Fastapi.jpg"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

# Connecting and disconnecting database
@app.on_event("startup")
async def startup():
    await database.connect()
    Base.metadata.create_all(sqlalchemy_engine)


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


# variable to indicate the API version in the URLs
API_VERSION = "/api/v1"

# Including routes
app.include_router(
    router=admin_router, prefix=API_VERSION + "/admins", tags=["Administrators"]
)
app.include_router(
    router=requester_router, prefix=API_VERSION + "/requesters", tags=["Requesters"]
)
app.include_router(
    router=request_router, prefix=API_VERSION + "/requests", tags=["Purchase Requests"]
)
app.include_router(
    router=provider_router, prefix=API_VERSION + "/providers", tags=["Providers"]
)
