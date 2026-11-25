
import pandas as pd


def profile_hillstrom(file_path="data/raw/hillstrom.csv"):
    df = pd.read_csv(file_path)

    print("\n========== DATASET OVERVIEW ==========")
    print("Shape:", df.shape)
    print("\nData types:")
    print(df.dtypes)

    print("\n========== DUPLICATE ANALYSIS ==========")
    print("Exact duplicate rows:", df.duplicated().sum())
    print("Duplicate percentage:", round(df.duplicated().mean() * 100, 2))

    print("\n========== MISSING VALUE ANALYSIS ==========")
    print(df.isna().sum())

    print("\n========== CATEGORICAL VALUE ANALYSIS ==========")
    categorical_columns = [
        "history_segment",
        "zip_code",
        "channel",
        "segment",
    ]

    for column in categorical_columns:
        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False))

    print("\n========== NUMERIC DISTRIBUTIONS ==========")
    print(df.describe().T)

    print("\n========== BINARY COLUMN VALIDATION ==========")
    binary_columns = ["mens", "womens", "newbie", "visit", "conversion"]

    for column in binary_columns:
        print(f"{column}: {sorted(df[column].dropna().unique())}")

    print("\n========== ASSIGNMENT GROUP COUNTS ==========")
    print(df["segment"].value_counts())

    print("\n========== SPENDING ANALYSIS ==========")
    print(df["spend"].quantile([0, 0.25, 0.50, 0.75, 0.90, 0.95, 0.99, 1]))


def investigate_hillstrom(df):
    print("\n========== POSITIVE SPENDING ==========")

    positive_spend = df.loc[df["spend"] > 0, "spend"]

    print("Positive spending records:", len(positive_spend))
    print("Zero spending records:", (df["spend"] == 0).sum())
    print("Positive spending percentage:", round(
        len(positive_spend) / len(df) * 100, 2
    ))

    print("\nPositive spending distribution:")
    print(positive_spend.describe(
        percentiles=[0.25, 0.50, 0.75, 0.90, 0.95, 0.99]
    ))

    print("\n========== CONVERSION AND VISIT CONSISTENCY ==========")
    print(pd.crosstab(df["visit"], df["conversion"]))

    print("\n========== SPENDING BY CONVERSION ==========")
    print(df.groupby("conversion")["spend"].agg(
        ["count", "mean", "median", "sum", "max"]
    ))

    print("\n========== SPENDING BY EXPERIMENT GROUP ==========")
    print(df.groupby("segment")["spend"].agg(
        ["count", "mean", "median", "sum"]
    ))

    print("\n========== EXPERIMENT GROUP CONVERSION ==========")
    print(df.groupby("segment")["conversion"].agg(
        ["count", "mean", "sum"]
    ))

    print("\n========== CATEGORY SPELLING INVESTIGATION ==========")
    for column in ["zip_code", "channel", "segment"]:
        print(column, sorted(df[column].unique()))

    print("\n========== LOGICAL VALIDATION ==========")
    print("Negative spending:", (df["spend"] < 0).sum())
    print("Conversion without visit:", (
        (df["conversion"] == 1) & (df["visit"] == 0)
    ).sum())
    print("Positive spend without conversion:", (
        (df["spend"] > 0) & (df["conversion"] == 0)
    ).sum())
    print("Conversion with zero spend:", (
        (df["conversion"] == 1) & (df["spend"] == 0)
    ).sum())



if __name__ == "__main__":
    profile_hillstrom()
if __name__ == "__main__":
    df = pd.read_csv("data/raw/hillstrom.csv")
    profile_hillstrom()
    investigate_hillstrom(df)