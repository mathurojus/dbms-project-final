
import os
import json

# Create the complete project structure
project_structure = """
chicago-crime-forecast/
├── README.md
├── docker-compose.yml
├── .env.example
├── data/
│   └── README.md
├── etl/
│   ├── __init__.py
│   ├── download_data.py
│   ├── clean_data.py
│   ├── feature_engineering.py
│   └── load_to_mysql.py
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   └── routers/
│       ├── __init__.py
│       ├── predictions.py
│       ├── historical.py
│       └── health.py
├── models/
│   ├── __init__.py
│   ├── train_model.py
│   ├── model_utils.py
│   └── explainer.py
├── frontend/
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── index.html
│   ├── Dockerfile
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/
│       │   ├── Sidebar.tsx
│       │   ├── Header.tsx
│       │   ├── HeatMap.tsx
│       │   ├── TimeSeriesChart.tsx
│       │   ├── StatsCard.tsx
│       │   └── ExplanationModal.tsx
│       ├── pages/
│       │   ├── Dashboard.tsx
│       │   ├── ZoneDetail.tsx
│       │   ├── PatrolPlanner.tsx
│       │   └── Analytics.tsx
│       ├── services/
│       │   └── api.ts
│       └── types/
│           └── index.ts
└── infra/
    ├── mysql/
    │   └── init.sql
    └── nginx/
        └── nginx.conf
"""

print("=" * 80)
print("CHICAGO CRIMES PREDICTIVE ANALYTICS DASHBOARD - PROJECT STRUCTURE")
print("=" * 80)
print(project_structure)
print("\n" + "=" * 80)
print("Generating all project files...")
print("=" * 80 + "\n")

# Create a dictionary to store all files
files = {}

# 1. Root level files
files['README.md'] = """# Chicago Crimes Predictive Analytics Dashboard

**A complete full-stack data-driven system for Chicago crime analysis and prediction**

## 🎯 Overview

This project combines **MySQL**, **Machine Learning**, and a **React-based dashboard** to predict crime hotspots and time windows for future crimes in Chicago.

### Tech Stack

- **Database**: MySQL 8.0 with spatial indexing
- **Backend**: FastAPI + SQLAlchemy
- **ML Models**: LightGBM, XGBoost, LSTM
- **Frontend**: React + TypeScript + Tailwind CSS + Mapbox GL
- **Deployment**: Docker + Docker Compose

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- 8GB+ RAM recommended
- Mapbox API Token (free tier works)

### Installation

1. Clone the repository:
```bash
git clone <repo-url>
cd chicago-crime-forecast
```

2. Copy environment file and configure:
```bash
cp .env.example .env
# Edit .env with your configurations
```

3. Start all services:
```bash
docker-compose up --build
```

4. Access the applications:
- Frontend Dashboard: http://localhost:3000
- API Documentation: http://localhost:8000/docs
- MySQL Database: localhost:3306

## 📊 Data Pipeline

### 1. Download Dataset

```bash
python etl/download_data.py
```

### 2. Clean & Transform

```bash
python etl/clean_data.py
python etl/feature_engineering.py
```

### 3. Load to MySQL

```bash
python etl/load_to_mysql.py
```

## 🤖 Train ML Models

```bash
python models/train_model.py --model lightgbm --epochs 100
```

## 📁 Project Structure

See full structure in the codebase. Key directories:
- `/etl`: Data extraction, transformation, and loading
- `/api`: FastAPI backend with prediction endpoints
- `/models`: ML training and inference
- `/frontend`: React dashboard with Mapbox visualizations

## 🔧 Configuration

Edit `.env` file:

```
# Database
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=chicago_crime
MYSQL_USER=crime_user
MYSQL_PASSWORD=your_password

# API
API_HOST=0.0.0.0
API_PORT=8000

# Mapbox
VITE_MAPBOX_TOKEN=your_mapbox_token

# ML Models
MODEL_PATH=./models/saved/
```

## 🌐 API Endpoints

- `GET /health` - Health check
- `GET /grids/{grid_id}/forecast` - Get crime forecast for grid
- `GET /grids/nearby` - Find grids near coordinates
- `GET /historical` - Query historical crime data
- `GET /explain` - Get SHAP explanations

## 📊 Features

✅ MySQL database with spatial indexing and partitioning  
✅ ETL pipeline for Chicago crime data  
✅ Multiple ML models (LightGBM, XGBoost, LSTM)  
✅ SHAP-based model explainability  
✅ FastAPI backend with prediction endpoints  
✅ React dashboard with Mapbox heatmaps  
✅ Time-series visualizations  
✅ Patrol planning recommendations  
✅ Dark/light theme support  
✅ Docker deployment  

## 🔒 Privacy & Ethics

- All data is aggregated to block-level
- Predictions are probabilistic, not deterministic
- Model decisions are explainable via SHAP
- API access is logged for auditability

## 📝 License

MIT License

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 📧 Contact

For questions, open an issue on GitHub.
"""

files['.env.example'] = """# Database Configuration
MYSQL_HOST=mysql
MYSQL_PORT=3306
MYSQL_DATABASE=chicago_crime
MYSQL_USER=crime_user
MYSQL_PASSWORD=change_this_password
MYSQL_ROOT_PASSWORD=change_root_password

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
SECRET_KEY=change_this_secret_key_to_something_secure

# Frontend Configuration
VITE_API_URL=http://localhost:8000
VITE_MAPBOX_TOKEN=your_mapbox_token_here

# ML Model Configuration
MODEL_PATH=./models/saved/
MODEL_NAME=lightgbm_crime_predictor.pkl
"""

files['docker-compose.yml'] = """version: '3.8'

services:
  mysql:
    image: mysql:8.0
    container_name: chicago_crime_mysql
    environment:
      MYSQL_ROOT_PASSWORD: ${MYSQL_ROOT_PASSWORD}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./infra/mysql/init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - crime_network
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    container_name: chicago_crime_api
    environment:
      MYSQL_HOST: mysql
      MYSQL_PORT: ${MYSQL_PORT}
      MYSQL_DATABASE: ${MYSQL_DATABASE}
      MYSQL_USER: ${MYSQL_USER}
      MYSQL_PASSWORD: ${MYSQL_PASSWORD}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "8000:8000"
    volumes:
      - ./api:/app
      - ./models:/models
    depends_on:
      mysql:
        condition: service_healthy
    networks:
      - crime_network
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: chicago_crime_frontend
    environment:
      VITE_API_URL: ${VITE_API_URL}
      VITE_MAPBOX_TOKEN: ${VITE_MAPBOX_TOKEN}
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    depends_on:
      - api
    networks:
      - crime_network
    command: npm run dev -- --host

volumes:
  mysql_data:

networks:
  crime_network:
    driver: bridge
"""

print("✅ Root configuration files generated")

# Store files in a list to save later
file_list = [
    ('README.md', files['README.md']),
    ('.env.example', files['.env.example']),
    ('docker-compose.yml', files['docker-compose.yml'])
]

# Display summary
for filename, _ in file_list:
    print(f"   - {filename}")
