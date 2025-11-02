
# Generate ML Model Training Files

model_train = """#!/usr/bin/env python3
\"\"\"
Train machine learning models for crime prediction
\"\"\"
import pandas as pd
import numpy as np
from pathlib import Path
import pickle
from datetime import datetime
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import lightgbm as lgb
import xgboost as xgb
import argparse

DATA_DIR = Path(__file__).parent.parent / "data"
MODEL_DIR = Path(__file__).parent / "saved"
MODEL_DIR.mkdir(exist_ok=True)

def load_and_prepare_data():
    \"\"\"Load and prepare data for training\"\"\"
    print("Loading feature-engineered data...")
    
    input_file = DATA_DIR / "chicago_crimes_features.csv"
    df = pd.read_csv(input_file, parse_dates=['event_ts', 'event_date'])
    
    # Sort by time
    df = df.sort_values('event_ts')
    
    # Create target: crime count in next time period
    # Group by grid and hour
    df_agg = df.groupby(['grid_id', 'event_date', 'event_hour']).size().reset_index(name='crime_count')
    
    # Add features
    feature_df = df.groupby(['grid_id', 'event_date', 'event_hour']).agg({
        'rolling_1d': 'first',
        'rolling_7d': 'first',
        'rolling_30d': 'first',
        'day_of_week': 'first',
        'is_weekend': 'first',
        'month': 'first',
        'district': 'first',
        'total_crimes': 'first'
    }).reset_index()
    
    # Merge
    df_ml = df_agg.merge(feature_df, on=['grid_id', 'event_date', 'event_hour'], how='left')
    
    # Remove NaNs
    df_ml = df_ml.dropna()
    
    print(f"ML Dataset shape: {df_ml.shape}")
    print(f"Date range: {df_ml['event_date'].min()} to {df_ml['event_date'].max()}")
    
    return df_ml

def prepare_features_target(df):
    \"\"\"Separate features and target\"\"\"
    
    feature_cols = [
        'rolling_1d', 'rolling_7d', 'rolling_30d',
        'event_hour', 'day_of_week', 'is_weekend',
        'month', 'district', 'total_crimes'
    ]
    
    X = df[feature_cols]
    y = df['crime_count']
    
    return X, y, feature_cols

def train_lightgbm(X_train, y_train, X_val, y_val):
    \"\"\"Train LightGBM model\"\"\"
    print("\\nTraining LightGBM...")
    
    train_data = lgb.Dataset(X_train, label=y_train)
    val_data = lgb.Dataset(X_val, label=y_val, reference=train_data)
    
    params = {
        'objective': 'regression',
        'metric': 'rmse',
        'boosting_type': 'gbdt',
        'num_leaves': 31,
        'learning_rate': 0.05,
        'feature_fraction': 0.9,
        'bagging_fraction': 0.8,
        'bagging_freq': 5,
        'verbose': -1
    }
    
    model = lgb.train(
        params,
        train_data,
        num_boost_round=1000,
        valid_sets=[train_data, val_data],
        callbacks=[
            lgb.early_stopping(stopping_rounds=50),
            lgb.log_evaluation(period=100)
        ]
    )
    
    return model

def train_xgboost(X_train, y_train, X_val, y_val):
    \"\"\"Train XGBoost model\"\"\"
    print("\\nTraining XGBoost...")
    
    params = {
        'objective': 'reg:squarederror',
        'eval_metric': 'rmse',
        'max_depth': 6,
        'learning_rate': 0.05,
        'subsample': 0.8,
        'colsample_bytree': 0.8,
        'verbosity': 1
    }
    
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dval = xgb.DMatrix(X_val, label=y_val)
    
    model = xgb.train(
        params,
        dtrain,
        num_boost_round=1000,
        evals=[(dtrain, 'train'), (dval, 'val')],
        early_stopping_rounds=50,
        verbose_eval=100
    )
    
    return model

def evaluate_model(model, X_test, y_test, model_type='lightgbm'):
    \"\"\"Evaluate model performance\"\"\"
    
    if model_type == 'lightgbm':
        y_pred = model.predict(X_test, num_iteration=model.best_iteration)
    elif model_type == 'xgboost':
        dtest = xgb.DMatrix(X_test)
        y_pred = model.predict(dtest)
    else:
        y_pred = model.predict(X_test)
    
    # Calculate metrics
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    
    print(f"\\n{'='*50}")
    print(f"Model Evaluation - {model_type.upper()}")
    print(f"{'='*50}")
    print(f"RMSE: {rmse:.4f}")
    print(f"MAE:  {mae:.4f}")
    print(f"R2:   {r2:.4f}")
    print(f"{'='*50}\\n")
    
    return {
        'rmse': rmse,
        'mae': mae,
        'r2': r2,
        'predictions': y_pred
    }

def save_model(model, model_type, feature_cols, metrics):
    \"\"\"Save trained model\"\"\"
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{model_type}_crime_predictor_{timestamp}.pkl"
    filepath = MODEL_DIR / filename
    
    model_package = {
        'model': model,
        'model_type': model_type,
        'feature_cols': feature_cols,
        'metrics': metrics,
        'timestamp': timestamp
    }
    
    with open(filepath, 'wb') as f:
        pickle.dump(model_package, f)
    
    print(f"✅ Model saved to {filepath}")
    
    # Also save as latest
    latest_path = MODEL_DIR / f"{model_type}_crime_predictor.pkl"
    with open(latest_path, 'wb') as f:
        pickle.dump(model_package, f)
    
    print(f"✅ Model saved as {latest_path}")

def main(model_type='lightgbm'):
    \"\"\"Main training pipeline\"\"\"
    print("="*70)
    print("CHICAGO CRIME PREDICTION MODEL TRAINING")
    print("="*70)
    
    # Load data
    df = load_and_prepare_data()
    
    # Prepare features and target
    X, y, feature_cols = prepare_features_target(df)
    
    # Time-based split (80-10-10)
    n = len(X)
    train_end = int(n * 0.8)
    val_end = int(n * 0.9)
    
    X_train, y_train = X[:train_end], y[:train_end]
    X_val, y_val = X[train_end:val_end], y[train_end:val_end]
    X_test, y_test = X[val_end:], y[val_end:]
    
    print(f"\\nTrain set: {len(X_train)} samples")
    print(f"Val set:   {len(X_val)} samples")
    print(f"Test set:  {len(X_test)} samples")
    
    # Train model
    if model_type == 'lightgbm':
        model = train_lightgbm(X_train, y_train, X_val, y_val)
    elif model_type == 'xgboost':
        model = train_xgboost(X_train, y_train, X_val, y_val)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Evaluate
    metrics = evaluate_model(model, X_test, y_test, model_type)
    
    # Save model
    save_model(model, model_type, feature_cols, metrics)
    
    print("\\n✅ Training complete!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Train crime prediction model')
    parser.add_argument('--model', type=str, default='lightgbm',
                       choices=['lightgbm', 'xgboost'],
                       help='Model type to train')
    
    args = parser.parse_args()
    main(args.model)
"""

model_explainer = """#!/usr/bin/env python3
\"\"\"
Model explainability using SHAP
\"\"\"
import pandas as pd
import numpy as np
import pickle
import shap
from pathlib import Path
import matplotlib.pyplot as plt

MODEL_DIR = Path(__file__).parent / "saved"

def load_model(model_type='lightgbm'):
    \"\"\"Load trained model\"\"\"
    model_file = MODEL_DIR / f"{model_type}_crime_predictor.pkl"
    
    if not model_file.exists():
        raise FileNotFoundError(f"Model not found: {model_file}")
    
    with open(model_file, 'rb') as f:
        model_package = pickle.load(f)
    
    return model_package

def explain_predictions(model_package, X_sample):
    \"\"\"Generate SHAP explanations\"\"\"
    
    model = model_package['model']
    model_type = model_package['model_type']
    
    print("Generating SHAP explanations...")
    
    if model_type == 'lightgbm':
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
    elif model_type == 'xgboost':
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_sample)
    else:
        explainer = shap.Explainer(model, X_sample)
        shap_values = explainer(X_sample)
    
    return explainer, shap_values

def plot_shap_summary(shap_values, X_sample, feature_names):
    \"\"\"Plot SHAP summary\"\"\"
    shap.summary_plot(shap_values, X_sample, feature_names=feature_names)

def plot_shap_waterfall(explainer, shap_values, X_sample, idx=0):
    \"\"\"Plot SHAP waterfall for single prediction\"\"\"
    shap.waterfall_plot(shap.Explanation(
        values=shap_values[idx],
        base_values=explainer.expected_value,
        data=X_sample.iloc[idx],
        feature_names=X_sample.columns.tolist()
    ))

def get_feature_importance(shap_values, feature_names):
    \"\"\"Get feature importance from SHAP values\"\"\"
    
    # Mean absolute SHAP values
    importance = np.abs(shap_values).mean(axis=0)
    
    importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importance
    }).sort_values('importance', ascending=False)
    
    return importance_df

if __name__ == "__main__":
    print("SHAP Model Explainability")
    print("="*50)
    
    # Load model
    model_package = load_model('lightgbm')
    print(f"Model loaded: {model_package['model_type']}")
    print(f"Metrics: {model_package['metrics']}")
    
    # Load sample data
    from train_model import load_and_prepare_data, prepare_features_target
    df = load_and_prepare_data()
    X, y, feature_cols = prepare_features_target(df)
    
    # Take sample
    X_sample = X.sample(n=100, random_state=42)
    
    # Generate explanations
    explainer, shap_values = explain_predictions(model_package, X_sample)
    
    # Feature importance
    importance = get_feature_importance(shap_values, feature_cols)
    print("\\nFeature Importance (SHAP):")
    print(importance)
    
    # Plot summary
    plot_shap_summary(shap_values, X_sample, feature_cols)
"""

print("✅ ML Model Training Files Generated:")
print("   - models/train_model.py")
print("   - models/explainer.py")
