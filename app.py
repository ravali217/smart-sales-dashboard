# app.py
import streamlit as st
import pandas as pd
from services import list_products, get_sales_report

st.set_page_config(page_title="📈 Smart Sales Dashboard", layout="wide")

st.title("📈 Smart Sales Dashboard")

# ========== PRODUCTS SECTION ==========
st.subheader("🛍️ Product List")
products = list_products()

if products:
    df_products = pd.DataFrame(products)
    st.dataframe(df_products)
else:
    st.warning("No products found in the database.")

# ========== SALES REPORT SECTION ==========
st.subheader("📊 Sales Report")
sales_data = get_sales_report()

if sales_data:
    df_sales = pd.DataFrame(sales_data)
    st.dataframe(df_sales)
else:
    st.info("No sales data available yet.")
