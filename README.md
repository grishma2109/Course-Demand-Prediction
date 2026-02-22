# Course-Demand-Prediction
📊 Course Demand Prediction System

A Machine Learning based web application that predicts course demand trends using historical data and multiple regression models. This project helps analyze which courses are growing, stable, or declining based on user engagement metrics.

🚀 Project Overview

The Course Demand Prediction system:

Analyzes historical course data

Generates lag-based and time-based features

Trains multiple ML models

Predicts future course demand

Displays trends using charts in a web interface

🛠️ Tech Stack
🔹 Backend

Python

Flask

Pandas

NumPy

Scikit-learn

XGBoost

LightGBM

CatBoost

🔹 Frontend

HTML

CSS

JavaScript

Chart.js

📂 Project Structure
Course-Demand-Prediction/
│
├── app.py
├── training_model.py
├── requirements.txt
├── final_monthly_data.csv
│
├── src/
│   ├── feature_engineering.py
│   ├── model_training.py
│
├── templates/
│   └── index.html
│
└── static/
    ├── style.css
    └── script.js
📈 Features

Lag feature creation (Previous 1 month, 2 months)

Time-based feature engineering

Linear Regression

KNN Regressor

XGBoost Regressor

Ensemble model comparison

R², MAE, RMSE evaluation

Trend classification (Strong Growth, Moderate Growth, Stable, Decline)

Interactive charts for visualization

⚙️ How to Run the Project
1️⃣ Clone the repository
git clone https://github.com/grishma2109/Course-Demand-Prediction.git
cd Course-Demand-Prediction
2️⃣ Install dependencies
pip install -r requirements.txt
3️⃣ Run the Flask app
python app.py

Open browser:

http://127.0.0.1:5000/
📊 Model Evaluation Metrics

R² Score

Mean Absolute Error (MAE)

Root Mean Squared Error (RMSE)

These metrics help evaluate prediction accuracy.

🧠 Machine Learning Approach

Data preprocessing

Feature engineering (lag & time features)

Train-test split

Model training:

Linear Regression

KNN

XGBoost

LightGBM

CatBoost

Model comparison

Best model selection

🔮 Future Enhancements

Deploy using AWS / Render

Add user login authentication

Add real-time data updates

Add model retraining API

Add download prediction reports (CSV)

👩‍💻 Author

Grishma Shanbhag
