# 🚀 QUICK START

## Get Running in 5 Minutes!

### 1️⃣ Setup Environment (2 min)
```powershell
cd C:\Users\Admin\Downloads\stocks
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2️⃣ Train Model (1 min)
```powershell
python train.py --data data/sample_data.csv
```

### 3️⃣ Make Predictions (30 sec)
```powershell
python predict.py --model models/xgb_model.joblib --data data/sample_data.csv
```

### 4️⃣ Run Tests (1 min)
```powershell
pytest tests/ -v
```

### 5️⃣ Push to GitHub (30 sec)
```powershell
git init
git add .
git commit -m "Initial commit: Stock forecasting pipeline"
git remote add origin https://github.com/<your-username>/tata-steel-forecast.git
git push -u origin main
```

---

## 📚 More Help?

- **Setup Issues?** → [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **Want Details?** → [README.md](README.md)
- **Technical Deep Dive?** → [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md)
- **Contributing?** → [CONTRIBUTING.md](CONTRIBUTING.md)
- **All Docs?** → [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)

---

## ✅ What You Get

✅ **Complete ML Pipeline** - Data → Features → Model → Predictions  
✅ **Time-Series Safe** - No look-ahead bias  
✅ **Well Tested** - Unit & integration tests  
✅ **Documented** - 10+ markdown files  
✅ **CI/CD Ready** - GitHub Actions workflow  
✅ **Production Ready** - Error handling, logging  

---

## 🎯 Project Highlights

- **Machine Learning**: XGBoost with TimeSeriesSplit
- **Feature Engineering**: Lags, rolling stats, momentum
- **Explainability**: SHAP feature importance
- **Testing**: Comprehensive test suite
- **Documentation**: Professional-grade docs

---

**🎉 Your complete stock forecasting project is ready!**

*Built with ❤️ | MIT Licensed | GitHub Ready*
