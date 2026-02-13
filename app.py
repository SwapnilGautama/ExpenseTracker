import streamlit as st
import json
import os
from datetime import datetime

# ----------------------------------------
# File Configuration
# ----------------------------------------
DATA_FILE = "expense_data.json"

# ----------------------------------------
# Load Data
# ----------------------------------------
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"expenses": [], "monthly_budget": 0}

# ----------------------------------------
# Save Data
# ----------------------------------------
def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ----------------------------------------
# Initialize Data
# ----------------------------------------
if "data" not in st.session_state:
    st.session_state.data = load_data()

data = st.session_state.data

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰")

st.title("💰 Personal Expense Tracker")
st.write(
    "Log daily expenses, categorize them, and track spending against your monthly budget."
)

# ----------------------------------------
# Sidebar - Budget Section
# ----------------------------------------
st.sidebar.header("📊 Monthly Budget")

budget_input = st.sidebar.number_input(
    "Set Monthly Budget (₹)",
    min_value=0.0,
    value=float(data["monthly_budget"]),
    step=100.0
)

if st.sidebar.button("Save Budget"):
    data["monthly_budget"] = budget_input
    save_data(data)
    st.sidebar.success("Budget saved!")

# ----------------------------------------
# Add Expense Section
# ----------------------------------------
st.header("➕ Add Expense")

with st.form("expense_form"):
    date = st.date_input("Date", datetime.today())
    description = st.text_input("Description")
    category = st.selectbox(
        "Category",
        ["Food", "Travel", "Rent", "Shopping", "Utilities", "Entertainment", "Health", "Other"]
    )
    amount = st.number_input("Amount (₹)", min_value=0.0, step=10.0)

    submit = st.form_submit_button("Add Expense")

    if submit:
        if description.strip() == "":
            st.error("Description cannot be empty.")
        else:
            new_expense = {
                "date": date.strftime("%Y-%m-%d"),
                "description": description,
                "category": category,
                "amount": amount
            }
            data["expenses"].append(new_expense)
            save_data(data)
            st.success("Expense added successfully!")

# ----------------------------------------
# View Expenses
# ----------------------------------------
st.header("📋 Expense History")

if not data["expenses"]:
    st.info("No expenses recorded yet.")
else:
    st.dataframe(data["expenses"])

# ----------------------------------------
# Category Summary
# ----------------------------------------
st.header("📂 Category Summary")

category_totals = {}

for expense in data["expenses"]:
    category_totals[expense["category"]] = (
        category_totals.get(expense["category"], 0) + expense["amount"]
    )

if category_totals:
    st.bar_chart(category_totals)
else:
    st.info("No data available.")

# ----------------------------------------
# Budget Status
# ----------------------------------------
st.header("📉 Budget Status")

total_spent = sum(exp["amount"] for exp in data["expenses"])
remaining = data["monthly_budget"] - total_spent

st.write(f"**Monthly Budget:** ₹{data['monthly_budget']}")
st.write(f"**Total Spent:** ₹{total_spent}")
st.write(f"**Remaining:** ₹{remaining}")

if remaining < 0:
    st.error("⚠️ You have exceeded your budget!")
else:
    st.success("You are within your budget.")
