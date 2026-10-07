import pytest
import copy

def calculate_monthly_interest(balance, apr):
    """Calculate accrued monthly interest rounded to two decimals"""
    if balance <= 0 or apr == 0:
        return 0
    return round(balance * (apr / 12) / 100, 2)


def calculate_avalanche(debt_list, extra_monthly_budget):
    """
    Calculates timeline to pay off all debts in a closed balance system using avalance method. 
    Paying minimum required amount on all debts and focusing extra monthly budget on smallest interest rate (APR). 
    This method pay debts from lowest balance to highest APR.
    """
    total_months = 0
    total_interest_paid = 0
    monthly_history = []

    # Sort debt list by APR in descending (highest APR -> lowest APR). Use deepcopy to avoid modified data during loop
    avalanche_debt_list = copy.deepcopy(debt_list)
    avalanche_debt_list.sort(key=lambda debt: debt['apr'], reverse=True)

    while any (debt['balance'] > 0 for debt in avalanche_debt_list):
        total_months += 1
        #   Budget available to make extra payment
        current_extra_pool = extra_monthly_budget

        #   Estimate accrue monthly interest on all debts
        for debt in avalanche_debt_list:
            if debt['balance'] > 0:
                interest = calculate_monthly_interest(debt['balance'], debt['apr'])
                debt['balance'] += interest 
                total_interest_paid = round(total_interest_paid + interest, 2)
                # print(debt['name'], interest)
                # print('total interest payment: ', total_interest_paid)

        #   Make minimum payment to all debts
        for debt in avalanche_debt_list:
            if debt['balance'] > 0:
                min_pay = min(debt['balance'], debt['min_payment'])
                debt['balance'] = round(debt['balance'] - min_pay, 2)
            else:
                #   Once debt is paid, its min payment is added to extra budget on the following month
                current_extra_pool += debt['min_payment'] 

        #   Use extra budget pool to pay highest APR debt. Ignores other debts even if there's left over extra budget
        for debt in avalanche_debt_list:
            if debt['balance'] > 0 and current_extra_pool > 0:
                extra_pay = min(debt['balance'], current_extra_pool)
                debt['balance'] -= extra_pay
                #   Remaining extra pool 
                current_extra_pool -= extra_pay 
                break

        remaining_debt_total = 0
        for debt in avalanche_debt_list:
            remaining_debt_total += debt['balance']
            
        monthly_history.append({
            'month': total_months,
            'remaining_balance': round(remaining_debt_total, 2)
        })
    
    return {
        # avalanche_debt_list
        'strategy': 'Avalanche',
        'total_months': total_months,
        'total_interest_paid': total_interest_paid,
        'monthly_history': monthly_history
    }

def calculate_snowball(debt_list, extra_monthly_budget):
    """
        Calculates timeline to pay off all debts in a closed balance system using snowball method. 
        Paying minimum required amount on all debts and focusing extra monthly budget on smallest balance. 
        This method pay debts from lowest balance to highest.
    """

    total_months = 0
    total_interest_paid = 0
    monthly_history = []

    # Sort debt list by BALANCE in ascending (lowest balance -> highest balance). Use deepcopy to avoid modified data during loop
    snowball_debt_list = copy.deepcopy(debt_list)
    snowball_debt_list.sort(key=lambda debt: debt['balance'])

    while any (debt['balance'] > 0 for debt in snowball_debt_list):
        total_months += 1
        #   Budget available to make extra payment
        current_extra_pool = extra_monthly_budget

        #   Estimate accrue monthly interest on all debts
        for debt in snowball_debt_list:
            if debt['balance'] > 0:
                interest = calculate_monthly_interest(debt['balance'], debt['apr'])
                debt['balance'] += interest 
                total_interest_paid = round(total_interest_paid + interest, 2)

        #   Make minimum payment to all debts
        for debt in snowball_debt_list:
            if debt['balance'] > 0:
                min_pay = min(debt['balance'], debt['min_payment'])
                debt['balance'] = round(debt['balance'] - min_pay, 2)
            else:
                #   Once debt is paid, its min payment is added to extra budget on the following month
                current_extra_pool += debt['min_payment'] 

        #   Use extra budget pool to pay highest APR debt. Ignores other debts even if there's left over extra budget
        for debt in snowball_debt_list:
            if debt['balance'] > 0 and current_extra_pool > 0:
                extra_pay = min(debt['balance'], current_extra_pool)
                debt['balance'] -= extra_pay
                #   Remaining extra pool 
                current_extra_pool -= extra_pay 
                break

        remaining_debt_total = 0
        for debt in snowball_debt_list:
            remaining_debt_total += debt['balance']
            
        monthly_history.append({
            'month': total_months,
            'remaining_balance': round(remaining_debt_total, 2)
        })

    return {
        #   snowball_debt_list
        'strategy': 'Snowball',
        'total_months': total_months,
        'total_interest_paid': total_interest_paid,
        'monthly_history': monthly_history
    }