"""
Here live all the functions which get called during a request over Depends()
with these you get a database session and do the authentication
"""

from typing import Generator

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


async def get_db_schema(request: Request):
    """
    example code from: https://github.com/tiangolo/fastapi/issues/1333

    our idea: get tenant info from header and scopes from JWT
    """
    # Get db from subdomain
    # db_name = request.base_url.hostname.split(".")[0]

    # get tenant from header
    tenant_header: str = "HTTP_X_TENANT"
    if tenant_header not in request.headers:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"{tenant_header} is missing")
    tenant_name = request.headers[tenant_header]

    return tenant_name


def get_db(tenant_name: str = Depends(get_db_schema)) -> Generator:
    """
    Create a database session to create, read, update or delete database entries
    It will called for each requests which have to interact with the database
    """
    print(tenant_name)
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# This is just an example how to realize the oauth stuff
# def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> models.User:
#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
#         token_data = schemas.TokenPayload(**payload)
#     except (jwt.JWTError, ValidationError):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Could not validate credentials",
#         )
#     user = crud.user.get(db, id=token_data.sub)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user
