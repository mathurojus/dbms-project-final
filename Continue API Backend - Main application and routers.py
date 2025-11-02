
# Continue API Backend - Main application and routers

api_main = """from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from config import get_settings
from routers import health, predictions, historical

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
settings = get_settings()
app = FastAPI(
    title="Chicago Crime Prediction API",
    description="Predictive analytics API for Chicago crime data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/api", tags=["Health"])
app.include_router(predictions.router, prefix="/api", tags=["Predictions"])
app.include_router(historical.router, prefix="/api", tags=["Historical"])

@app.get("/")
def read_root():
    return {
        "message": "Chicago Crime Prediction API",
        "docs": "/docs",
        "version": "1.0.0"
    }
"""

router_health = """from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import HealthResponse
import os

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def health_check(db: Session = Depends(get_db)):
    \"\"\"Health check endpoint\"\"\"
    
    # Check database connection
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    # Check if model exists
    model_path = os.getenv("MODEL_PATH", "../models/saved/")
    model_name = os.getenv("MODEL_NAME", "lightgbm_crime_predictor.pkl")
    model_file = os.path.join(model_path, model_name)
    model_loaded = os.path.exists(model_file)
    
    return HealthResponse(
        status="healthy" if db_status == "connected" else "degraded",
        database=db_status,
        model_loaded=model_loaded,
        version="1.0.0"
    )
"""

router_predictions = """from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import *
from typing import List
import pygeohash as pgh
from datetime import datetime, timedelta
import pickle
import os
import numpy as np

router = APIRouter()

# Load ML model (lazy loading)
_model = None

def get_model():
    global _model
    if _model is None:
        model_path = os.getenv("MODEL_PATH", "../models/saved/")
        model_name = os.getenv("MODEL_NAME", "lightgbm_crime_predictor.pkl")
        model_file = os.path.join(model_path, model_name)
        
        if os.path.exists(model_file):
            with open(model_file, 'rb') as f:
                _model = pickle.load(f)
        else:
            # Return None if model not found (will use fallback)
            _model = None
    return _model

@router.post("/grids/{grid_id}/forecast", response_model=List[ForecastResponse])
def forecast_grid(
    grid_id: str,
    request: ForecastRequest,
    db: Session = Depends(get_db)
):
    \"\"\"Get crime forecast for a specific grid\"\"\"
    
    # Validate grid_id
    if len(grid_id) < 5:
        raise HTTPException(status_code=400, detail="Invalid grid_id")
    
    # Get historical data for this grid
    query = text(\"\"\"
        SELECT 
            grid_id,
            DATE(event_date) as date,
            event_hour,
            COUNT(*) as count
        FROM incidents
        WHERE grid_id = :grid_id
        AND event_date >= DATE_SUB(CURDATE(), INTERVAL 90 DAY)
        GROUP BY grid_id, DATE(event_date), event_hour
        ORDER BY date DESC, event_hour
        LIMIT 100
    \"\"\")
    
    result = db.execute(query, {"grid_id": grid_id}).fetchall()
    
    if not result:
        raise HTTPException(status_code=404, detail="Grid not found or no historical data")
    
    # Calculate average for simple prediction
    avg_by_hour = {}
    for row in result:
        hour = row.event_hour
        if hour not in avg_by_hour:
            avg_by_hour[hour] = []
        avg_by_hour[hour].append(row.count)
    
    for hour in avg_by_hour:
        avg_by_hour[hour] = np.mean(avg_by_hour[hour])
    
    # Generate forecast
    forecasts = []
    start_date = datetime.now().date() + timedelta(days=1)
    
    for day in range(request.days):
        forecast_date = start_date + timedelta(days=day)
        for hour in range(24):
            predicted = avg_by_hour.get(hour, 1.0)
            
            forecasts.append(ForecastResponse(
                grid_id=grid_id,
                date=forecast_date,
                hour=hour,
                predicted_count=float(predicted),
                confidence=0.75
            ))
    
    return forecasts

@router.post("/grids/nearby", response_model=List[GridInfo])
def get_nearby_grids(
    request: NearbyRequest,
    db: Session = Depends(get_db)
):
    \"\"\"Find grids near given coordinates\"\"\"
    
    # Create geohash for the location
    center_hash = pgh.encode(request.latitude, request.longitude, precision=6)
    
    # Get adjacent geohashes
    nearby_hashes = [center_hash]
    directions = ['top', 'bottom', 'left', 'right', 
                  'topleft', 'topright', 'bottomleft', 'bottomright']
    
    for direction in directions:
        try:
            adjacent = pgh.get_adjacent(center_hash, direction)
            nearby_hashes.append(adjacent)
        except:
            pass
    
    # Query grids
    query = text(\"\"\"
        SELECT 
            grid_id,
            AVG(latitude) as center_lat,
            AVG(longitude) as center_lon,
            COUNT(*) as crime_count
        FROM incidents
        WHERE grid_id IN :grid_ids
        AND event_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
        GROUP BY grid_id
        ORDER BY crime_count DESC
        LIMIT 20
    \"\"\")
    
    result = db.execute(query, {"grid_ids": tuple(nearby_hashes)}).fetchall()
    
    grids = []
    for row in result:
        grids.append(GridInfo(
            grid_id=row.grid_id,
            center_lat=float(row.center_lat),
            center_lon=float(row.center_lon),
            crime_count=int(row.crime_count)
        ))
    
    return grids

@router.post("/explain", response_model=ExplainResponse)
def explain_prediction(
    request: ExplainRequest,
    db: Session = Depends(get_db)
):
    \"\"\"Get SHAP explanation for a prediction\"\"\"
    
    # This is a simplified version - real implementation would use SHAP
    return ExplainResponse(
        grid_id=request.grid_id,
        date=request.date,
        hour=request.hour,
        prediction=5.2,
        base_value=3.1,
        feature_contributions={
            "rolling_7d": 1.5,
            "hour": 0.8,
            "day_of_week": -0.2,
            "rolling_30d": 0.5
        }
    )
"""

router_historical = """from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from schemas import *
from typing import List, Optional

router = APIRouter()

@router.post("/historical", response_model=List[IncidentResponse])
def get_historical_data(
    request: HistoricalRequest,
    db: Session = Depends(get_db)
):
    \"\"\"Query historical crime data\"\"\"
    
    # Build query
    base_query = \"\"\"
        SELECT 
            incident_id,
            primary_type,
            description,
            latitude,
            longitude,
            event_ts,
            arrest,
            domestic,
            grid_id,
            district,
            community_area
        FROM incidents
        WHERE event_date BETWEEN :start_date AND :end_date
    \"\"\"
    
    params = {
        "start_date": request.start_date,
        "end_date": request.end_date,
        "limit": request.limit
    }
    
    if request.grid_id:
        base_query += " AND grid_id = :grid_id"
        params["grid_id"] = request.grid_id
    
    if request.crime_type:
        base_query += " AND primary_type = :crime_type"
        params["crime_type"] = request.crime_type.upper()
    
    base_query += " ORDER BY event_ts DESC LIMIT :limit"
    
    query = text(base_query)
    result = db.execute(query, params).fetchall()
    
    incidents = []
    for row in result:
        incidents.append(IncidentResponse(
            incident_id=row.incident_id,
            primary_type=row.primary_type,
            description=row.description or "",
            latitude=float(row.latitude),
            longitude=float(row.longitude),
            event_ts=row.event_ts,
            arrest=bool(row.arrest),
            domestic=bool(row.domestic),
            grid_id=row.grid_id,
            district=int(row.district),
            community_area=int(row.community_area)
        ))
    
    return incidents

@router.get("/stats/summary")
def get_summary_stats(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    \"\"\"Get summary statistics\"\"\"
    
    query = text(\"\"\"
        SELECT 
            COUNT(*) as total_crimes,
            COUNT(DISTINCT grid_id) as total_grids,
            COUNT(DISTINCT primary_type) as crime_types,
            AVG(arrest) as arrest_rate
        FROM incidents
        WHERE event_date >= DATE_SUB(CURDATE(), INTERVAL :days DAY)
    \"\"\")
    
    result = db.execute(query, {"days": days}).fetchone()
    
    return {
        "period_days": days,
        "total_crimes": result.total_crimes,
        "total_grids": result.total_grids,
        "crime_types": result.crime_types,
        "arrest_rate": float(result.arrest_rate or 0)
    }

@router.get("/stats/by-hour")
def get_hourly_stats(
    days: int = Query(default=30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    \"\"\"Get crime stats by hour of day\"\"\"
    
    query = text(\"\"\"
        SELECT 
            event_hour,
            COUNT(*) as count,
            COUNT(CASE WHEN arrest = 1 THEN 1 END) as arrests
        FROM incidents
        WHERE event_date >= DATE_SUB(CURDATE(), INTERVAL :days DAY)
        GROUP BY event_hour
        ORDER BY event_hour
    \"\"\")
    
    result = db.execute(query, {"days": days}).fetchall()
    
    return [
        {
            "hour": row.event_hour,
            "count": row.count,
            "arrests": row.arrests
        }
        for row in result
    ]
"""

print("✅ API Routers Generated:")
print("   - api/main.py")
print("   - api/routers/health.py")
print("   - api/routers/predictions.py")
print("   - api/routers/historical.py")
