"""
Simple Flask API for Stock Forecasting
Deploy locally or on cloud platforms
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import pandas as pd
import os
import sys

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from model import load_model
from data import load_data, prepare_features

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

MODEL_PATH = 'models/xgb_model.joblib'

# Simple HTML template for homepage
HOME_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Tata Steel Stock Forecast API</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
        h1 { color: #2c3e50; }
        .endpoint { background: #ecf0f1; padding: 15px; margin: 10px 0; border-radius: 5px; }
        code { background: #34495e; color: #ecf0f1; padding: 2px 6px; border-radius: 3px; }
        .method { display: inline-block; padding: 3px 8px; border-radius: 3px; font-weight: bold; }
        .get { background: #3498db; color: white; }
        .post { background: #2ecc71; color: white; }
    </style>
</head>
<body>
    <h1>📈 Tata Steel Stock Forecast API</h1>
    <p>Machine Learning API for stock price predictions using XGBoost</p>
    
    <h2>Available Endpoints:</h2>
    
    <div class="endpoint">
        <span class="method get">GET</span>
        <strong>/health</strong>
        <p>Check API health status</p>
        <p>Example: <code>curl http://localhost:5000/health</code></p>
    </div>
    
    <div class="endpoint">
        <span class="method get">GET</span>
        <strong>/model/info</strong>
        <p>Get model information and metrics</p>
        <p>Example: <code>curl http://localhost:5000/model/info</code></p>
    </div>
    
    <div class="endpoint">
        <span class="method post">POST</span>
        <strong>/predict</strong>
        <p>Generate stock price predictions</p>
        <p>Body: <code>{"data_path": "data/sample_data.csv"}</code></p>
        <p>Example: <code>curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"data_path": "data/sample_data.csv"}'</code></p>
    </div>
    
    <h2>Quick Test:</h2>
    <p>Open a new terminal and try:</p>
    <pre><code>curl http://localhost:5000/health</code></pre>
    
    <h2>Documentation:</h2>
    <p>For full documentation, see <a href="https://github.com/YOUR-USERNAME/tata-steel-forecast">GitHub Repository</a></p>
</body>
</html>
"""

@app.route('/')
def home():
    """Homepage with API documentation"""
    return render_template_string(HOME_HTML)

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "tata-steel-forecast",
        "version": "0.1.0"
    })

@app.route('/model/info', methods=['GET'])
def model_info():
    """Get model information"""
    try:
        # Check if model exists
        if not os.path.exists(MODEL_PATH):
            return jsonify({
                "status": "error",
                "message": "Model not found. Please train the model first."
            }), 404
        
        # Load metrics if available
        metrics_path = 'models/metrics.json'
        metrics = {}
        if os.path.exists(metrics_path):
            import json
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
        
        return jsonify({
            "status": "success",
            "model": {
                "path": MODEL_PATH,
                "size_mb": round(os.path.getsize(MODEL_PATH) / (1024*1024), 2),
                "algorithm": "XGBoost Regressor"
            },
            "metrics": metrics
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    """Generate predictions"""
    try:
        data = request.json
        
        if not data or 'data_path' not in data:
            return jsonify({
                "status": "error",
                "message": "Missing 'data_path' in request body"
            }), 400
        
        data_path = data['data_path']
        
        # Check if data file exists
        if not os.path.exists(data_path):
            return jsonify({
                "status": "error",
                "message": f"Data file not found: {data_path}"
            }), 404
        
        # Check if model exists
        if not os.path.exists(MODEL_PATH):
            return jsonify({
                "status": "error",
                "message": "Model not found. Please train the model first."
            }), 404
        
        # Load model and data
        model = load_model(MODEL_PATH)
        df = load_data(data_path)
        dfp = prepare_features(df, dropna=False)
        
        # Prepare features
        import numpy as np
        features = [c for c in dfp.columns if c not in ["Date", "target"]]
        X = dfp[features].select_dtypes(include=[np.number])
        
        # Remove rows with NaN
        valid_idx = X.notna().all(axis=1)
        X_valid = X[valid_idx]
        dates_valid = dfp["Date"][valid_idx]
        
        # Generate predictions
        predictions = model.predict(X_valid)
        
        # Create results
        results = []
        for date, pred in zip(dates_valid, predictions):
            results.append({
                "date": date.strftime('%Y-%m-%d'),
                "predicted_close": round(float(pred), 2)
            })
        
        return jsonify({
            "status": "success",
            "predictions": results,
            "count": len(results)
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

@app.route('/train', methods=['POST'])
def train():
    """Trigger model training (use with caution in production)"""
    try:
        data = request.json or {}
        data_path = data.get('data_path', 'data/sample_data.csv')
        
        # Run training in background
        import subprocess
        subprocess.Popen([
            sys.executable, 
            'train.py', 
            '--data', data_path
        ])
        
        return jsonify({
            "status": "training started",
            "data_path": data_path,
            "message": "Training process initiated in background"
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Starting Tata Steel Forecast API...")
    print("📍 Server running at: http://localhost:5000")
    print("📖 Documentation: http://localhost:5000")
    print("💚 Health check: http://localhost:5000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
