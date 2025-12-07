from fastapi import FastAPI

from app.routers import (
    users,
    activities,
    friends,
    challenges,
    leaderboard,
    admin,
)

app = FastAPI(
    title="Sporty API",
)


app.include_router(users.router)
app.include_router(activities.router)
app.include_router(friends.router)
app.include_router(challenges.router)
app.include_router(leaderboard.router)
app.include_router(admin.router)
# app.include_router(achievements.router)  # если есть
