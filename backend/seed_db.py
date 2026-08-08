"""
Run this once to populate your MongoDB database with sample
charging station data.

Usage:
    python seed_db.py
"""

import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["evmitra"]
stations = db["stations"]

sample_stations = [
    {"name": "Station A", "distance_km": 2.1, "status": "available",
     "price_per_kwh": 18, "waiting_vehicles": 0, "fast_charger": True},
    {"name": "Station B", "distance_km": 3.4, "status": "busy",
     "price_per_kwh": 16, "waiting_vehicles": 4, "fast_charger": False},
    {"name": "Station C", "distance_km": 5.2, "status": "available",
     "price_per_kwh": 20, "waiting_vehicles": 0, "fast_charger": True},
    {"name": "Station D", "distance_km": 6.8, "status": "available",
     "price_per_kwh": 17, "waiting_vehicles": 1, "fast_charger": True},
]

for s in sample_stations:
    stations.update_one({"name": s["name"]}, {"$set": s}, upsert=True)

print(f"✅ Seeded {len(sample_stations)} stations into MongoDB at {MONGO_URI}")
print("Collections in 'evmitra' database:", db.list_collection_names())
