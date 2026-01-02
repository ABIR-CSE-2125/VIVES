import pandas as pd


def derive_date_parts(date_value):
    date_obj = pd.to_datetime(date_value)

    weekday = date_obj.day_name()
    month = date_obj.month_name()

    # Calculate week number inside month
    week_in_month = (
        date_obj.isocalendar().week
        - date_obj.to_period('M').start_time.isocalendar().week
        + 1
    )

    return weekday, month, int(week_in_month)
