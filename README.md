# ⚡ EV-Mitra — Intelligent EV Mobility Platform

AI-powered platform that predicts EV charging demand, recommends optimal
charging stations, and provides battery-aware route optimization.
Built as an ideathon prototype.

## Tech Stack
| Layer | Technology |
|---|---|
| Frontend | React.js + Tailwind CSS |
| Backend | FastAPI (Python) |
| Database | MongoDB Atlas |
| AI/ML | Scikit-learn, XGBoost, Pandas, NumPy |
| Maps | Google Maps API / OpenStreetMap |
| Charts | Chart.js / Plotly |
| Auth | Firebase Auth or JWT |
| Deployment | Render / Vercel |

## Project structure
```
ev-mitra/
├── backend/
│   ├── main.py            # FastAPI app with mock EV-Mitra endpoints
│   └── requirements.txt
├── frontend/
│   └── index.html         # React (CDN) + Tailwind demo UI, no build step
└── README.md
```

## Run it locally

### 1. Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs at `http://localhost:8000`. Interactive API docs at
`http://localhost:8000/docs`.

### 2. Frontend
No build step needed for the demo — just open `frontend/index.html`
directly in your browser, or serve it:
```bash
cd frontend
python -m http.server 5500
```
Then visit `http://localhost:5500`.

> The frontend currently calls mock endpoints on the backend. Swap in
> real ML models, MongoDB queries, and the Google Maps API as you build
> the platform out further.

## Roadmap / features to extend
- [ ] Real route optimization (Google Directions API + battery model)
- [ ] MongoDB Atlas integration for stations & historical demand
- [ ] Trained XGBoost demand-forecast model per station
- [ ] EV mobility heatmap on a real map (Leaflet / Google Maps)
- [ ] AI charging station placement recommender
- [ ] Firebase authentication
- [ ] Deploy backend to Render, frontend to Vercel
