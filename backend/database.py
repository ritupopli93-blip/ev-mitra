"""
EV-Mitra database connection.

Uses Motor (the async MongoDB driver) so FastAPI's async endpoints can
query MongoDB without blocking. Reads the connection string from
backend/.env (MONGO_URI). Falls back to a local MongoDB instance if
that variable isn't set.

tlsCAFile=certifi.where() fixes SSL handshake errors that commonly
happen when connecting to MongoDB Atlas from cloud hosts (Render,
Railway, etc.) whose default CA bundles are outdated.
"""

import os
import certifi
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Only Atlas (mongodb+srv://) connections need the explicit CA bundle;
# a plain local mongodb:// connection doesn't use TLS.
if MONGO_URI.startswith("mongodb+srv://"):
    client = AsyncIOMotorClient(
        MONGO_URI, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where()
    )
else:
    client = AsyncIOMotorClient(MONGO_URI, serverSelectionTimeoutMS=5000)

db = client["evmitra"]
stations_collection = db["stations"]
