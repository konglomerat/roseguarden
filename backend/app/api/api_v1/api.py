"""
Collect all endpoints and add them to APIRouter
By comment out one of the include_router lines, you disable all endpoints which are related to this entity
"""

from fastapi import APIRouter

# from app.api.api_v1.endpoints import initial_boneycomb, marktteilnehmer, tenants, transactions, users

api_router = APIRouter()
# api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(initial_boneycomb.router, prefix="/initial-boneycomb", tags=["initial-boneycomb"])
# api_router.include_router(marktteilnehmer.router, prefix="/marktteilnehmer", tags=["marktteilnehmer"])
# api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
