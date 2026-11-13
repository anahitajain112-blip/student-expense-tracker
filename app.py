import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

st.set_page_config(
    page_title="Student Expense Tracker",
    page_icon="💸",
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

CATEGORY_EMOJI = {
    "Food": "🍜",
    "Transport": "🚌",
    "Academic": "📚",
    "Shopping": "🛍️",
    "Entertainment": "🎬",
    "Miscellaneous": "✨"
}

# Custom styling

# Custom styling - Deep Sage & Cream Theme
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F0EFE6;
    color: #263D30;
}

/* Main content */
.main .block-container {
    padding-top: 2rem;
}

/* Main title */
.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #263D30;
    margin-bottom: 0.2rem;
}

/* Subtitle */
.subtitle {
    font-size: 1.05rem;
    color: #596B5D;
    margin-bottom: 1.5rem;
}

/* Dashboard cards */
.metric-card {
    background-color: #FFFFFF;
    padding: 1.3rem;
    border-radius: 18px;
    border: 1px solid #D9DFD2;
    box-shadow: 0 4px 12px rgba(38, 61, 48, 0.09);
    text-align: center;
}

.metric-label {
    font-size: 0.9rem;
    color: #526454;
    margin-bottom: 0.4rem;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 750;
    color: #355C43;
}

/* Section headings */
.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    color: #263D30;
    margin-top: 1.5rem;
    margin-bottom: 0.7rem;
}

/* Expense history */
.history-card {
    background-color: #FFFFFF;
    padding: 1.1rem;
    border-radius: 16px;
    border: 1px solid #D9DFD2;
    box-shadow: 0 3px 10px rgba(38, 61, 48, 0.07);
    color: #263D30;
    margin-bottom: 0.7rem;
}

.history-note {
    color: #596B5D;
    font-size: 0.85rem;
}

/* SIDEBAR - FIXED TEXT VISIBILITY */
section[data-testid="stSidebar"] {
    background-color: #DCE5D8;
}

section[data-testid="stSidebar"] * {
    color: #263D30 !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #263D30 !important;
    font-weight: 750;
}

section[data-testid="stSidebar"] hr {
    border-color: #B7C6B3;
}

/* Input fields */
div[data-baseweb="input"],
div[data-baseweb="select"] {
    border-radius: 10px !important;
}

/* Buttons */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #426B4F;
    color: #FFFFFF !important;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 650;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #2F533B;
    color: #FFFFFF !important;
}

/* Progress bar */
.stProgress > div > div > div > div {
    background-color: #527C5C;
}

/* Chart text and labels */
[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 12px;
    border: 1px solid #D9DFD2;
}

/* Expanders */
.streamlit-expanderHeader {
    color: #263D30 !important;
    font-weight: 650;
}

/* Dataframe */
[data-testid="stDataFrame"] {
    border: 1px solid #D9DFD2;
    border-radius: 12px;
}

/* Captions */
.stCaption {
    color: #526454 !important;
}

</style>
""", unsafe_allow_html=True)

# Initialize expense file
if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "Date", "Category", "Amount", "Note"
    ]).to_csv(CSV_FILE, index=False)

@st.cache_data
def load_expenses():
    return pd.read_csv(CSV_FILE)

def save_expense(new_expense):
    df = load_expenses()
    df = pd.concat([df, pd.DataFrame([new_expense])], ignore_index=True)
    df.to_csv(CSV_FILE, index=False)
    st.cache_data.clear()

# Sidebar
st.sidebar.markdown("## 💸 Expense Tracker")
st.sidebar.write("Keep your monthly spending under control.")

monthly_budget = st.sidebar.number_input(
    "Monthly budget (₹)",
    min_value=0,
    value=8000,
    step=500
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 🎯 Quick Tips")
st.sidebar.markdown(
    "- Add expenses immediately after spending\n"
    "- Keep food and shopping limits realistic\n"
    "- Check your daily limit regularly\n"
    "- Save a small amount every month"
)

# Header
st.markdown('<p class="main-title">💸 Student Expense Tracker</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Track daily expenses, monitor your monthly budget, and spend mindfully.</p>',
    unsafe_allow_html=True
)

# Load expenses
expenses = load_expenses()

total_spent = expenses["Amount"].sum()
remaining = monthly_budget - total_spent

today = date.today()

if today.month == 12:
    next_month = date(today.year + 1, 1, 1)
else:
    next_month = date(today.year, today.month + 1, 1)

days_left = (next_month - today).days

if days_left > 0 and remaining > 0:
    daily_limit = remaining / days_left
else:
    daily_limit = 0

# Dashboard cards
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">Monthly Budget</div>
            <div class="metric-value">₹{monthly_budget:,.0f}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">Total Spent</div>
            <div class="metric-value">₹{total_spent:,.0f}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">Remaining</div>
            <div class="metric-value">₹{remaining:,.0f}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f'''
        <div class="metric-card">
            <div class="metric-label">Daily Limit</div>
            <div class="metric-value">₹{daily_limit:,.0f}</div>
        </div>
        ''',
        unsafe_allow_html=True
    )

# Progress bar
if monthly_budget > 0:
    used_percent = total_spent / monthly_budget
    st.progress(min(used_percent, 1.0))
    st.caption(f"You have used {used_percent * 100:.1f}% of your monthly budget.")

# Alerts
if remaining < 0:
    st.error("⚠️ You have exceeded your monthly budget.")
elif remaining < monthly_budget * 0.10:
    st.warning("⚠️ You are close to your monthly budget limit. Reduce non-essential spending.")
else:
    st.success("✅ You are within your monthly budget.")

# Expense history — moved above Add Expense
st.markdown('<p class="section-title">🧾 Recent Expenses</p>', unsafe_allow_html=True)

if not expenses.empty:
    recent_expenses = expenses.sort_values("Date", ascending=False).head(8)

    for index, row in recent_expenses.iterrows():
        emoji = CATEGORY_EMOJI.get(row["Category"], "💸")

        st.markdown(
    f'''
    <div class="history-card">
        <b>{emoji} {row["Category"]}</b> &nbsp;•&nbsp; ₹{row["Amount"]:,.0f}
        <br>
        <span class="history-note">
            {row["Date"]} {("• " + row["Note"]) if pd.notna(row["Note"]) and row["Note"] != "" else ""}
        </span>
    </div>
    ''',
    unsafe_allow_html=True
        )

    with st.expander("🔍 View full expense history"):
        st.dataframe(
            expenses.sort_values("Date", ascending=False),
            use_container_width=True
        )

        selected_index = st.selectbox(
            "Select expense number to delete",
            expenses.index.tolist()
        )

        if st.button("Delete Selected Expense"):
            expenses = expenses.drop(selected_index)
            expenses.to_csv(CSV_FILE, index=False)
            st.cache_data.clear()
            st.success("Expense deleted successfully.")
            st.rerun()

else:
    st.info("No expenses added yet. Add your first expense below! ✨")

# Add expense
st.markdown('<p class="section-title">➕ Add an Expense</p>', unsafe_allow_html=True)

with st.form("expense_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    expense_date = col1.date_input("Date", value=date.today())
    category = col2.selectbox("Category", CATEGORIES)
    amount = col3.number_input("Amount spent (₹)", min_value=0.0, format="%.2f")

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
            st.success("Expense added successfully! 💜")
            st.rerun()


# Category chart
st.markdown(
    '<p class="section-title">📊 Where Your Money Goes</p>',
    unsafe_allow_html=True
)

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
        title="Total Spending by Category",
        color_discrete_sequence=[
            "#527C5C",
            "#D9A18F",
            "#A8B99F",
            "#E6CBA8",
            "#91A9A0",
            "#B5A6C9"
        ]
    )

    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",

        font=dict(
            color="#263D30",
            family="Arial",
            size=13
        ),

        title=dict(
            font=dict(size=20, color="#263D30")
        ),

        xaxis=dict(
            title="Expense Category",
            title_font=dict(color="#263D30", size=14),
            tickfont=dict(color="#344F3B", size=12),
            showgrid=False
        ),

        yaxis=dict(
            title="Amount (₹)",
            title_font=dict(color="#263D30", size=14),
            tickfont=dict(color="#344F3B", size=12),
            gridcolor="#E5E9DF"
        ),

        legend=dict(
            font=dict(color="#263D30")
        ),

        margin=dict(l=20, r=20, t=65, b=20),
        bargap=0.35
    )

    fig.update_traces(
        marker_line_width=0,
        opacity=0.9
    )

    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("Add expenses to see your spending breakdown.")
