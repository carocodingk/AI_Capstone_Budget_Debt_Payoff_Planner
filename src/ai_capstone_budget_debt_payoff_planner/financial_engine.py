import pytest
import copy

def calculate_monthly_interest(balance, apr):
    """Calculate accrued monthly interest rounded to two decimals"""
    if balance <= 0 or apr == 0:
        return 0
    return round(balance * (apr / 12) / 100, 2)

def calculate_strategy(strategy, debt_list, extra_monthly_budget):
    """
        Calculates timeline to pay off all debts in a closed balance system using avalance and snowball method. 
        *   Avalanche method: Paying minimum required amount on all debts and focusing extra monthly budget on debts 
        with highest interest rate (APR). This method pays debts from highest APR to lowest.
        *   Snowball method: Paying minimum required amount on all debts and focusing extra monthly budget on debts with lowest balance.  
    """
    total_months = 0
    total_interest_paid = 0
    monthly_history = []

    # Sort debt list by APR in descending (highest APR -> lowest APR). Use deepcopy to avoid modified data during loop
    strategy_debt_list = copy.deepcopy(debt_list)
    if strategy == 'Snowball':
        strategy_debt_list.sort(key=lambda debt: debt['balance'])
    elif strategy == 'Avalanche':
        strategy_debt_list.sort(key=lambda debt: debt['apr'], reverse=True)
    # print(strategy.upper())

    #   One loop per month 
    while any (debt['balance'] > 0 for debt in strategy_debt_list):
        total_months += 1
        current_month_interest = 0
        
        monthly_history.append({
            'month': total_months
        })
        # print('here ', monthly_history[total_months-1])

        #   Budget available to make extra payment
        current_extra_pool = extra_monthly_budget

        # FIX: Establish a clean baseline monthly budget
        # current_extra_pool = extra_monthly_budget

        #   Establish a clean baseline monthly budget
        for debt in strategy_debt_list:
            if debt['balance'] <= 0:
                # If a debt was cleared in a previous month, its min payment permanently rolls into the extra pool
                current_extra_pool += debt['min_payment']

        #   Estimate accrue monthly interest on all debts
        for debt in strategy_debt_list:
            if debt['balance'] > 0:
                # interest = calculate_monthly_interest(debt['balance'], debt['apr'])
                # debt['balance'] = round(debt['balance'] + interest, 2)  
                # total_interest_paid = round(total_interest_paid + interest, 2)
                interest = calculate_monthly_interest(debt['balance'], debt['apr'])
                current_month_interest += interest
                debt['balance'] = round(debt['balance'] + interest, 2)  
                total_interest_paid = round(total_interest_paid + interest, 2)

        for debt in strategy_debt_list:
            if debt['balance'] > 0:
                #   Estimate minimum payment. If remaining balance < min payment -> Pay remaining balance
                min_pay = min(debt['balance'], debt['min_payment'])
                #   Update balance after minimum payment
                debt['balance'] = round(debt['balance'] - min_pay, 2)

                #If debt is paid off by its minimum payment, any leftover from that minimum payment goes into current month extra pay
                if debt['balance'] == 0:
                    current_extra_pool += (debt['min_payment'] - min_pay)

        #   Use extra budget pool to pay highest APR debt. Ignores other debts even if there's left over extra budget
        for debt in strategy_debt_list:
            if debt['balance'] > 0 and current_extra_pool > 0:
                #   Estimate extra payment amount. Total current_extra_payment or remaining balance  if it's less than current_extra_pool
                extra_pay = min(debt['balance'], current_extra_pool)
                #   Update balance after extra payment
                debt['balance'] = round(debt['balance'] - extra_pay, 2)
                #   Remaining extra pool 
                current_extra_pool = round(current_extra_pool - extra_pay, 2)
                #   Ran out of money for extra payments - No need to look at the other debts
                if current_extra_pool <= 0:
                    break

        #   Update remaining total debt balance after current month payment
        remaining_debt_total = 0
        for debt in strategy_debt_list:
            remaining_debt_total += debt['balance']
            
        # monthly_history[total_months] ={
        #     # 'month': total_months,
        #     'remaining_balance': round(remaining_debt_total, 2)
        # }
        # monthly_history[total_months-1]['remaining_balance'] = round(remaining_debt_total, 2)
        monthly_history[total_months-1]['remaining_balance'] = round(remaining_debt_total, 2)
        monthly_history[total_months-1]['current_month_paid_interest'] = round(current_month_interest, 2)

        print(monthly_history[total_months-1])

    #####
    # for i in monthly_history:
    #     print(i)    
    # print(monthly_history)
    # print(type(monthly_history))
    return {
        'strategy': strategy,
        'total_months': total_months,
        'total_interest_paid': total_interest_paid,
        'monthly_history': monthly_history
    }