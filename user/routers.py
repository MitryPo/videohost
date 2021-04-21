from fastapi import APIRouter

from user.api import on_after_register, send_sms, after_verification
from user.auth import SECRET, jwt_authentication, fastapi_users


user_router = APIRouter()


user_router.include_router(
    fastapi_users.get_auth_router(jwt_authentication), prefix="/auth/jwt", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_register_router(on_after_register), prefix="/auth", tags=["auth"]
)

user_router.include_router(
    fastapi_users.get_users_router(), prefix="/users", tags=["users"]
)

user_router.include_router(
    fastapi_users.get_verify_router(
        SECRET, after_verification_request=after_verification
    ), 
    prefix="/auth", 
    tags=["auth"]
)