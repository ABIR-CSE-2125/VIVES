import pandas as pd
import streamlit as st

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


def load_css(file_name: str):
    with open(file_name) as f:
        css = f"<style>{f.read()}</style>"
        st.markdown(css, unsafe_allow_html=True)