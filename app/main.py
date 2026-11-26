import time

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.routers.auth import auth_router
from app.api.routers.options import options_router
from app.api.routers.participants import participant_router
from app.api.routers.swipes import swipes_router
from app.api.routers.rooms import rooms_router
from app.api.routers.results import results_router



app = FastAPI(title="Room Voting API", version="1.0.0")

app.include_router(auth_router)
app.include_router(options_router)
app.include_router(participant_router)
app.include_router(swipes_router)
app.include_router(rooms_router)
app.include_router(results_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)