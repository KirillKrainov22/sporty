from fastapi import FastAPI

from app.routers import (
    users,
    activities,
    friends,
    challenges,
    leaderboard,
)

app = FastAPI(
    title="Sporty API",
    version="0.1.0",
)

# если у тебя уже был какой-то healthcheck – оставь его

app.include_router(users.router, prefix="/api")
app.include_router(activities.router, prefix="/api")
app.include_router(friends.router, prefix="/api")
app.include_router(challenges.router, prefix="/api")
app.include_router(leaderboard.router, prefix="/api")
