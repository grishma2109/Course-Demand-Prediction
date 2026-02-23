import pickle
import os
# from xgboost import XGBRegressor,LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
def train_model(df):

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

    X_train = X.iloc[:split_index]
    X_test = X.iloc[split_index:]
    y_train = y.iloc[:split_index]
    y_test = y.iloc[split_index:]

    # model = XGBRegressor(
    #     n_estimators=900,
    #     learning_rate=0.03,
    #     max_depth=4,
    #     subsample=0.9,
    #     colsample_bytree=0.9,
    #     random_state=42
    # )
    model=LinearRegression()

    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    print("R2 Score:", r2_score(y_test, y_pred))

    os.makedirs("models", exist_ok=True)
    pickle.dump(model, open("models/lr_model.pkl", "wb"))

    print("Model saved successfully")

    return model