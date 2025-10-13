# Complete Setup and Deployment Guide

## 🚀 From Zero to GitHub in 10 Minutes

This guide walks you through setting up, testing, and deploying your Tata Steel Stock Forecasting project to GitHub.

---

## Part 1: Local Setup (5 minutes)

### Step 1: Verify Files
You should have these files in `c:\Users\Admin\Downloads\stocks`:
```
✅ README.md, requirements.txt, .gitignore
✅ src/data.py, src/model.py, src/__init__.py
✅ train.py, predict.py
✅ tests/test_data.py, test_model.py, test_pipeline.py
✅ data/sample_data.csv
✅ .github/workflows/ci.yml
```

### Step 2: Create Virtual Environment

Open PowerShell in the project directory:

```powershell
cd C:\Users\Admin\Downloads\stocks

# Create virtual environment
python -m venv .venv

# Activate it
.\.venv\Scripts\Activate.ps1

# Verify activation (should show (.venv) in prompt)
```

**Troubleshooting**: If activation fails with "execution policy" error:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 3: Install Dependencies

```powershell
# Upgrade pip
python -m pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt
```

This installs: numpy, pandas, scikit-learn, xgboost, shap, joblib, pyyaml, pytest

**Wait time**: 2-3 minutes depending on internet speed

### Step 4: Verify Installation

```powershell
# Check Python version
python --version

# Check installed packages
pip list

# Quick test
python -c "import pandas, numpy, xgboost, sklearn; print('All imports successful!')"
```

---

## Part 2: Testing (2 minutes)

### Step 5: Run Tests

```powershell
# Run all tests
pytest tests/ -v

# Expected output:
# tests/test_data.py::test_load_data PASSED
# tests/test_data.py::test_add_lag_features PASSED
# tests/test_data.py::test_add_return_and_rolling PASSED
# tests/test_data.py::test_prepare_features PASSED
# tests/test_data.py::test_feature_no_leakage PASSED
# tests/test_model.py::test_pipeline_runs PASSED
# tests/test_model.py::test_model_save_load PASSED
# tests/test_model.py::test_predictions_reasonable PASSED
# tests/test_pipeline.py::test_pipeline_runs PASSED
```

**If tests fail**: Check error messages and ensure all dependencies installed correctly.

### Step 6: Train Model

```powershell
# Train on sample data
python train.py --data data/sample_data.csv --target Close --date_col Date

# Expected output:
# Training summary: {'mean_rmse': 0.XX, 'mean_mae': 0.XX}
# Top SHAP features:
#   feature  mean_abs_shap
# 0  Close_lag_1    0.XXX
# ...
```

Check that `models/xgb_model.joblib` and `models/metrics.json` were created:
```powershell
ls models/
```

### Step 7: Test Predictions

```powershell
# Generate predictions
python predict.py --model models/xgb_model.joblib --data data/sample_data.csv --output predictions.csv

# View predictions
Get-Content predictions.csv | Select-Object -First 6
```

---

## Part 3: GitHub Setup (3 minutes)

### Step 8: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `tata-steel-forecast` (or your choice)
3. Description: "Stock price forecasting pipeline using XGBoost and feature engineering"
4. **Keep it Public** (or Private if preferred)
5. **DO NOT** initialize with README, .gitignore, or license (we have them)
6. Click "Create repository"

### Step 9: Initialize Git

Back in PowerShell:

```powershell
# Initialize git (if not already done)
git init

# Check status
git status

# Should show untracked files
```

### Step 10: First Commit

```powershell
# Add all files
git add .

# Verify what will be committed
git status

# Commit
git commit -m "Initial commit: Complete stock forecasting pipeline with XGBoost"

# Verify commit
git log --oneline
```

### Step 11: Connect to GitHub

Replace `<your-username>` with your actual GitHub username:

```powershell
# Set branch to main
git branch -M main

# Add remote
git remote add origin https://github.com/<your-username>/tata-steel-forecast.git

# Verify remote
git remote -v
```

### Step 12: Push to GitHub

```powershell
# Push to GitHub
git push -u origin main

# Enter GitHub credentials if prompted
```

**Authentication Options**:
- **Token**: Use Personal Access Token (Settings → Developer settings → Personal access tokens)
- **SSH**: Set up SSH keys (recommended for frequent use)
- **GitHub CLI**: Use `gh auth login`

---

## Part 4: Post-Deployment (Optional)

### Step 13: Verify on GitHub

1. Go to your repository: `https://github.com/<your-username>/tata-steel-forecast`
2. Verify files are there
3. Check that README displays correctly
4. Click "Actions" tab to see CI/CD workflow (may take a few minutes)

### Step 14: Add Repository Details

On GitHub:
1. Click "About" settings (gear icon top right)
2. Add description: "Stock price forecasting using ML"
3. Add topics: `machine-learning` `xgboost` `stock-prediction` `time-series` `python` `forecasting`
4. Add website (if you have docs)
5. Save changes

### Step 15: Create Release (Optional)

```powershell
# Tag the release
git tag -a v0.1.0 -m "Initial release: Basic forecasting pipeline"

# Push tag
git push origin v0.1.0
```

On GitHub:
1. Go to "Releases" → "Draft a new release"
2. Choose tag: v0.1.0
3. Title: "v0.1.0 - Initial Release"
4. Description: Copy from PROJECT_SUMMARY.md
5. Publish release

---

## Part 5: Next Steps

### For Your Portfolio

Add to README.md badge section:
```markdown
![Build Status](https://github.com/<username>/tata-steel-forecast/workflows/CI%2FCD%20Pipeline/badge.svg)
```

### Share Your Project

- LinkedIn post with project link
- Twitter/X announcement
- Add to portfolio website
- Include in resume

### Continue Development

```powershell
# Create development branch
git checkout -b develop

# Make changes
# ... edit files ...

# Commit changes
git add .
git commit -m "Add new feature"

# Push branch
git push origin develop

# Create Pull Request on GitHub
```

---

## Troubleshooting

### Issue: Python not found
**Solution**: Install Python 3.8+ from python.org or Microsoft Store

### Issue: pip install fails
**Solution**: 
```powershell
python -m pip install --upgrade pip
pip install --upgrade setuptools wheel
```

### Issue: pytest not found
**Solution**: Make sure virtual environment is activated
```powershell
.\.venv\Scripts\Activate.ps1
pip install pytest
```

### Issue: Git push authentication failed
**Solution**: Use Personal Access Token instead of password
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`
4. Use token as password when pushing

### Issue: XGBoost installation fails
**Solution**: 
```powershell
# Try with conda (if you have it)
conda install -c conda-forge xgboost

# Or use pip with no-cache
pip install --no-cache-dir xgboost
```

---

## Quick Command Reference

```powershell
# Activate environment
.\.venv\Scripts\Activate.ps1

# Train model
python train.py --data data/sample_data.csv

# Run tests
pytest tests/ -v

# Check git status
git status

# Commit changes
git add .
git commit -m "Your message"
git push

# View log
git log --oneline --graph

# Create branch
git checkout -b feature-name

# Switch branch
git checkout main
```

---

## Success Checklist

After completing this guide, you should have:

- ✅ Virtual environment created and activated
- ✅ All dependencies installed
- ✅ Tests passing
- ✅ Model trained successfully
- ✅ Predictions generated
- ✅ Git repository initialized
- ✅ Code pushed to GitHub
- ✅ Repository configured with description and topics
- ✅ README displaying correctly
- ✅ CI/CD workflow running

---

## 🎉 Congratulations!

Your Tata Steel Stock Forecasting project is now live on GitHub!

**Next Actions**:
1. ⭐ Star your own repo (why not!)
2. 📝 Share on LinkedIn/Twitter
3. 👥 Invite collaborators
4. 🚀 Keep improving

**Questions?** Open an issue on your GitHub repo or check CONTRIBUTING.md

---

**Built with ❤️ | Ready for production | MIT Licensed**
