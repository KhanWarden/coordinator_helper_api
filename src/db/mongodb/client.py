from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

MONGO_URL = "mongodb://mongo:27017"
MONGO_DB_NAME = "team_schedule_db"

client = AsyncIOMotorClient(MONGO_URL)
db: AsyncIOMotorDatabase = client[MONGO_DB_NAME]


def get_teams_collection():
    return db["teams"]


def get_schedules_collection():
    return db["schedules"]
