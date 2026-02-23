# ==================== IMPORTS ====================
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import pickle

# ==================== 1️⃣ LOAD DATA ====================
df = pd.read_csv("data_100000_records_daily.csv")  # Replace with your CSV file

# ==================== 2️⃣ DEFINE TARGET AND FEATURES ====================
y = df["Hours_Watched"]
X = df.drop(columns=["Learner_ID", "Date", "Hours_Watched"])

# ==================== 3️⃣ ENCODE CATEGORICAL VARIABLES ====================
categorical_cols = ["Experience_Category", "Course_Name", "Skill_Level", "Device_Type"]
X = pd.get_dummies(X, columns=categorical_cols, drop_first=True)

# ==================== 4️⃣ SCALE FEATURES (for KNN) ====================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ==================== 5️⃣ TRAIN-TEST SPLIT ====================
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# ==================== 6️⃣ LINEAR REGRESSION ====================
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr = lr.predict(X_test)

mae_lr = mean_absolute_error(y_test, y_pred_lr)
rmse_lr = np.sqrt(mean_squared_error(y_test, y_pred_lr))
r2_lr = lr.score(X_test, y_test)  # LinearRegression has its own score method

# ==================== 7️⃣ XGBOOST ====================
xgb = XGBRegressor(n_estimators=100, learning_rate=0.1, random_state=42)
xgb.fit(X_train, y_train)
y_pred_xgb = xgb.predict(X_test)

mae_xgb = mean_absolute_error(y_test, y_pred_xgb)
rmse_xgb = np.sqrt(mean_squared_error(y_test, y_pred_xgb))
r2_xgb = xgb.score(X_test, y_test)

# ==================== 8️⃣ KNN REGRESSOR ====================
knn = KNeighborsRegressor(n_neighbors=5, weights='distance')
knn.fit(X_train, y_train)
y_pred_knn = knn.predict(X_test)

mae_knn = mean_absolute_error(y_test, y_pred_knn)
rmse_knn = np.sqrt(mean_squared_error(y_test, y_pred_knn))
r2_knn = knn.score(X_test, y_test)

# ==================== 9️⃣ RESULTS COMPARISON ====================
results = {
    "Linear Regression": {"MAE": mae_lr, "RMSE": rmse_lr, "R2": r2_lr},
    "XGBoost": {"MAE": mae_xgb, "RMSE": rmse_xgb, "R2": r2_xgb},
    "KNN": {"MAE": mae_knn, "RMSE": rmse_knn, "R2": r2_knn}
}

comparison_df = pd.DataFrame(results).T
print("✅ Model Comparison:\n", comparison_df)

# ==================== 🔟 SAVE MODELS ====================
with open("scaler.pkl", "wb") as f:
    pickle.dump(scaler, f)

with open("lr_model.pkl", "wb") as f:
    pickle.dump(lr, f)

with open("xgb_model.pkl", "wb") as f:
    pickle.dump(xgb, f)

with open("knn_model.pkl", "wb") as f:
    pickle.dump(knn, f)

print("\nAll models and scaler saved successfully!")