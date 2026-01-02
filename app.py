import streamlit as st
import pandas as pd

from db import create_table, insert_expense, fetch_all
from utils import derive_date_parts
from analytics import (
    df_from_rows,
    monthly_summary,
    category_summary,
    weekday_summary,
)

st.set_page_config(page_title="Expense Tracker", layout="wide")

create_table()

st.title("💸 Daily Expense Tracker")


# ------------------------------
# Expense Entry Form
# ------------------------------
with st.form("expense_form"):
    date = st.date_input("Date")
    amount = st.number_input("Amount Spent", min_value=0.0, format="%.2f")
    exp_type = st.selectbox(
        "Type of Expense",
        ["Food", "Travel", "Rent", "Shopping", "Bills", "Medical", "Entertainment", "Misc"],
    )
    comments = st.text_area("Comments (optional)")

    submitted = st.form_submit_button("Save Entry")

    if submitted:
        weekday, month, week_in_month = derive_date_parts(date)

        insert_expense(
            str(date),
            weekday,
            month,
            week_in_month,
            amount,
            exp_type,
            comments,
        )

        st.success("Expense saved successfully!")


# ------------------------------
# Data & Analytics Section
# ------------------------------
rows = fetch_all()

if rows:
    df = df_from_rows(rows)

    st.subheader("📋 All Expenses")
    st.dataframe(df, use_container_width=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("📆 Monthly Spend")
        st.bar_chart(monthly_summary(df), x="month", y="amount")

    with col2:
        st.subheader("🏷 Category Spend")
        st.bar_chart(category_summary(df), x="type", y="amount")

    with col3:
        st.subheader("📅 Weekday Spend")
        st.bar_chart(weekday_summary(df), x="weekday", y="amount")

else:
    st.info("No expenses yet. Add one above!")
