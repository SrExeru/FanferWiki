from .users import user_router
from .communities import community_router
from .auth import auth_router

all_routes = [
    user_router,
    auth_router,
    community_router
]