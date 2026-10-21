import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Zeeshan's Financial Dashboard", layout="wide"
)

st.title("📊 Zeeshan's Live Financial Dashboard (October 2026)")
st.markdown("Live operational, rental, and capital accounts ledger.")

# --- CONNECT TO GOOGLE SHEET ---
sheet_url = "YOUR_GOOGLE_SHEET_URL_HERE"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")


@st.cache_data(ttl=60)
def load_data(url):
  return pd.read_csv(url)


try:
  df = load_data(csv_url)

  # --- TOP METRICS ---
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric("Total Incomes", "Rs 885,270.00")
  with col2:
    st.metric("Operational Expenses", "Rs 721,598.90")
  with col3:
    st.metric("Capital Assets (Land)", "Rs 12,504,748.80", "ShareefPura")

  st.divider()

  # --- TABS FOR SEPARATION ---
  tab1, tab2, tab3 = st.tabs(
      ["Master Ledger", "Property Rentals", "Capital & Perks (NGTSOL)"]
  )

  with tab1:
    st.subheader("All Logged Transactions & Itemized Details")
    st.dataframe(df, use_container_width=True)

  with tab2:
    st.subheader("Rental Incomes")
    if "Category" in df.columns:
      rent_df = df[df["Category"].str.contains("Rental", case=False, na=False)]
      st.dataframe(rent_df, use_container_width=True)

  with tab3:
    st.subheader("Special Assets & Perks")
    st.info(
        "Land Purchase: 4 Acres in ShareefPura Near Kala Khatai Road (~Rs 12.5M"
        " Alfalah Payorders)"
    )
    st.info("Fuel Perks: Total Infini Cards managed via NGTSOL.")

except Exception as e:
  st.error(f"Could not load data from Google Sheet. Error: {e}")
