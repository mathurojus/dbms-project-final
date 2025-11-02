
# Continue generating backend files

# ETL Files
etl_download = """#!/usr/bin/env python3
\"\"\"
Download Chicago Crime Dataset from Kaggle or Chicago Data Portal
\"\"\"
import os
import requests
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# Chicago Data Portal API endpoint
CHICAGO_API_URL = "https://data.cityofchicago.org/resource/ijzp-q8t2.json"
OUTPUT_FILE = DATA_DIR / "chicago_crimes_raw.csv"

def download_from_chicago_portal(limit=100000):
    \"\"\"Download data from Chicago Data Portal API\"\"\"
    print(f"Downloading data from Chicago Data Portal...")
    print(f"API: {CHICAGO_API_URL}")
    
    all_data = []
    offset = 0
    batch_size = 50000
    
    while offset < limit:
        params = {
            "$limit": batch_size,
            "$offset": offset,
            "$order": "date DESC"
        }
        
        print(f"Fetching records {offset} to {offset + batch_size}...")
        response = requests.get(CHICAGO_API_URL, params=params)
        
        if response.status_code == 200:
            batch_data = response.json()
            if not batch_data:
                break
            all_data.extend(batch_data)
            offset += batch_size
        else:
            print(f"Error: {response.status_code}")
            break
    
    print(f"Downloaded {len(all_data)} records")
    
    # Convert to DataFrame
    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to {OUTPUT_FILE}")
    print(f"Shape: {df.shape}")
    print(f"\\nColumns: {list(df.columns)}")
    
    return df

def download_from_kaggle():
    \"\"\"
    Download from Kaggle (requires kaggle API setup)
    Requires: pip install kaggle
    And kaggle.json in ~/.kaggle/
    \"\"\"
    try:
        import kaggle
        print("Downloading from Kaggle...")
        kaggle.api.dataset_download_files(
            'currie32/crimes-in-chicago',
            path=str(DATA_DIR),
            unzip=True
        )
        print(f"Downloaded to {DATA_DIR}")
    except Exception as e:
        print(f"Kaggle download failed: {e}")
        print("Falling back to Chicago Data Portal...")
        return download_from_chicago_portal()

if __name__ == "__main__":
    print("=" * 70)
    print("CHICAGO CRIME DATA DOWNLOADER")
    print("=" * 70)
    
    # Try Kaggle first, fallback to API
    choice = input("Download from (1) Kaggle or (2) Chicago Portal? [1/2]: ")
    
    if choice == "1":
        download_from_kaggle()
    else:
        limit = int(input("How many records to download? [default 100000]: ") or 100000)
        download_from_chicago_portal(limit)
    
    print("\\n✅ Download complete!")
"""

etl_clean = """#!/usr/bin/env python3
\"\"\"
Clean and preprocess Chicago crime data
\"\"\"
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(__file__).parent.parent / "data"
INPUT_FILE = DATA_DIR / "chicago_crimes_raw.csv"
OUTPUT_FILE = DATA_DIR / "chicago_crimes_cleaned.csv"

def clean_data(df):
    \"\"\"Clean the raw crime data\"\"\"
    print(f"Initial shape: {df.shape}")
    
    # Rename columns to standard format
    column_mapping = {
        'id': 'incident_id',
        'case_number': 'case_number',
        'date': 'event_ts',
        'block': 'block',
        'iucr': 'iucr',
        'primary_type': 'primary_type',
        'description': 'description',
        'location_description': 'location_description',
        'arrest': 'arrest',
        'domestic': 'domestic',
        'beat': 'beat',
        'district': 'district',
        'ward': 'ward',
        'community_area': 'community_area',
        'fbi_code': 'fbi_code',
        'x_coordinate': 'x_coordinate',
        'y_coordinate': 'y_coordinate',
        'year': 'reported_year',
        'latitude': 'latitude',
        'longitude': 'longitude',
        'location': 'location'
    }
    
    df = df.rename(columns=column_mapping)
    
    # Drop rows with missing critical fields
    print("Removing rows with missing coordinates...")
    df = df.dropna(subset=['latitude', 'longitude'])
    
    # Drop rows with invalid coordinates
    df = df[(df['latitude'] != 0) & (df['longitude'] != 0)]
    df = df[(df['latitude'].between(41.6, 42.1)) & 
            (df['longitude'].between(-87.9, -87.5))]
    
    # Parse datetime
    print("Parsing timestamps...")
    df['event_ts'] = pd.to_datetime(df['event_ts'], errors='coerce')
    df = df.dropna(subset=['event_ts'])
    
    # Extract date components
    df['event_date'] = df['event_ts'].dt.date
    df['event_hour'] = df['event_ts'].dt.hour
    df['day_of_week'] = df['event_ts'].dt.dayofweek
    df['month'] = df['event_ts'].dt.month
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    
    # Clean boolean fields
    df['arrest'] = df['arrest'].fillna(False).astype(bool)
    df['domestic'] = df['domestic'].fillna(False).astype(bool)
    
    # Fill missing categorical fields
    df['district'] = df['district'].fillna(0).astype(int)
    df['community_area'] = df['community_area'].fillna(0).astype(int)
    df['beat'] = df['beat'].fillna(0).astype(int)
    
    # Clean text fields
    df['primary_type'] = df['primary_type'].fillna('UNKNOWN').str.upper()
    df['description'] = df['description'].fillna('').str.upper()
    
    print(f"Final shape: {df.shape}")
    print(f"Date range: {df['event_ts'].min()} to {df['event_ts'].max()}")
    print(f"\\nCrime types: {df['primary_type'].nunique()}")
    print(df['primary_type'].value_counts().head(10))
    
    return df

if __name__ == "__main__":
    print("=" * 70)
    print("CHICAGO CRIME DATA CLEANING")
    print("=" * 70)
    
    # Load raw data
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE, low_memory=False)
    
    # Clean data
    df_cleaned = clean_data(df)
    
    # Save cleaned data
    df_cleaned.to_csv(OUTPUT_FILE, index=False)
    print(f"\\n✅ Cleaned data saved to {OUTPUT_FILE}")
    print(f"Shape: {df_cleaned.shape}")
"""

etl_features = """#!/usr/bin/env python3
\"\"\"
Feature engineering for crime prediction
\"\"\"
import pandas as pd
import numpy as np
import pygeohash as pgh
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
INPUT_FILE = DATA_DIR / "chicago_crimes_cleaned.csv"
OUTPUT_FILE = DATA_DIR / "chicago_crimes_features.csv"

def create_grid_id(lat, lon, precision=6):
    \"\"\"Create grid ID from lat/lon using geohash\"\"\"
    return pgh.encode(lat, lon, precision=precision)

def add_spatial_features(df):
    \"\"\"Add geohash-based spatial features\"\"\"
    print("Creating spatial features...")
    
    # Create geohashes at different precisions
    df['geohash6'] = df.apply(
        lambda x: create_grid_id(x['latitude'], x['longitude'], 6), 
        axis=1
    )
    df['geohash8'] = df.apply(
        lambda x: create_grid_id(x['latitude'], x['longitude'], 8), 
        axis=1
    )
    
    # Use geohash6 as primary grid_id
    df['grid_id'] = df['geohash6']
    
    print(f"Created {df['grid_id'].nunique()} unique grids")
    return df

def add_temporal_features(df):
    \"\"\"Add time-based features\"\"\"
    print("Creating temporal features...")
    
    # Already have: event_hour, day_of_week, month, is_weekend
    
    # Add season
    df['season'] = df['month'].apply(lambda m: 
        'Winter' if m in [12, 1, 2] else
        'Spring' if m in [3, 4, 5] else
        'Summer' if m in [6, 7, 8] else 'Fall'
    )
    
    # Is holiday (simplified)
    df['is_holiday'] = df['event_date'].apply(lambda d:
        d.month == 12 and d.day == 25 or  # Christmas
        d.month == 1 and d.day == 1 or     # New Year
        d.month == 7 and d.day == 4        # Independence Day
    ).astype(int)
    
    # Time of day categories
    df['time_of_day'] = df['event_hour'].apply(lambda h:
        'Night' if h < 6 else
        'Morning' if h < 12 else
        'Afternoon' if h < 18 else 'Evening'
    )
    
    return df

def add_lag_features(df):
    \"\"\"Add rolling count features\"\"\"
    print("Creating lag features (this may take time)...")
    
    # Sort by grid and time
    df = df.sort_values(['grid_id', 'event_ts'])
    
    # Group by grid_id and date
    daily_counts = df.groupby(['grid_id', 'event_date']).size().reset_index(name='daily_count')
    
    # Calculate rolling counts
    daily_counts = daily_counts.sort_values(['grid_id', 'event_date'])
    
    for window in [1, 7, 30]:
        daily_counts[f'rolling_{window}d'] = daily_counts.groupby('grid_id')['daily_count'].transform(
            lambda x: x.rolling(window=window, min_periods=1).sum()
        )
    
    # Merge back to main dataframe
    df = df.merge(daily_counts[['grid_id', 'event_date', 'rolling_1d', 'rolling_7d', 'rolling_30d']], 
                  on=['grid_id', 'event_date'], 
                  how='left')
    
    # Fill NaN with 0
    df[['rolling_1d', 'rolling_7d', 'rolling_30d']] = df[['rolling_1d', 'rolling_7d', 'rolling_30d']].fillna(0)
    
    return df

def add_crime_type_features(df):
    \"\"\"Add crime type encoding and frequency features\"\"\"
    print("Creating crime type features...")
    
    # Crime type frequency per grid
    crime_freq = df.groupby(['grid_id', 'primary_type']).size().reset_index(name='type_freq')
    top_crimes = crime_freq.groupby('grid_id')['type_freq'].sum().reset_index(name='total_crimes')
    
    df = df.merge(top_crimes, on='grid_id', how='left')
    df['total_crimes'] = df['total_crimes'].fillna(0)
    
    return df

if __name__ == "__main__":
    print("=" * 70)
    print("CHICAGO CRIME FEATURE ENGINEERING")
    print("=" * 70)
    
    # Load cleaned data
    print(f"Loading data from {INPUT_FILE}...")
    df = pd.read_csv(INPUT_FILE, parse_dates=['event_ts', 'event_date'])
    
    # Add features
    df = add_spatial_features(df)
    df = add_temporal_features(df)
    df = add_lag_features(df)
    df = add_crime_type_features(df)
    
    # Save feature-engineered data
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"\\n✅ Feature-engineered data saved to {OUTPUT_FILE}")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
"""

print("\n✅ ETL Pipeline Files Generated:")
print("   - etl/download_data.py")
print("   - etl/clean_data.py") 
print("   - etl/feature_engineering.py")
