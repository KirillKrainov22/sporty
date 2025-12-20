from fastapi import FastAPI
from app.core.kafka_producer import init_kafka_producer, close_kafka_producer
from app.routers import (
    users,
    activities,
    friends,
    challenges,
    leaderboard,
    admin,
    achievements,
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
app.include_router(achievements.router)

# пока не надо кбирать комменты тк не запуститься сваггер. Сейчас все эндпоинты работают
@app.on_event("startup")
async def startup():
    await init_kafka_producer()

@app.on_event("shutdown")
async def shutdown():
    await close_kafka_producer()

#kom