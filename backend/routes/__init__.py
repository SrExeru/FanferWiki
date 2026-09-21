from .users import user_router
from .auth import auth_router
from .profile import profile_router
from .communities import community_router

all_routes = [
    user_router,
    auth_router,
    profile_router,
    community_router
]