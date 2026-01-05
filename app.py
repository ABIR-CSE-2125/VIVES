import streamlit as st
import pandas as pd

from db import create_table
from utils import load_css
from services.expenses import get_expenses_df
from ui.forms import expense_form
from ui.filters import filter_dataframe
from ui.layout import show_expense_table_with_actions, show_analytics


st.set_page_config(page_title="VIVES", layout="wide")
load_css("style.css")
create_table()

st.title("VIVES")

expense_form()

df = get_expenses_df()

if df is None:
    st.info("No expenses yet. Add one above!")
else:
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")

    st.markdown("---")
    st.subheader("📋 All Expenses")

    filtered_df = filter_dataframe(df)

    show_expense_table_with_actions(filtered_df)

    show_analytics(df)
