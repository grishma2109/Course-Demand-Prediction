import pandas as pd

def create_features(df):

    df_course = df.groupby(["Course_Name", "Date"]).agg({
        "Hours_Watched": "sum",
        "Course_Rating": "mean",
        "Completion_Rate": "mean",
        "Dropout_Risk_Score": "mean",
        "Years_of_Experience": "mean",
        "Salary_Expectation": "mean",
        "Loss_of_Job_Score": "mean"
    }).reset_index()

    df_course["growth_rate"] = (
        df_course.groupby("Course_Name")["Hours_Watched"]
        .pct_change()
    )

    # Date features
    df_course["Month"] = df_course["Date"].dt.month
    df_course["Quarter"] = df_course["Date"].dt.quarter
    df_course["Year"] = df_course["Date"].dt.year

    # Lag features
    df_course["lag_1"] = df_course.groupby("Course_Name")["Hours_Watched"].shift(1)
    df_course["lag_2"] = df_course.groupby("Course_Name")["Hours_Watched"].shift(2)
    df_course["lag_3"] = df_course.groupby("Course_Name")["Hours_Watched"].shift(3)

    df_course["rolling_mean_3"] = (
        df_course.groupby("Course_Name")["Hours_Watched"]
        .rolling(3)
        .mean()
        .reset_index(level=0, drop=True)
    )

    df_course = df_course.dropna()

    return df_course