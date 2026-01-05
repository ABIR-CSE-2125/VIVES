import streamlit as st
import pandas as pd

from db import create_table, insert_expense, fetch_all
from utils import derive_date_parts, load_css
from analytics import (
    df_from_rows,
    monthly_summary,
    category_summary,
)

# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Expense Tracker",
    layout="wide"
)

# -------------------------------------------------
# Minimalist Styling
# -------------------------------------------------





load_css("style.css")



# -------------------------------------------------
# DB Setup
# -------------------------------------------------
create_table()


# -------------------------------------------------
# Title
# -------------------------------------------------
st.title("VIVES")


# -------------------------------------------------
# Expense Entry Form (centered)
# -------------------------------------------------
st.markdown('<div class="form-wrapper">', unsafe_allow_html=True)

with st.form("expense_form"):
    date = st.date_input("Date (you can type too)")
    amount = st.number_input("Amount Spent", min_value=0.0, format="%.2f")
    exp_type = st.selectbox(
        "Type of Expense",
        [
            "Rent",
            "Home",
            "Miscellaneous",
            "Investment",
            "Home Travel",
            "Food",
            "Home Accesory",
            "Debt Owed",
            "Clothing",
            "Travel",
            "Internet",
            "Grooming",
            "Kali Pujo",
            "Outing",
            "Subscription",
            "Electricity",
            "Internet"
        ],
    )
    comments = st.text_area("Comments")

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

st.markdown('</div>', unsafe_allow_html=True)


# -------------------------------------------------
# Data & Analytics Section
# -------------------------------------------------
rows = fetch_all()

if rows:
    df = df_from_rows(rows)

    # Ensure date is datetime
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    st.markdown("---")
    st.subheader("📋 All Expenses")

    # ------------------ COLUMN FILTERS ------------------
    st.write("🔍 **Filter your data below:**")
    columns_to_skip = ["id","date","week_in_month","amount"]
    filterable_cols = [c for c in df.columns if c not in columns_to_skip]
    filter_cols = st.columns(len(filterable_cols))

    filters = {}

    for col, ui_col in zip(filterable_cols, filter_cols):
        with ui_col:

            # Numeric filters
            if pd.api.types.is_numeric_dtype(df[col]):
                min_val = float(df[col].min())
                max_val = float(df[col].max())

                if min_val == max_val:
                    st.write(f"{col}: {min_val}")
                    filters[col] = (min_val, max_val)

                else:
                    filters[col] = st.slider(
                        col,
                        min_value=min_val,
                        max_value=max_val,
                        value=(min_val, max_val),
                    )

            # Datetime filters
            elif pd.api.types.is_datetime64_any_dtype(df[col]):
                filters[col] = st.date_input(col)

            # Text / category filters
            else:
                unique = sorted(df[col].dropna().unique())
                filters[col] = st.multiselect(
                    col,
                    options=unique,
                    default=unique  # show ALL by default
                )


    # APPLY FILTERS
    filtered_df = df.copy()

    for col in filterable_cols:

        if pd.api.types.is_numeric_dtype(df[col]):
            filtered_df = filtered_df[
                (filtered_df[col] >= filters[col][0]) &
                (filtered_df[col] <= filters[col][1])
            ] # optional: add date range filtering here
        else:
            filtered_df = filtered_df[filtered_df[col].isin(filters[col])]

    st.dataframe(filtered_df, width="stretch")

    # -------------------------------------------------
    # STACKED ANALYTICS CARDS
    # -------------------------------------------------
    st.markdown("### 📊 Analytics")

    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("📆 Monthly Spend")
        st.bar_chart(monthly_summary(df), x="month", y="amount", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

    with st.container():
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        st.subheader("🏷 Category Spend")
        st.bar_chart(category_summary(df), x="type", y="amount", width="stretch")
        st.markdown('</div>', unsafe_allow_html=True)

else:
    st.info("No expenses yet. Add one above!")
