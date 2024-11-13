"""Import all routers and add them to routers_list."""

from .start import router as start_router
from .tarot import router as tarot_router

routers_list = [
    start_router,
    tarot_router,
]

__all__ = [
    "routers_list",
]
