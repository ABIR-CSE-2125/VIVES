import pandas as pd


def df_from_rows(rows):
    return pd.DataFrame(
        rows,
        columns=[
            "id",
            "date",
            "weekday",
            "month",
            "week_in_month",
            "amount",
            "type",
            "comments",
        ],
    )


def monthly_summary(df):
    return df.groupby("month")["amount"].sum().reset_index()


def category_summary(df):
    return df.groupby("type")["amount"].sum().reset_index()


def weekday_summary(df):
    return df.groupby("weekday")["amount"].sum().reset_index()
