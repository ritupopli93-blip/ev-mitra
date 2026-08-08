"""
Seed MongoDB with realistic charging station data for the EV-Mitra demo.

Usage:
    python seed_db.py
"""

import asyncio
from database import stations_collection

stations = [
    {
        "name": "Connaught Place Charging Hub", "distance_km": 2.1,
        "lat": 28.6315, "lng": 77.2167, "status": "available",
        "price_per_kwh": 18.5, "fast_charger": True, "city": "Delhi"
    },
    {
        "name": "Saket Select Citywalk", "distance_km": 3.4,
        "lat": 28.5286, "lng": 77.2190, "status": "available",
        "price_per_kwh": 12.0, "fast_charger": False, "city": "Delhi"
    },
    {
        "name": "Dwarka Sector 21 Metro", "distance_km": 4.7,
        "lat": 28.5523, "lng": 77.0586, "status": "available",
        "price_per_kwh": 19.0, "fast_charger": True, "city": "Delhi"
    },
    {
        "name": "Noida Sector 18", "distance_km": 6.0,
        "lat": 28.5708, "lng": 77.3260, "status": "available",
        "price_per_kwh": 15.0, "fast_charger": True, "city": "Noida"
    },
    {
        "name": "Gurgaon Cyber Hub", "distance_km": 7.3,
        "lat": 28.4950, "lng": 77.0890, "status": "available",
        "price_per_kwh": 18.5, "fast_charger": True, "city": "Gurgaon"
    },
    {
        "name": "Rohini Sector 10", "distance_km": 8.6,
        "lat": 28.7041, "lng": 77.1025, "status": "available",
        "price_per_kwh": 12.0, "fast_charger": False, "city": "Delhi"
    },
    {
        "name": "Lajpat Nagar Market", "distance_km": 9.9,
        "lat": 28.5677, "lng": 77.2431, "status": "busy",
        "price_per_kwh": 14.0, "fast_charger": False, "city": "Delhi"
    },
]


async def seed():
    await stations_collection.delete_many({})
    result = await stations_collection.insert_many(stations)
    print(f"✅ Inserted {len(result.inserted_ids)} stations")


if __name__ == "__main__":
    asyncio.run(seed())
