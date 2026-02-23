import os
import pickle
from src.feature_engineering import create_features
from src.model_training import train_model
from src.data_processing import load_and_clean_data
from sklearn.linear_model import LinearRegression
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
from flask import Flask, render_template, jsonify
app = Flask(__name__)

df = load_and_clean_data("data_100000_records_daily.csv")
df = create_features(df)
train_model(df)
model_path = os.path.join("models", "lr_model.pkl")
model = pickle.load(open(model_path, "rb"))


import numpy as np
from sklearn.metrics import r2_score

# Prepare features
features = [
    "lag_1", "lag_2", "lag_3",
    "rolling_mean_3",
    "Month", "Quarter", "Year",
    "Course_Rating",
    "Completion_Rate",
    "Dropout_Risk_Score",
    "Years_of_Experience",
    "Salary_Expectation",
    "Loss_of_Job_Score"
]

X = df[features]
y = df["growth_rate"]

split_index = int(len(df) * 0.8)

X_test = X.iloc[split_index:]
y_test = y.iloc[split_index:]

# Predict
y_pred = model.predict(X_test)

# R2
print("R2 Score:", r2_score(y_test, y_pred))

# Residuals
residuals = y_test - y_pred

# Variance of residuals
print("Residual Variance:", np.var(residuals))

# Variance of predictions
print("Prediction Variance:", np.var(y_pred))

# Variance of target
print("Target Variance:", np.var(y_test))
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/courses")
def get_courses():

    # Get latest record per course using Date
    latest = df.sort_values("Date").groupby("Course_Name").last().reset_index()

    # Ensure all required features exist
    latest = latest.fillna(0)

    growth = model.predict(latest[features])

    median_hours = df["Hours_Watched"].median()

    result = []

    for i, row in latest.iterrows():
        next_hours = row["Hours_Watched"] * (1 + growth[i])
        demand = "High" if growth[i] > 0  else "Low"
# and next_hours >= median_hours
        result.append({
            "course": row["Course_Name"],
            "growth": float(growth[i]),
            "next_hours": float(next_hours),
            "demand": demand,
            "salary": float(row["Salary_Expectation"])
        })

    return jsonify(result)


# @app.route("/trend/<course>")
# def course_trend(course):
#     course_df = df[df["Course_Name"] == course]
#     return jsonify({
#         "months": course_df["Month"].astype(str).tolist(),
#         "hours": course_df["Hours_Watched"].tolist()
#     })



@app.route("/trend/<course>")
def course_trend(course):

    course_df = df[df["Course_Name"] == course].copy()

    # Convert Date to monthly period
    course_df["YearMonth"] = course_df["Date"].dt.to_period("M")

    # Aggregate monthly hours
    monthly = (
        course_df.groupby("YearMonth")["Hours_Watched"]
        .sum()
        .reset_index()
    )

    # Convert back to string for JSON
    monthly["YearMonth"] = monthly["YearMonth"].astype(str)

    # Create time index
    monthly["Time_Index"] = np.arange(len(monthly))

    X = monthly[["Time_Index"]]
    y = monthly["Hours_Watched"]

    lr = LinearRegression()
    lr.fit(X, y)

    trend = lr.predict(X)

    return jsonify({
        "months": monthly["YearMonth"].tolist(),
        "hours": y.tolist(),
        "trend": trend.tolist(),
        "slope": float(lr.coef_[0])
    })
@app.route("/cluster")
def cluster():

    # Take latest record per course
    # cluster_df = df.sort_values("Month").groupby("Course_Name").last().reset_index()
    cluster_df = df.sort_values("Date").groupby("Course_Name").last().reset_index()

    # Encode Skill_Level if it is text
    if "Skill_Level" in cluster_df.columns:
        if cluster_df["Skill_Level"].dtype == "object":
            cluster_df["Skill_Level"] = cluster_df["Skill_Level"].astype("category").cat.codes
    else:
        # If Skill_Level does not exist, create dummy numeric column
        cluster_df["Skill_Level"] = np.random.randint(1, 4, size=len(cluster_df))

    # Select features for clustering
    X = cluster_df[[
        "Skill_Level",
        "Hours_Watched",
        "Salary_Expectation"
    ]]

    # Remove missing values
    X = X.fillna(0)

    # Apply KMeans
    kmeans = KMeans(n_clusters=3, random_state=42)
    cluster_df["Cluster"] = kmeans.fit_predict(X)

    return jsonify(
        cluster_df[[
            "Course_Name",
            "Skill_Level",
            "Hours_Watched",
            "Salary_Expectation",
            "Cluster"
        ]].to_dict(orient="records")
    )

@app.route("/feature_importance")
def feature_importance():

    importances = model.feature_importances_

    return jsonify({
        "features": features,
        "importance": importances.tolist()
    })


if __name__ == "__main__":
    app.run(debug=True)