import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Zeeshan's Financial Dashboard", layout="wide"
)

st.title("📊 Zeeshan's Live Financial Dashboard (October 2026)")
st.markdown("Automated tracking for Operational, Rental, and Capital accounts.")

# For now, this connects to a sample view. We will link your Google Sheet next!
data = {
    "Date": ["2026-10-01", "2026-10-06", "2026-10-20", "2026-10-20"],
    "Type": ["Expense", "Income", "Income", "Income"],
    "Description": [
        "Foodpanda",
        "NGTSOL Salary",
        "Zeeshan Tailor (Shop 1 Rent)",
        "581 D House Rent",
    ],
    "Category": [
        "Food & Dining",
        "Salary / Business",
        "Rental Income",
        "Rental Income",
    ],
    "Amount (PKR)": [2079.99, 287894.00, 90000.00, 125000.00],
    "Source": ["HBL CC", "UBL", "JazzCash", "HBL Account"],
}

df = pd.DataFrame(data)

# Top Metrics Row
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Incomes", "Rs 885,270.00")
with col2:
    st.metric("Operational Expenses", "Rs 717,379.41")
with col3:
    st.metric("Capital Assets (Land)", "Rs 12,504,748.80", "ShareefPura")

st.divider()

# Tables and Views
st.subheader("Master Transaction Ledger")
st.dataframe(df, use_container_width=True)
