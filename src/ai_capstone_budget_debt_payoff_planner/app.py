"""
    Main entry point and user interface. Renders UI components, manages user interactions, 
    captures inputs, passes data to database.py, financial_engine.py and llm_service.py
"""

import streamlit as st
import pandas as pd

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
    calculate_strategy
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

################################################################################
#   Main Dashboard Layout
################################################################################

tab_income, tab_expenses, tab_debts = st.tabs(["Income Sources", "Expenses Trackers", "Debt Management"])

#   TAB 1: Income Streams
################################################################################
with tab_income:
    st.subheader("Manage Income Sources")

    col1, col2 = st.columns([1, 2])

    with col1: 
        st.markdown("##### Add New Income")
        with st.form("add_income_form", clear_on_submit=True):
            i_name = st.text_input("Income Name", placeholder="e.g. Work payroll")
            i_amount = st.number_input("Amount ($)", min_value=0.0, value=0.0, step=50.0)
            
            if st.form_submit_button("Add Income"):
                if i_name.strip():
                    add_income(i_name, i_amount)
                    st.success(f"Added {i_name}!")
                    st.rerun()
                else:
                    st.error("Please enter a valid income name.")

    with col2:
        st.markdown("##### Current Income Sources")
        income = show_all_income()
        if income:
            df_income = pd.DataFrame(income)
            st.dataframe(df_income[["id", "name", "amount"]], use_container_width=True, hide_index=True)
            total_income = df_income["amount"].sum()
            st.metric(label='Total income', value=total_income)   

            income_to_delete = st.selectbox("Select income source to remove:", [d["id"] for d in income], format_func=lambda x: f"ID {x}: {next(d['name'] for d in income if d['id']==x)}")
            if st.button("Delete Selected Income Source"):
                delete_income(income_to_delete)
                st.rerun()

#   TAB 2: Expenses Tracker
################################################################################
with tab_expenses:
    st.subheader("Expense tracker")
    expenses = show_all_expenses()

    col1, col2 = st.columns([1, 2])

    with col1:
        #   Add new expense section
        st.markdown('##### Add new expense')
        with st.form("add_expense_form", clear_on_submit=True):
            exp_description = st.text_input("Expense description", placeholder="e.g. Breakfast")
            exp_amount = st.number_input("Amount ($)", min_value=0.0, step=5.0)
            exp_category = st.selectbox("Select category", ('', 'Food', 'Housing', 'Utilities', 'Transportation', 'Entertainment', 'Personal Care', 'Clothing', 'Education', 'Other'))

            if st.form_submit_button("Log Expense"):
                if exp_description.strip():
                    if not exp_category.strip():
                        exp_category = categorize_expense(exp_description) if check_ollama_status() else "Other"
                        # print('Here ', exp_category)
                    add_expense(exp_description, exp_amount, exp_category)
                    st.rerun()
                else:
                    st.error("Please enter a valid expense description.")

        st.markdown("<br>", unsafe_allow_html=True)

        #   Delete logged expense section
        st.markdown('##### Delete logged expense')
        with st.container(border=True):
            expense_to_delete = st.selectbox("Select expense record to remove:", [d["id"] for d in expenses], format_func=lambda x: f"ID {x}: {next(d['description'] for d in expenses if d['id']==x)}")
            if st.button("Delete Selected Expense"):
                delete_expense(expense_to_delete)
                st.rerun()

    with col2:
        st.markdown('##### Expenses Log')
        # expenses = show_all_expenses()
        if expenses:
            df_expenses = pd.DataFrame(expenses)
            st.dataframe(df_expenses[["id", "description", "amount", "category"]], use_container_width=True, hide_index=True)
            #   Calculate total spent
            total_spent = df_expenses['amount'].sum()
            st.metric(label="Total Recorded Expenses", value=f"${total_spent:,.2f}")
            st.divider()
            #   Calculate category total spent
            category_totals = df_expenses.groupby("category")["amount"].sum().reset_index()

            if not category_totals.empty:
                st.markdown("##### Spent by Category")
                cols_per_row = 3
                records = category_totals.to_dict(orient="records")

                for i in range(0, len(records), cols_per_row):
                    row_records = records[i: i + cols_per_row]
                    cols = st.columns(cols_per_row)
                    for idx, record in enumerate(row_records):
                        with cols[idx]:
                            st.metric(
                                label=record["category"], 
                                value=f"${record['amount']:,.2f}"
                            )
                st.markdown("") # Spacing
            st.divider()
        else:
            st.info('No expenses logged yet')


#   TAB 3: Debts tracker
################################################################################
with tab_debts:
    st.subheader("Manage Active Debts")
    debts = show_all_debts()
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("#### Add New Debt")
        with st.form("add_debt_form", clear_on_submit=True):
            d_name = st.text_input("Debt Name", placeholder="e.g. Visa Credit Card")
            d_balance = st.number_input("Current Balance ($)", min_value=0.0, value=1000.0, step=50.0)
            d_apr = st.number_input("APR (%)", min_value=0.0, value=18.5, step=0.1)
            d_min = st.number_input("Minimum Monthly Payment ($)", min_value=0.0, value=35.0, step=5.0)
            
            if st.form_submit_button("Add Debt"):
                if d_name.strip():
                    add_debt(d_name, d_balance, d_apr, d_min)
                    st.success(f"Added {d_name}!")
                    st.rerun()
                else:
                    st.error("Please enter a valid debt name.")

    with col2:
        st.markdown("#### Current Closed Balance Debts")
        # debts = show_all_debts()
        if debts:
            df_debts = pd.DataFrame(debts)
            st.dataframe(df_debts[["id", "name", "balance", "apr", "min_payment"]], use_container_width=True, hide_index=True)
            
            # Simple deletion control
            debt_to_delete = st.selectbox("Select debt to remove:", [d["id"] for d in debts], format_func=lambda x: f"ID {x}: {next(d['name'] for d in debts if d['id']==x)}")
            if st.button("Delete Selected Debt"):
                delete_debt(debt_to_delete)
                st.rerun()
        else:
            st.info("No active debts added yet. Use the form on the left to add your accounts.")


    st.subheader("Debt Pay Off Strategy Analysis")
    extra_budget = st.number_input("Extra monthly budget towards debt ($) ", min_value=0.0, step=10.00)
    if not debts: 
        st.warning('No debts reported')
    else:
        snowball_res = calculate_strategy('Snowball', debts, extra_monthly_budget=extra_budget)
        avalanche_res = calculate_strategy('Avalanche',debts, extra_monthly_budget=extra_budget)

        col_sb, col_av = st.columns(2)
            
        with col_sb:
            st.metric("Snowball Payoff Time", f"{snowball_res['total_months']} Months")
            st.metric("Snowball Total Interest", f"${snowball_res['total_interest_paid']:,.2f}")
        
        with col_av:
            st.metric("Avalanche Payoff Time", f"{avalanche_res['total_months']} Months")
            st.metric("Avalanche Total Interest", f"${avalanche_res['total_interest_paid']:,.2f}")
            
        interest_saved = snowball_res['total_interest_paid'] - avalanche_res['total_interest_paid']
        st.success(f"💡 Choosing the **Avalanche strategy** saves you **${interest_saved:,.2f}** in interest charges!")


        #   Chart Payoff Curves
        st.markdown("### Balance Reduction Over Time")
        df_sb = pd.DataFrame(snowball_res["monthly_history"]).rename(columns={"remaining_balance": "Total Balance"})
        df_av = pd.DataFrame(avalanche_res["monthly_history"]).rename(columns={"remaining_balance": "Total Balance"})
        
        # df_chart = pd.merge(df_sb, df_av, on="month").set_index("month")
        # st.line_chart(df_chart)

        #   Generate AI Strategy Narrative
        st.markdown("### 🤖 AI Financial Mentor Analysis")
        if check_ollama_status():
            with st.spinner("Generating comparative analysis with local Llama 3.2..."):
                summary_narrative = generate_strategy_summary(snowball_res, avalanche_res)
                st.info(summary_narrative)
        else:
            st.caption("Ollama is offline. Start Ollama locally to display AI strategy summaries.")

        #   Monthly payment details
        st.markdown("### Monthly Details")
        col_snow, col_aval = st.columns(2)
        with col_snow:
            st.markdown("#### Snowball method")
            st.dataframe(
                df_sb,
                column_config={
                    "current_month_paid_interest": "Monthly Interest"
                },
                hide_index=True
            )
        with col_aval:
            st.markdown("#### Avalanche method")
            st.dataframe(
                df_av,
                column_config={
                    "current_month_paid_interest": "Monthly Interest"
                },
                hide_index=True
            )