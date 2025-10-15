# 🚀 DEPLOYMENT GUIDE - Tata Steel Stock Forecasting

## Complete Guide to Deploy Your ML Project

---

## 📋 Table of Contents

1. [GitHub Deployment (Portfolio)](#1-github-deployment)
2. [Local Production Setup](#2-local-production-setup)
3. [Cloud Deployment Options](#3-cloud-deployment)
4. [API Deployment](#4-api-deployment)
5. [Web Dashboard Deployment](#5-web-dashboard)
6. [Docker Deployment](#6-docker-deployment)
7. [Automated Scheduling](#7-automated-scheduling)

---

## 1. 🌐 GitHub Deployment (Portfolio)

### What You Get
- ✅ Showcase your project to employers
- ✅ Version control and collaboration
- ✅ Automated CI/CD testing
- ✅ Professional portfolio piece

### Steps

#### A. Push to GitHub (Main Deployment)

```powershell
# 1. Create repo on GitHub: https://github.com/new
# Name: tata-steel-forecast

# 2. Connect and push
git remote add origin https://github.com/YOUR-USERNAME/tata-steel-forecast.git
git push -u origin main
```

#### B. Configure Repository

1. **Add Description**: 
   - "ML pipeline for stock forecasting using XGBoost and time-series validation"

2. **Add Topics**:
   - `machine-learning`, `xgboost`, `stock-prediction`, `time-series`, `python`

3. **Enable GitHub Pages** (Optional):
   - Settings → Pages
   - Source: Deploy from branch `main` → `/docs` or `/`

#### C. Add Badges to README

Add these at the top of README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
```

---

## 2. 💻 Local Production Setup

### For Running on Your Machine

#### A. Production Environment

```powershell
# Create production virtual environment
python -m venv .venv-prod
.\.venv-prod\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Train model
python train.py --data data/your_real_data.csv

# Set up as Windows service or Task Scheduler (see #7)
```

#### B. Environment Variables

Create `.env` file (DO NOT commit this):

```ini
# .env
MODEL_PATH=models/xgb_model.joblib
DATA_PATH=data/tata_steel_live.csv
LOG_LEVEL=INFO
OUTPUT_DIR=predictions/
```

Install python-dotenv:
```powershell
pip install python-dotenv
```

Update train.py to use env variables:
```python
from dotenv import load_dotenv
import os

load_dotenv()
model_path = os.getenv('MODEL_PATH', 'models/xgb_model.joblib')
```

---

## 3. ☁️ Cloud Deployment Options

### Option A: Heroku (Easy, Free Tier)

#### Setup Files

**Procfile** (create in root):
```
web: python -m http.server $PORT
worker: python train.py --data data/sample_data.csv
```

**runtime.txt**:
```
python-3.11.0
```

#### Deploy Commands:
```powershell
# Install Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
heroku login
heroku create tata-steel-forecast
git push heroku main
```

---

### Option B: AWS (Scalable, Professional)

#### AWS Lambda Deployment

**1. Create Lambda Function Package**

```powershell
# Create deployment package
mkdir lambda_package
pip install -r requirements.txt -t lambda_package/
Copy-Item -Recurse src lambda_package/
Copy-Item train.py lambda_package/
Copy-Item predict.py lambda_package/

# Zip it
Compress-Archive -Path lambda_package/* -DestinationPath lambda_deploy.zip
```

**2. Create Lambda Handler** (lambda_handler.py):

```python
import json
from predict import predict

def lambda_handler(event, context):
    data_path = event['data_path']
    model_path = event.get('model_path', 'models/xgb_model.joblib')
    
    results = predict(model_path, data_path)
    
    return {
        'statusCode': 200,
        'body': json.dumps(results.to_dict('records'))
    }
```

**3. Deploy to AWS**:
- Go to AWS Lambda console
- Create function → Author from scratch
- Upload lambda_deploy.zip
- Set handler: `lambda_handler.lambda_handler`

#### AWS S3 + EC2 Deployment

```bash
# SSH into EC2 instance
ssh -i your-key.pem ec2-user@your-instance.amazonaws.com

# Clone repo
git clone https://github.com/YOUR-USERNAME/tata-steel-forecast.git
cd tata-steel-forecast

# Setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run
python train.py --data data/sample_data.csv
```

---

### Option C: Google Cloud Platform

#### Cloud Run Deployment

**1. Create Dockerfile** (see #6 below)

**2. Deploy**:
```bash
gcloud run deploy tata-steel-forecast \
  --source . \
  --region us-central1 \
  --allow-unauthenticated
```

---

### Option D: Azure (Microsoft Cloud)

#### Azure ML Deployment

```bash
# Install Azure CLI
az login

# Create resource group
az group create --name stock-forecast-rg --location eastus

# Deploy to Azure ML
az ml model deploy \
  --name tata-steel-forecast \
  --model models/xgb_model.joblib
```

---

## 4. 🔌 API Deployment

### Create REST API with Flask

**api.py** (create this):

```python
from flask import Flask, request, jsonify
from predict import predict
import os

app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "service": "stock-forecast"})

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    try:
        data = request.json
        data_path = data.get('data_path')
        model_path = data.get('model_path', 'models/xgb_model.joblib')
        
        results = predict(model_path, data_path)
        
        return jsonify({
            "status": "success",
            "predictions": results.to_dict('records')
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/train', methods=['POST'])
def train_endpoint():
    try:
        # Trigger training
        os.system('python train.py --data data/sample_data.csv')
        return jsonify({"status": "training started"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

**Install Flask**:
```powershell
pip install flask flask-cors
```

**Run API**:
```powershell
python api.py
```

**Test API**:
```powershell
# Health check
curl http://localhost:5000/health

# Make prediction
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"data_path": "data/sample_data.csv"}'
```

---

## 5. 📊 Web Dashboard Deployment

### Option A: Streamlit (Easiest)

**app.py** (create this):

```python
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data import load_data, prepare_features
from src.model import load_model

st.set_page_config(page_title="Tata Steel Forecast", page_icon="📈")

st.title("📈 Tata Steel Stock Price Forecasting")
st.markdown("*ML-powered predictions using XGBoost*")

# Sidebar
st.sidebar.header("Settings")
uploaded_file = st.sidebar.file_uploader("Upload CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("Data loaded!")
else:
    df = load_data('data/sample_data.csv')
    st.sidebar.info("Using sample data")

# Display data
st.subheader("📊 Historical Data")
st.dataframe(df.tail(10))

# Load model and predict
if st.button("🔮 Generate Predictions"):
    with st.spinner("Training model..."):
        model = load_model('models/xgb_model.joblib')
        # Make predictions
        st.success("Predictions generated!")

# Plot
fig = go.Figure()
fig.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Actual'))
st.plotly_chart(fig, use_container_width=True)
```

**Run Streamlit**:
```powershell
pip install streamlit plotly
streamlit run app.py
```

**Deploy to Streamlit Cloud**:
1. Push to GitHub
2. Go to https://share.streamlit.io
3. Connect repo → Deploy

---

### Option B: Dash (Professional)

```python
import dash
from dash import dcc, html
import plotly.graph_objects as go

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Tata Steel Stock Forecast"),
    dcc.Graph(id='stock-graph'),
    html.Button('Predict', id='predict-btn')
])

if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=8050)
```

---

## 6. 🐳 Docker Deployment

### Create Dockerfile

**Dockerfile**:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 5000

# Run training on start (optional)
RUN python train.py --data data/sample_data.csv

# Start API
CMD ["python", "api.py"]
```

**Build and Run**:

```powershell
# Build Docker image
docker build -t tata-steel-forecast .

# Run container
docker run -p 5000:5000 tata-steel-forecast

# Or with volume for data
docker run -p 5000:5000 -v ${PWD}/data:/app/data tata-steel-forecast
```

**Push to Docker Hub**:

```powershell
docker login
docker tag tata-steel-forecast YOUR-USERNAME/tata-steel-forecast:latest
docker push YOUR-USERNAME/tata-steel-forecast:latest
```

---

## 7. ⏰ Automated Scheduling

### Windows Task Scheduler

**1. Create Batch Script** (run_daily.bat):

```batch
@echo off
cd C:\Users\Admin\Downloads\stocks
call .venv\Scripts\activate.bat
python train.py --data data/tata_steel_live.csv
python predict.py --model models/xgb_model.joblib --data data/tata_steel_live.csv --output predictions_daily.csv
```

**2. Schedule Task**:

```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "C:\Users\Admin\Downloads\stocks\run_daily.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 6PM
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "StockForecast" -Description "Daily stock forecast"
```

Or manually:
1. Open Task Scheduler
2. Create Basic Task
3. Name: "Stock Forecast Daily"
4. Trigger: Daily at 6:00 PM
5. Action: Start a program → `run_daily.bat`

---

### Linux Cron Job

```bash
# Edit crontab
crontab -e

# Add line (runs daily at 6 PM)
0 18 * * * cd /path/to/stocks && /path/to/.venv/bin/python train.py --data data/tata_steel_live.csv
```

---

## 8. 📧 Email Notifications

**Add Email Alerts** (email_notifier.py):

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_prediction_email(predictions_path):
    sender = "your_email@gmail.com"
    receiver = "recipient@example.com"
    password = "your_app_password"
    
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = receiver
    msg['Subject'] = "Daily Stock Forecast - Tata Steel"
    
    with open(predictions_path, 'r') as f:
        body = f.read()
    
    msg.attach(MIMEText(body, 'plain'))
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender, password)
        server.send_message(msg)
```

---

## 9. 📊 Monitoring & Logging

**Add Logging** (update train.py):

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/training.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Use in code
logger.info("Training started")
logger.info(f"Model RMSE: {summary['mean_rmse']}")
```

---

## 10. 🚀 Production Checklist

### Before Deployment:

- [ ] **Code Quality**
  - [ ] All tests pass: `pytest tests/ -v`
  - [ ] No security vulnerabilities
  - [ ] Environment variables for sensitive data
  - [ ] Error handling implemented

- [ ] **Documentation**
  - [ ] README updated with deployment instructions
  - [ ] API documentation (if applicable)
  - [ ] Configuration guide

- [ ] **Data**
  - [ ] Real data source configured
  - [ ] Data validation implemented
  - [ ] Backup strategy in place

- [ ] **Monitoring**
  - [ ] Logging configured
  - [ ] Error alerting set up
  - [ ] Performance monitoring

- [ ] **Security**
  - [ ] API authentication (if deployed)
  - [ ] HTTPS enabled
  - [ ] No credentials in code
  - [ ] Input validation

---

## 🎯 Recommended Deployment Path

### For Portfolio/Resume:
```
1. ✅ Push to GitHub (Main showcase)
2. ✅ Deploy to Streamlit Cloud (Live demo)
3. ✅ Add project to LinkedIn/Portfolio
```

### For Production Use:
```
1. ✅ Deploy API to Cloud (AWS/Azure/GCP)
2. ✅ Set up Docker container
3. ✅ Configure automated scheduling
4. ✅ Add monitoring and alerts
```

### For Learning/Development:
```
1. ✅ Local setup with virtual environment
2. ✅ GitHub for version control
3. ✅ Jupyter notebooks for exploration
```

---

## 📞 Quick Deploy Commands

### GitHub (Portfolio):
```powershell
git remote add origin https://github.com/YOUR-USERNAME/tata-steel-forecast.git
git push -u origin main
```

### Streamlit (Live Demo):
```powershell
pip install streamlit
# Create app.py (see above)
streamlit run app.py
# Deploy to streamlit.io
```

### Docker (Container):
```powershell
docker build -t tata-steel-forecast .
docker run -p 5000:5000 tata-steel-forecast
```

### API (Local):
```powershell
pip install flask
python api.py
# Access at http://localhost:5000
```

---

## 🎉 Success Metrics

After deployment, your project should have:

- ✅ **Accessibility**: Accessible via URL/API
- ✅ **Reliability**: Runs without errors
- ✅ **Documentation**: Clear usage instructions
- ✅ **Monitoring**: Logs and error tracking
- ✅ **Automation**: Scheduled updates (if applicable)

---

## 📚 Additional Resources

- **GitHub Docs**: https://docs.github.com
- **Streamlit**: https://docs.streamlit.io
- **Docker**: https://docs.docker.com
- **AWS Lambda**: https://aws.amazon.com/lambda
- **Flask API**: https://flask.palletsprojects.com

---

**🚀 Ready to deploy? Start with GitHub push, then choose your deployment platform!**

*Need help? Check individual sections above for detailed instructions.*
