"""
EV-Mitra Backend — FastAPI
Intelligent EV Mobility Platform (Ideathon Prototype)

Run locally:
    pip install -r requirements.txt
    uvicorn main:app --reload

All endpoints below return realistic MOCK data so the frontend has
something to render immediately. Swap the mock logic for real ML
models / MongoDB queries as you build the platform out further.
"""

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import random

from database import client as mongo_client, stations_collection

app = FastAPI(title="EV-Mitra API", version="0.1.0")

# Allow the frontend (any origin, fine for a hackathon demo) to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def check_mongo_connection():
    try:
        await mongo_client.admin.command("ping")
        print("✅ Connected to MongoDB")
    except Exception as e:
        print(f"⚠️  Could not connect to MongoDB: {e}")
        print("    /api/stations will fall back to mock data until this is fixed.")


@app.get("/")
def root():
    return {"message": "EV-Mitra API is running", "status": "ok"}


# ---------------------------------------------------------------------------
# 1. Battery-aware route planner
# ---------------------------------------------------------------------------
class RouteRequest(BaseModel):
    origin: str
    destination: str
    battery_percent: float


@app.post("/api/route-plan")
def route_plan(req: RouteRequest):
    routes = [
        {
            "name": "Route A",
            "distance_km": 32,
            "battery_required_pct": 25,
            "eta_minutes": 55,
            "charging_cost_inr": 120,
            "charging_station_available": False,
        },
        {
            "name": "Route B",
            "distance_km": 35,
            "battery_required_pct": 21,
            "eta_minutes": 48,
            "charging_cost_inr": 95,
            "charging_station_available": True,
        },
    ]
    recommended = min(routes, key=lambda r: r["eta_minutes"])
    return {
        "origin": req.origin,
        "destination": req.destination,
        "battery_percent": req.battery_percent,
        "routes": routes,
        "ai_recommendation": f"{recommended['name']} — lower estimated travel "
        f"time and {'sufficient' if recommended['charging_station_available'] else 'limited'} "
        f"charging availability.",
    }


# ---------------------------------------------------------------------------
# 2. Smart charging station finder — reads real stations from MongoDB
# ---------------------------------------------------------------------------
_FALLBACK_STATIONS = [
    {"name": "Connaught Place Charging Hub", "distance_km": 2.1, "status": "available",
     "price_per_kwh": 18.5, "fast_charger": True, "city": "Delhi"},
    {"name": "Saket Select Citywalk", "distance_km": 3.4, "status": "available",
     "price_per_kwh": 12.0, "fast_charger": False, "city": "Delhi"},
    {"name": "Gurgaon Cyber Hub", "distance_km": 7.3, "status": "available",
     "price_per_kwh": 18.5, "fast_charger": True, "city": "Gurgaon"},
]


@app.get("/api/stations")
async def find_stations(city: Optional[str] = None):
    try:
        query = {"city": city} if city else {}
        stations = await stations_collection.find(query, {"_id": 0}).to_list(length=100)
        if not stations:
            stations = _FALLBACK_STATIONS
    except Exception:
        stations = _FALLBACK_STATIONS

    # Recommend the closest available station
    available = [s for s in stations if s["status"] == "available"]
    best = min(available or stations, key=lambda s: s["distance_km"])
    return {"stations": stations, "ai_recommended": best["name"]}


class StationIn(BaseModel):
    name: str
    distance_km: float
    lat: Optional[float] = None
    lng: Optional[float] = None
    status: str  # "available" | "busy"
    price_per_kwh: float
    fast_charger: bool
    city: str


@app.post("/api/stations")
async def add_station(station: StationIn):
    """Add or update a charging station in MongoDB."""
    await stations_collection.update_one(
        {"name": station.name}, {"$set": station.model_dump()}, upsert=True
    )
    return {"message": f"Station '{station.name}' saved.", "station": station}


# ---------------------------------------------------------------------------
# 3. Charging demand prediction
# ---------------------------------------------------------------------------
@app.get("/api/demand-forecast")
def demand_forecast(station_id: str = "station_a"):
    hours = ["8 AM", "10 AM", "12 PM", "2 PM", "6 PM", "8 PM", "10 PM"]
    base = [3, 5, 7, 8, 10, 8, 3]
    forecast = [{"hour": h, "demand_index": d} for h, d in zip(hours, base)]
    peak = max(forecast, key=lambda f: f["demand_index"])
    return {"station_id": station_id, "forecast": forecast,
            "peak_hour": peak["hour"], "message": f"Expected high demand around {peak['hour']}"}


# ---------------------------------------------------------------------------
# 4. Dynamic re-routing recommendation
# ---------------------------------------------------------------------------
@app.get("/api/dynamic-recommendation")
def dynamic_recommendation():
    return {
        "warning": "Station A likely to become crowded in 15 minutes.",
        "alternative": {
            "name": "Station B",
            "extra_distance_km": 1.2,
            "predicted_wait_minutes": 2,
        },
        "original": {
            "name": "Station A",
            "predicted_wait_minutes": 22,
        },
    }


# ---------------------------------------------------------------------------
# 5. EV mobility heatmap (zone-level demand)
# ---------------------------------------------------------------------------
@app.get("/api/heatmap")
def heatmap():
    zones = []
    labels = ["Low", "Medium", "High", "Critical"]
    for i in range(1, 9):
        zones.append({
            "zone": f"Zone {chr(64 + i)}",
            "lat": 28.6 + random.uniform(-0.08, 0.08),
            "lng": 77.2 + random.uniform(-0.08, 0.08),
            "demand_level": random.choice(labels),
        })
    return {"zones": zones}


# ---------------------------------------------------------------------------
# 6. AI charging station placement suggestions
# ---------------------------------------------------------------------------
@app.get("/api/station-placement")
def station_placement():
    return {
        "recommended_zones": [
            {"zone": "Zone A", "current_demand": "HIGH", "existing_stations": 1, "predicted_growth": "HIGH"},
            {"zone": "Zone B", "current_demand": "HIGH", "existing_stations": 0, "predicted_growth": "HIGH"},
            {"zone": "Zone C", "current_demand": "MEDIUM", "existing_stations": 1, "predicted_growth": "HIGH"},
        ]
    }


# ---------------------------------------------------------------------------
# 7. Cost optimization modes
# ---------------------------------------------------------------------------
@app.get("/api/optimize")
def optimize(mode: str = Query("balanced", enum=["cheapest", "fastest", "greenest", "balanced"])):
    options = {
        "cheapest": {"route": "Route A", "cost_inr": 95, "eta_minutes": 60},
        "fastest": {"route": "Route B", "cost_inr": 130, "eta_minutes": 42},
        "greenest": {"route": "Route C", "cost_inr": 110, "eta_minutes": 52},
        "balanced": {"route": "Route B", "cost_inr": 110, "eta_minutes": 48},
    }
    return {"mode": mode, "recommendation": options[mode]}


# ---------------------------------------------------------------------------
# 8. Emergency / low-battery mode
# ---------------------------------------------------------------------------
@app.get("/api/emergency")
def emergency(battery_percent: float = Query(...)):
    if battery_percent > 15:
        return {"critical": False, "message": "Battery level is safe."}
    return {
        "critical": True,
        "message": "Critical battery. Rerouting to nearest safe, available charger.",
        "nearest_station": {"name": "Station A", "distance_km": 2.1, "status": "available"},
    }
