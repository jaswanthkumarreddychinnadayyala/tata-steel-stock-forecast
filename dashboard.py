# Streamlit Web Dashboard for Stock Forecasting
# Run with: streamlit run dashboard.py

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from data import load_data, prepare_features
from model import load_model, train_xgb
import numpy as np

# Page config
st.set_page_config(
    page_title="Tata Steel Forecast",
    page_icon="📈",
    layout="wide"
)

# Title
st.title("📈 Tata Steel Stock Price Forecasting")
st.markdown("*Machine Learning powered predictions using XGBoost and feature engineering*")

# Sidebar
st.sidebar.header("⚙️ Settings")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload Stock Data CSV", type=['csv'])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    df['Date'] = pd.to_datetime(df['Date'])
    st.sidebar.success("✅ Data loaded!")
    data_source = "Uploaded file"
else:
    if os.path.exists('data/sample_data.csv'):
        df = load_data('data/sample_data.csv')
        st.sidebar.info("ℹ️ Using sample data")
        data_source = "Sample data"
    else:
        st.error("No data available. Please upload a CSV file.")
        st.stop()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📊 Data Overview", "🔮 Predictions", "📈 Visualizations", "ℹ️ About"])

with tab1:
    st.header("📊 Historical Stock Data")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Days", len(df))
    with col2:
        st.metric("Latest Close", f"${df['Close'].iloc[-1]:.2f}")
    with col3:
        st.metric("Average Price", f"${df['Close'].mean():.2f}")
    with col4:
        st.metric("Volatility", f"{df['Close'].std():.2f}")
    
    st.subheader("Recent Data")
    st.dataframe(df.tail(10), use_container_width=True)
    
    st.subheader("Data Summary")
    st.write(df.describe())

with tab2:
    st.header("🔮 Generate Predictions")
    
    # Check if model exists
    model_path = 'models/xgb_model.joblib'
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("🎯 Train New Model", type="primary"):
            with st.spinner("Training model... This may take a minute."):
                try:
                    dfp = prepare_features(df)
                    features = [c for c in dfp.columns if c not in ["Date", "target"]]
                    X = dfp[features].select_dtypes(include=[np.number])
                    y = dfp["target"]
                    
                    model, summary = train_xgb(X, y, n_splits=3)
                    
                    # Save model
                    from model import save_model
                    import json
                    
                    os.makedirs('models', exist_ok=True)
                    save_model(model, model_path)
                    
                    with open('models/metrics.json', 'w') as f:
                        json.dump(summary, f)
                    
                    st.success("✅ Model trained successfully!")
                    st.json(summary)
                except Exception as e:
                    st.error(f"Error training model: {e}")
    
    with col2:
        if os.path.exists(model_path):
            st.success("✅ Model available")
            
            # Load metrics
            if os.path.exists('models/metrics.json'):
                import json
                with open('models/metrics.json', 'r') as f:
                    metrics = json.load(f)
                st.metric("RMSE", f"{metrics.get('mean_rmse', 0):.2f}")
                st.metric("MAE", f"{metrics.get('mean_mae', 0):.2f}")
        else:
            st.warning("⚠️ No model found. Train a model first.")
    
    st.divider()
    
    if os.path.exists(model_path):
        if st.button("🚀 Generate Predictions"):
            with st.spinner("Generating predictions..."):
                try:
                    model = load_model(model_path)
                    dfp = prepare_features(df, dropna=False)
                    
                    features = [c for c in dfp.columns if c not in ["Date", "target"]]
                    X = dfp[features].select_dtypes(include=[np.number])
                    
                    valid_idx = X.notna().all(axis=1)
                    X_valid = X[valid_idx]
                    dates_valid = dfp["Date"][valid_idx]
                    
                    predictions = model.predict(X_valid)
                    
                    results = pd.DataFrame({
                        'Date': dates_valid,
                        'Predicted_Close': predictions
                    })
                    
                    st.success(f"✅ Generated {len(results)} predictions!")
                    
                    st.subheader("Predictions Preview")
                    st.dataframe(results.tail(10), use_container_width=True)
                    
                    # Download button
                    csv = results.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Predictions CSV",
                        data=csv,
                        file_name="predictions.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"Error generating predictions: {e}")

with tab3:
    st.header("📈 Visualizations")
    
    # Price chart
    st.subheader("Historical Closing Price")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df['Date'], 
        y=df['Close'],
        mode='lines',
        name='Close Price',
        line=dict(color='#3498db', width=2)
    ))
    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Close Price ($)",
        hovermode='x unified',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Volume chart
    if 'Volume' in df.columns:
        st.subheader("Trading Volume")
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=df['Date'],
            y=df['Volume'],
            name='Volume',
            marker_color='#2ecc71'
        ))
        fig2.update_layout(
            xaxis_title="Date",
            yaxis_title="Volume",
            template='plotly_white'
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Price distribution
    st.subheader("Price Distribution")
    fig3 = go.Figure()
    fig3.add_trace(go.Histogram(
        x=df['Close'],
        nbinsx=30,
        marker_color='#9b59b6',
        name='Frequency'
    ))
    fig3.update_layout(
        xaxis_title="Close Price ($)",
        yaxis_title="Frequency",
        template='plotly_white'
    )
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.header("ℹ️ About This Project")
    
    st.markdown("""
    ### 🎯 Project Overview
    
    This is a machine learning application for forecasting stock prices using:
    - **XGBoost Regression** for prediction
    - **Time-series features** (lags, rolling statistics, momentum)
    - **TimeSeriesSplit** cross-validation
    - **RMSE and MAE** evaluation metrics
    
    ### 🔧 Features
    
    - ✅ Upload custom stock data (CSV format)
    - ✅ Train models on your data
    - ✅ Generate next-day price forecasts
    - ✅ Interactive visualizations
    - ✅ Download predictions as CSV
    
    ### 📊 Data Requirements
    
    Your CSV should have these columns:
    - `Date`: Trading date (YYYY-MM-DD format)
    - `Close`: Closing price
    - `Open`, `High`, `Low`, `Volume` (optional but recommended)
    
    ### 🚀 Deployment
    
    This dashboard can be deployed to:
    - Streamlit Cloud (free)
    - Heroku
    - AWS/GCP/Azure
    
    ### 📚 Documentation
    
    For full documentation, visit the [GitHub Repository](https://github.com/YOUR-USERNAME/tata-steel-forecast)
    
    ### 👨‍💻 Developer
    
    Built with: Python, XGBoost, Streamlit, Plotly
    """)
    
    st.info("💡 **Tip**: For best results, use at least 100 days of historical data.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #7f8c8d;'>
    <p>📈 Tata Steel Stock Forecast | Built with Streamlit & XGBoost | 
    <a href='https://github.com/YOUR-USERNAME/tata-steel-forecast'>GitHub</a></p>
</div>
""", unsafe_allow_html=True)
