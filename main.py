from fastapi import FastAPI
from app.routes.admins import router as admin_router
from app.routes.providers import router as provider_router
from app.routes.requesters import router as requester_router
from app.routes.requests import router as request_router

app = FastAPI(title="Follow Them")

API_VERSION = "/api/v1"

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
