
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

# ==========================================
# PAGE CONFIGURATION
# ==========================================

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


# ==========================================
# CUSTOM STYLING - SAGE & CREAM THEME
# ==========================================

st.markdown("""
<style>

/* MAIN WEBSITE */
.stApp {
    background-color: #ECECE2;
    color: #263D30;
}

.main .block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* MAIN TITLE */
.main-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #263D30;
    margin-bottom: 0.2rem;
}

.subtitle {
    font-size: 1.05rem;
    color: #526454;
    margin-bottom: 1.5rem;
}

/* SECTION HEADINGS */
.section-title {
    font-size: 1.35rem;
    font-weight: 750;
    color: #263D30;
    margin-top: 1.5rem;
    margin-bottom: 0.7rem;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #D6E0D2;
}

section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h1,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h2,
section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] h3,
section[data-testid="stSidebar"] label {
    color: #263D30 !important;
}

section[data-testid="stSidebar"] hr {
    border-color: #AABBA7;
}

/* ALL INPUT LABELS */
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] p,
.stTextInput label,
.stNumberInput label,
.stSelectbox label,
.stDateInput label {
    color: #263D30 !important;
    font-weight: 700 !important;
}

/* INPUT BOXES */
div[data-baseweb="input"],
div[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #B7C7B3 !important;
    border-radius: 10px !important;
}

input,
textarea {
    color: #263D30 !important;
    -webkit-text-fill-color: #263D30 !important;
    background-color: #FFFFFF !important;
    font-weight: 600 !important;
}

input::placeholder,
textarea::placeholder {
    color: #7A897B !important;
    -webkit-text-fill-color: #7A897B !important;
}

/* NUMBER INPUTS */
.stNumberInput button {
    background-color: #DCE5D8 !important;
    color: #263D30 !important;
    border-color: #B7C7B3 !important;
}

/* DROPDOWNS */
div[data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-color: #B7C7B3 !important;
}

div[data-baseweb="select"] span {
    color: #263D30 !important;
}

div[role="listbox"],
div[role="option"] {
    background-color: #FFFFFF !important;
    color: #263D30 !important;
}

div[role="option"] * {
    color: #263D30 !important;
}

/* DATE PICKER */
div[data-baseweb="datepicker"] {
    background-color: #FFFFFF !important;
}

div[data-baseweb="calendar"] {
    background-color: #FFFFFF !important;
    color: #263D30 !important;
}

/* FORM */
[data-testid="stForm"] {
    background-color: #E0E5D9;
    padding: 22px;
    border-radius: 18px;
    border: 1px solid #C7D2C3;
}

/* DASHBOARD CARDS */
.metric-card {
    background-color: #FFFFFF;
    padding: 1.3rem;
    border-radius: 18px;
    border: 1px solid #D5DDD0;
    box-shadow: 0 4px 14px rgba(38, 61, 48, 0.09);
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

/* EXPENSE HISTORY */
.history-card {
    background-color: #FFFFFF;
    padding: 1.1rem;
    border-radius: 16px;
    border: 1px solid #D5DDD0;
    box-shadow: 0 3px 10px rgba(38, 61, 48, 0.07);
    color: #263D30;
    margin-bottom: 0.7rem;
}

.history-note {
    color: #526454;
    font-size: 0.85rem;
}

/* BUTTONS */
.stButton > button,
.stFormSubmitButton > button {
    background-color: #426B4F !important;
    color: #FFFFFF !important;
    border-radius: 12px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 650;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover {
    background-color: #2F533B !important;
    color: #FFFFFF !important;
}

/* PROGRESS BAR */
.stProgress > div > div > div > div {
    background-color: #527C5C;
}

/* CHART CONTAINER */
[data-testid="stPlotlyChart"] {
    background-color: #FFFFFF;
    border-radius: 16px;
    padding: 12px;
    border: 1px solid #D5DDD0;
}

/* EXPANDER */
[data-testid="stExpander"] {
    border-color: #C7D2C3;
}

[data-testid="stExpander"] summary {
    color: #263D30 !important;
    font-weight: 650;
}

/* DATAFRAME */
[data-testid="stDataFrame"] {
    border: 1px solid #D5DDD0;
    border-radius: 12px;
}

/* CAPTIONS */
[data-testid="stCaptionContainer"] {
    color: #526454 !important;
}

/* GENERAL TEXT */
.stApp p {
    color: #34483B;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# INITIALIZE EXPENSE FILE
# ==========================================

if not os.path.exists(CSV_FILE):
    pd.DataFrame(columns=[
        "Date", "Category", "Amount", "Note"
    ]).to_csv(CSV_FILE, index=False)


@st.cache_data
def load_expenses():
    return pd.read_csv(CSV_FILE)


def save_expense(new_expense):
    df = load_expenses()

    df = pd.concat(
        [df, pd.DataFrame([new_expense])],
        ignore_index=True
    )

    df.to_csv(CSV_FILE, index=False)
    st.cache_data.clear()


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.markdown("## 💸 Expense Tracker")

st.sidebar.write(
    "Keep your monthly spending under control."
)

monthly_budget = st.sidebar.number_input(
    "Monthly budget (₹)",
    min_value=0,
    value=8000,
    step=500
)

st.sidebar.markdown("---")

st.sidebar.markdown("### 🎯 Quick Tips")

st.sidebar.markdown(
    """
    - Add expenses immediately after spending
    - Keep food and shopping limits realistic
    - Check your daily limit regularly
    - Save a small amount every month
    """
)


# ==========================================
# HEADER
# ==========================================

st.markdown(
    '<p class="main-title">💸 Student Expense Tracker</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Track daily expenses, monitor your monthly budget, and spend mindfully.</p>',
    unsafe_allow_html=True
)


# ==========================================
# LOAD EXPENSES
# ==========================================

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


# ==========================================
# DASHBOARD CARDS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Monthly Budget</div>
            <div class="metric-value">₹{monthly_budget:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Total Spent</div>
            <div class="metric-value">₹{total_spent:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Remaining</div>
            <div class="metric-value">₹{remaining:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">Daily Limit</div>
            <div class="metric-value">₹{daily_limit:,.0f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================
# BUDGET PROGRESS
# ==========================================

if monthly_budget > 0:

    used_percent = total_spent / monthly_budget

    st.progress(min(used_percent, 1.0))

    st.caption(
        f"You have used {used_percent * 100:.1f}% of your monthly budget."
    )


# ==========================================
# BUDGET ALERTS
# ==========================================

if remaining < 0:

    st.error("⚠️ You have exceeded your monthly budget.")

elif remaining < monthly_budget * 0.10:

    st.warning(
        "⚠️ You are close to your monthly budget limit. Reduce non-essential spending."
    )

else:

    st.success(
        "✅ You are within your monthly budget."
    )


# ==========================================
# RECENT EXPENSES
# ==========================================

st.markdown(
    '<p class="section-title">🧾 Recent Expenses</p>',
    unsafe_allow_html=True
)

if not expenses.empty:

    recent_expenses = expenses.sort_values(
        "Date",
        ascending=False
    ).head(8)

    for index, row in recent_expenses.iterrows():

        emoji = CATEGORY_EMOJI.get(
            row["Category"],
            "💸"
        )

        note_text = (
            "• " + str(row["Note"])
            if pd.notna(row["Note"]) and row["Note"] != ""
            else ""
        )

        st.markdown(
            f"""
            <div class="history-card">
                <b>{emoji} {row["Category"]}</b>
                &nbsp;•&nbsp; ₹{row["Amount"]:,.0f}
                <br>
                <span class="history-note">
                    {row["Date"]} {note_text}
                </span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander("🔍 View full expense history"):

        st.dataframe(
            expenses.sort_values(
                "Date",
                ascending=False
            ),
            use_container_width=True
        )

        selected_index = st.selectbox(
            "Select expense number to delete",
            expenses.index.tolist()
        )

        if st.button("Delete Selected Expense"):

            expenses = expenses.drop(selected_index)

            expenses.to_csv(
                CSV_FILE,
                index=False
            )

            st.cache_data.clear()

            st.success("Expense deleted successfully.")

            st.rerun()

else:

    st.info(
        "No expenses added yet. Add your first expense below! ✨"
    )


# ==========================================
# ADD EXPENSE
# ==========================================

st.markdown(
    '<p class="section-title">➕ Add an Expense</p>',
    unsafe_allow_html=True
)

with st.form("expense_form", clear_on_submit=True):

    col1, col2, col3 = st.columns(3)

    expense_date = col1.date_input(
        "Date",
        value=date.today()
    )

    category = col2.selectbox(
        "Category",
        CATEGORIES
    )

    amount = col3.number_input(
        "Amount spent (₹)",
        min_value=0.0,
        format="%.2f"
    )

    note = st.text_input(
        "Note (optional)"
    )

    submitted = st.form_submit_button(
        "Add Expense"
    )

    if submitted:

        if amount <= 0:

            st.error(
                "Please enter an amount greater than 0."
            )

        else:

            save_expense({
                "Date": expense_date.strftime("%Y-%m-%d"),
                "Category": category,
                "Amount": amount,
                "Note": note
            })

            st.success(
                "Expense added successfully! 🌿"
            )

            st.rerun()


# ==========================================
# CATEGORY SPENDING CHART
# ==========================================

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
            font=dict(
                size=20,
                color="#263D30"
            )
        ),

        xaxis=dict(
            title="Expense Category",
            title_font=dict(
                color="#263D30",
                size=14
            ),
            tickfont=dict(
                color="#344F3B",
                size=12
            ),
            showgrid=False
        ),

        yaxis=dict(
            title="Amount (₹)",
            title_font=dict(
                color="#263D30",
                size=14
            ),
            tickfont=dict(
                color="#344F3B",
                size=12
            ),
            gridcolor="#E5E9DF"
        ),

        legend=dict(
            font=dict(
                color="#263D30"
            )
        ),

        margin=dict(
            l=20,
            r=20,
            t=65,
            b=20
        ),

        bargap=0.35
    )

    fig.update_traces(
        marker_line_width=0,
        opacity=0.9
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info(
        "Add expenses to see your spending breakdown."
    )
