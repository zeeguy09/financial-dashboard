import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Zeeshan's Financial Dashboard",
    layout="wide",
    page_icon="📊",
)


# --- PASSWORD PROTECTION SETUP ---
def check_password():
  """Returns `True` if the user had the correct password."""

  def password_entered():
    if st.session_state["password"] == "Z33shan@2O26":  # You can change this password anytime!
      st.session_state["password_correct"] = True
      del st.session_state["password"]  # don't store password
    else:
      st.session_state["password_correct"] = False

  if "password_correct" not in st.session_state:
    # First run, show input for password
    st.markdown("## 🔒 Secure Login Required")
    st.text_input(
        "Enter Dashboard Password",
        type="password",
        on_change=password_entered,
        key="password",
    )
    return False
  elif not st.session_state["password_correct"]:
    # Password incorrect, show input + error
    st.markdown("## 🔒 Secure Login Required")
    st.text_input(
        "Enter Dashboard Password",
        type="password",
        on_change=password_entered,
        key="password",
    )
    st.error("😕 Password incorrect")
    return False
  else:
    # Password correct
    return True


if not check_password():
  st.stop()  # Do not render dashboard if not logged in

# --- DASHBOARD CONTENT ---
st.title("📊 Zeeshan's Live Financial Dashboard (October 2026)")
st.markdown("Secure operational, rental, and capital accounts ledger.")

# --- CONNECT TO GOOGLE SHEET ---
sheet_url = "https://docs.google.com/spreadsheets/d/1CnyHjNVKo37030KzDDBEBPfpOUqF0bVnkKeoYyViKJU/edit?usp=sharing"
csv_url = sheet_url.replace("/edit?usp=sharing", "/export?format=csv")


@st.cache_data(ttl=60)
def load_data(url):
  return pd.read_csv(url)


try:
  df = load_data(csv_url)

  # Clean amount column
  if "Amount (PKR)" in df.columns:
    df["Amount (PKR)"] = (
        df["Amount (PKR)"]
        .astype(str)
        .str.replace(",", "")
        .astype(float, errors="ignore")
    )

  # --- TOP METRICS ---
  col1, col2, col3 = st.columns(3)
  with col1:
    st.metric("Total Incomes", "Rs 885,270.00")
  with col2:
    st.metric("Operational Expenses", "Rs 758,261.39")
  with col3:
    st.metric("Capital Assets (Land)", "Rs 12,504,748.80", "ShareefPura")

  st.divider()

  # --- TABS FOR SEPARATION & CHARTS ---
  tab1, tab2, tab3, tab4 = st.tabs([
      "Master Ledger",
      "📊 Expense & Earning Analytics",
      "Property Rentals",
      "Capital & Perks (NGTSOL)",
  ])

  with tab1:
    st.subheader("All Logged Transactions & Itemized Details")
    st.dataframe(df, use_container_width=True)

  with tab2:
    st.subheader("📈 Visual Financial Breakdown")

    # Separate Expenses and Incomes
    expenses_df = df[df["Type"].str.contains("Expense", case=False, na=False)]
    incomes_df = df[df["Type"].str.contains("Income", case=False, na=False)]

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
      st.markdown("### 💸 Expense Breakdown by Category")
      if not expenses_df.empty and "Category" in expenses_df.columns:
        cat_exp = (
            expenses_df.groupby("Category")["Amount (PKR)"].sum().reset_index()
        )
        st.bar_chart(cat_exp.set_index("Category"))
      else:
        st.info("No expense data available for charts.")

    with col_chart2:
      st.markdown("### 💰 Earnings / Incomes Breakdown")
      if not incomes_df.empty and "Category" in incomes_df.columns:
        cat_inc = (
            incomes_df.groupby("Category")["Amount (PKR)"].sum().reset_index()
        )
        st.bar_chart(cat_inc.set_index("Category"))
      else:
        st.info("No income data available for charts.")

    st.markdown("### 🏦 Spending by Payment Source")
    if not expenses_df.empty and "Source" in expenses_df.columns:
      source_exp = (
          expenses_df.groupby("Source")["Amount (PKR)"].sum().reset_index()
      )
      st.bar_chart(source_exp.set_index("Source"))

  with tab3:
    st.subheader("Rental Incomes")
    if "Category" in df.columns:
      rent_df = df[df["Category"].str.contains("Rental", case=False, na=False)]
      st.dataframe(rent_df, use_container_width=True)

  with tab4:
    st.subheader("Special Assets & Perks")
    st.info(
        "Land Purchase: 4 Acres in ShareefPura Near Kala Khatai Road (~Rs 12.5M"
        " Alfalah Payorders)"
    )
    st.info("Fuel Perks: Total Infini Cards managed via NGTSOL.")

except Exception as e:
  st.error(f"Could not load data from Google Sheet. Error: {e}")
