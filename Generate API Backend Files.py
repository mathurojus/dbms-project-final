
# Generate API Backend Files

api_requirements = """fastapi==0.115.0
uvicorn[standard]==0.32.0
sqlalchemy==2.0.35
pymysql==1.1.1
python-dotenv==1.0.1
pydantic==2.9.2
pydantic-settings==2.5.2
python-multipart==0.0.12
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
pandas==2.2.3
numpy==2.1.2
lightgbm==4.5.0
xgboost==2.1.1
shap==0.46.0
scikit-learn==1.5.2
pygeohash==1.2.0
"""

api_dockerfile = """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    g++ \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
"""

api_config = """from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    # Database
    mysql_host: str = "localhost"
    mysql_port: int = 3306
    mysql_database: str = "chicago_crime"
    mysql_user: str = "root"
    mysql_password: str = "password"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    secret_key: str = "your-secret-key-change-this"
    
    # Models
    model_path: str = "../models/saved/"
    model_name: str = "lightgbm_crime_predictor.pkl"
    
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def database_url(self) -> str:
        return f"mysql+pymysql://{self.mysql_user}:{self.mysql_password}@{self.mysql_host}:{self.mysql_port}/{self.mysql_database}"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
"""

api_database = """from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import get_settings

settings = get_settings()

# Create engine
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=20
)

# Create session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

api_models = """from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Date, SmallInteger, TIMESTAMP, Index, Text
from sqlalchemy.sql import func
from database import Base

class Incident(Base):
    __tablename__ = "incidents"
    
    # Primary Key
    incident_id = Column(Integer, primary_key=True, index=True)
    
    # Crime Information
    case_number = Column(String(50))
    iucr = Column(String(10), index=True)
    primary_type = Column(String(100), index=True)
    description = Column(Text)
    
    # Location
    district = Column(Integer, index=True)
    community_area = Column(Integer)
    beat = Column(Integer)
    grid_id = Column(String(32), index=True)
    geohash6 = Column(String(12), index=True)
    geohash8 = Column(String(12))
    latitude = Column(Float)
    longitude = Column(Float)
    
    # Temporal
    event_ts = Column(DateTime, index=True)
    event_date = Column(Date, index=True)
    event_hour = Column(SmallInteger)
    day_of_week = Column(SmallInteger)
    is_weekend = Column(SmallInteger)
    
    # Flags
    arrest = Column(Boolean, default=False)
    domestic = Column(Boolean, default=False)
    
    # Metadata
    reported_year = Column(SmallInteger)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    # Indexes
    __table_args__ = (
        Index('ix_grid_date_hour', 'grid_id', 'event_date', 'event_hour'),
        Index('ix_geo', 'geohash6', 'geohash8'),
        Index('ix_type_date', 'primary_type', 'event_date'),
    )

class GridAggregate(Base):
    __tablename__ = "grid_aggregates"
    
    grid_id = Column(String(32), primary_key=True)
    date = Column(Date, primary_key=True)
    hour = Column(SmallInteger, primary_key=True)
    count = Column(Integer, default=0)
    rolling_1d = Column(Integer, default=0)
    rolling_7d = Column(Integer, default=0)
    rolling_30d = Column(Integer, default=0)
    
    __table_args__ = (
        Index('ix_grid_agg_date', 'grid_id', 'date'),
    )

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    grid_id = Column(String(32), index=True)
    prediction_date = Column(Date, index=True)
    prediction_hour = Column(SmallInteger)
    predicted_count = Column(Float)
    confidence = Column(Float)
    model_version = Column(String(50))
    created_at = Column(TIMESTAMP, server_default=func.now())
"""

api_schemas = """from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional, List

class IncidentBase(BaseModel):
    incident_id: int
    primary_type: str
    description: Optional[str] = None
    latitude: float
    longitude: float
    event_ts: datetime
    arrest: bool
    domestic: bool

class IncidentResponse(IncidentBase):
    grid_id: str
    district: int
    community_area: int
    
    class Config:
        from_attributes = True

class ForecastRequest(BaseModel):
    grid_id: str
    days: int = Field(default=7, ge=1, le=30)

class ForecastResponse(BaseModel):
    grid_id: str
    date: date
    hour: int
    predicted_count: float
    confidence: float

class NearbyRequest(BaseModel):
    latitude: float = Field(..., ge=41.6, le=42.1)
    longitude: float = Field(..., ge=-87.9, le=-87.5)
    radius_km: float = Field(default=1.0, ge=0.1, le=10.0)

class GridInfo(BaseModel):
    grid_id: str
    center_lat: float
    center_lon: float
    crime_count: int
    distance_km: Optional[float] = None

class HistoricalRequest(BaseModel):
    start_date: date
    end_date: date
    grid_id: Optional[str] = None
    crime_type: Optional[str] = None
    limit: int = Field(default=1000, le=10000)

class ExplainRequest(BaseModel):
    grid_id: str
    date: date
    hour: int

class ExplainResponse(BaseModel):
    grid_id: str
    date: date
    hour: int
    prediction: float
    base_value: float
    feature_contributions: dict

class HealthResponse(BaseModel):
    status: str
    database: str
    model_loaded: bool
    version: str
"""

print("✅ API Backend Core Files Generated:")
print("   - api/requirements.txt")
print("   - api/Dockerfile")
print("   - api/config.py")
print("   - api/database.py")
print("   - api/models.py")
print("   - api/schemas.py")
