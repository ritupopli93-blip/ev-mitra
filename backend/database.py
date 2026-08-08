"""
EV-Mitra database connection.

Uses Motor (the async MongoDB driver) so FastAPI's async endpoints can
query MongoDB without blocking. Reads the connection string from
backend/.env (MONGO_URI). Falls back to a local MongoDB instance if
that variable isn't set.
"""

import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=3000)
db = client["evmitra"]

stations_collection = db["stations"]
