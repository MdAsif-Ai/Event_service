from pymongo import MongoClient
from pymongo.errors import PyMongoError

from app.config import settings


client = MongoClient(
    settings.mongodb_url,
    serverSelectionTimeoutMS=5000,
)

database = client[settings.mongodb_database]

events_collection = database["events"]


def check_database_connection() -> bool:
    """Check whether MongoDB is reachable."""

    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False