from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTAuthentication

from user.models import user_db
from user.schemas import User, UserCreate, UserDB, UserUpdate


auth_backends = []

fastapi_users = FastAPIUsers(
    user_db,
    auth_backends,
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

SECRET = "gjo#eirJgpOJgPJGP&eojGVpseo1*tipw)As8fqe5pf0jO"

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=3600 * 1000)

auth_backends.append(jwt_authentication)


current_active_user = fastapi_users.current_user(active=True)