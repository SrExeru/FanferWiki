from .users import user_router
from .communities import community_router

all_routes = [
    user_router,
    community_router
]