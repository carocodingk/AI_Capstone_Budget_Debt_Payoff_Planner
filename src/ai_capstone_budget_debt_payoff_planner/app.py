"""
    Main entry point and user interface. Renders UI components, manages user interactions, 
    captures inputs, passes data to database.py, financial_engine.py and llm_service.py
"""

import streamlit as st
from ai_capstone_budget_debt_payoff_planner.database import (
    init_db,
    add_income,
    show_all_income, 
    delete_income,
    add_expense,
    show_all_expenses,
    delete_expense,
    add_debt,
    show_all_debts,
    delete_debt
)

from ai_capstone_budget_debt_payoff_planner.financial_engine import (
    Debt,
    # collect_debt_details,
    calculate_avalanche, 
    calculate_snowball
)

from ai_capstone_budget_debt_payoff_planner.llm_service import (
    check_ollama_status,
    categorize_expense,
    generate_strategy_summary
)

################################################################################
#   Page configuration and Database initialization
################################################################################
st.set_page_config(
    page_title="AI Budget & Debt Payoff Planner",
    page_icon=None,
    layout="wide",
)

#   Initialize database
init_db()

st.title("💰 AI Budget & Debt Payoff Planner")
st.caption("Privacy-First Local Personal Finance Assistant | Powered by Ollama")
st.warning("""IMPORTANT: Development and use of this application is for educational purposes only. 
    This application does NOT provide professional financial, legal, tax or investment advice.""")

#   Check Ollama connection 
if not check_ollama_status():
    st.warning("Local Ollama Server is offline. Expense classification and Debt strategy summary are unavailable")

st.divider()