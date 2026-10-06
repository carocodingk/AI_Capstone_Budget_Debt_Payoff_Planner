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


