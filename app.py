import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💰",
    layout="wide"
)

CSV_FILE = "expenses.csv"

CATEGORIES = [
    "Food",
    "Transport",
    "Academic",
    "Shopping",
    "Entertainment",
    "Miscellaneous"
]

# Initialize expense file
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "Date", "Category", "Amount", "Note"
    ]).to_csv(CSV_FILE, index=False)

# Load expenses
@st.cache_data
def load_expenses():
    return pd.read_csv(CSV_FILE)

def save_expense(new_expense):
    df = load_expenses()
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.cache_data.clear()

# Sidebar: monthly budget
st.sidebar.title("💰 Student Expense Tracker")

if "monthly_budget" not in st.session_state:
    st.session_state.monthly_budget = 8000

monthly_budget = st.sidebar.number_input(
    "Monthly budget (₹)",
    min_value=0,
    value=st.session_state.monthly_budget,
    step=500
)

st.session_state.monthly_budget = monthly_budget

# Main title
st.title("💰 Student Expense Tracker")
st.write("Track your daily expenses and stay within your monthly budget.")

# Add expense form
st.subheader("➕ Add Today's Expense")

with st.form("expense_form", clear_on_submit=True):
    col1, col2 = st.columns(2)

    expense_date = col1.date_input("Date", value=date.today())
    category = col2.selectbox("Category", CATEGORIES)

    amount = st.number_input(
        "Amount spent (₹)",
        min_value=0.0,
        format="%.2f"
    )

    note = st.text_input("Note (optional)")

    submitted = st.form_submit_button("Add Expense")

    if submitted:
        if amount <= 0:
            st.error("Please enter an amount greater than 0.")
        else:
            save_expense({
                "Date": expense_date.strftime("%Y-%m-%d"),
                "Category": category,
                "Amount": amount,
                "Note": note
            })
            st.success("Expense added successfully!")

# Load expenses
expenses = load_expenses()

# Calculate totals
total_spent = expenses["Amount"].sum()
remaining = monthly_budget - total_spent

today = date.today()

# Days left in current month
if today.month == 12:
    next_month = date(today.year + 1, 1, 1)
else:
    next_month = date(today.year, today.month + 1, 1)

days_left = (next_month - today).days

# Daily limit
if days_left > 0 and remaining > 0:
    daily_limit = remaining / days_left
else:
    daily_limit = 0

# Dashboard metrics
st.subheader("📊 Monthly Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Monthly Budget", f"₹{monthly_budget:,.0f}")
col2.metric("Total Spent", f"₹{total_spent:,.0f}")
col3.metric("Remaining", f"₹{remaining:,.0f}")
col4.metric("Daily Limit", f"₹{daily_limit:,.0f}")

# Budget progress
if monthly_budget > 0:
    used_percent = total_spent / monthly_budget
    st.progress(min(used_percent, 1.0))
    st.write(f"You have used **{used_percent * 100:.1f}%** of your monthly budget.")

# Alerts
if remaining < 0:
    st.error("⚠️ You have exceeded your monthly budget.")
elif remaining < monthly_budget * 0.10:
    st.warning("⚠️ You are close to your monthly budget limit. Reduce non-essential spending.")
else:
    st.success("✅ You are within your monthly budget.")

# Category chart
st.subheader("📌 Spending by Category")

if not expenses.empty:
    category_totals = (
        expenses.groupby("Category")["Amount"]
        .sum()
        .reset_index()
    )

    fig = px.bar(
        category_totals,
        x="Category",
        y="Amount",
        color="Category",
        title="Total Spending by Category"
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No expenses added yet. Add your first expense above.")

# Expense history
st.subheader("🧾 Expense History")

if not expenses.empty:
    st.dataframe(
        expenses.sort_values("Date", ascending=False),
        use_container_width=True
    )

    # Delete expense
    st.write("### Delete an Expense")

    expense_options = expenses.index.tolist()

    selected_index = st.selectbox(
        "Select expense number to delete",
        expense_options
    )

    if st.button("Delete Selected Expense"):
        expenses = expenses.drop(selected_index)
        expenses.to_csv(CSV_FILE, index=False)
        st.cache_data.clear()
        st.success("Expense deleted successfully.")
        st.rerun()
else:
    st.info("Your expense history is empty.")
