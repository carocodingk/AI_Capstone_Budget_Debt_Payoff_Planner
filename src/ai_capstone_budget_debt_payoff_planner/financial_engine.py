import pytest

class Debt:
    def __init__(self, name, balance, apr, min_payment):
        self.name = name
        self.balance = balance
        self.apr = apr
        self.min_payment = min_payment


def collect_debt_details():
    """Collects details (name, current balance, APR and type) about user's debts"""
    name = input('Enter account name: ')
    # type = input('Enter debt type: ')
    balance = input('Enter balance owed: ')
    apr = input('Enter debt APR: ')
    min_payment = input('Enter minimum payment: ')
    debt = Debt(name, balance, apr, min_payment)
    return debt

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

    # Sort debt list by APR in descending (highest APR -> lowest APR)
    avalanche_debt_list = sorted(debt_list, key=lambda debt: debt.apr, reverse=True)
    # print('here: ', avalanche_debt_list)

    for d in avalanche_debt_list:
        print('hello ', [d.name, d.balance, d.apr, d.min_payment])

    while any (debt.balance > 0 for debt in avalanche_debt_list):
        total_months += 1
        #   Budget available to make extra payment
        current_extra_pool = extra_monthly_budget

        #   Estimate accrue monthly interest on all debts
        for debt in avalanche_debt_list:
            if debt.balance > 0:
                interest = calculate_monthly_interest(debt.balance, debt.apr)
                debt.balance += interest 
                total_interest_paid = round(total_interest_paid + interest, 2)
                print(debt.name, interest)
                # print('total interest payment: ', total_interest_paid)

        #   Make minimum payment to all debts
        for debt in avalanche_debt_list:
            if debt.balance > 0:
                min_pay = min(debt.balance, debt.min_payment)
                print('debt before minimum ', debt.balance)
                debt.balance = round(debt.balance - min_pay, 2)
                print('debt balance after minimum: ', debt.balance)
            else:
                #   Once debt is paid, its min payment is added to extra budget on the following month
                current_extra_pool += debt.min_payment 
                print('DEBT IS PAID OFF')
                print('extra pool: ', current_extra_pool)

        #   Use extra budget pool to pay highest APR debt. Ignores other debts even if there's left over extra budget
        for debt in avalanche_debt_list:
            if debt.balance > 0 and current_extra_pool > 0:
                extra_pay = min(debt.balance, current_extra_pool)
                debt.balance -= extra_pay
                #   Remaining extra pool 
                current_extra_pool -= extra_pay 
                print('extraaaaaa ', debt.balance)
                break

        remaining_debt_total = 0
        for debt in avalanche_debt_list:
            remaining_debt_total += debt.balance
            
        monthly_history.append({
            'month': total_months,
            'remaining_balance': remaining_debt_total
        })

    # print(monthly_history)
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

    # Sort debt list by BALANCE in ascending (lowest balance -> highest balance)
    snowball_debt_list = sorted(debt_list, key=lambda debt: debt.balance)
    # print('here: ', avalanche_debt_list)

    for d in snowball_debt_list:
        print('hello ', [d.name, d.balance, d.apr, d.min_payment])

    while any (debt.balance > 0 for debt in snowball_debt_list):
        total_months += 1
        #   Budget available to make extra payment
        current_extra_pool = extra_monthly_budget

        #   Estimate accrue monthly interest on all debts
        for debt in snowball_debt_list:
            if debt.balance > 0:
                interest = calculate_monthly_interest(debt.balance, debt.apr)
                debt.balance += interest 
                total_interest_paid = round(total_interest_paid + interest, 2)
                print(debt.name, interest)
                # print('total interest payment: ', total_interest_paid)

        #   Make minimum payment to all debts
        for debt in snowball_debt_list:
            if debt.balance > 0:
                min_pay = min(debt.balance, debt.min_payment)
                print('debt before minimum ', debt.balance)
                debt.balance = round(debt.balance - min_pay, 2)
                print('debt balance after minimum: ', debt.balance)
            else:
                #   Once debt is paid, its min payment is added to extra budget on the following month
                current_extra_pool += debt.min_payment 
                print('extra pool: ', current_extra_pool)

        #   Use extra budget pool to pay highest APR debt. Ignores other debts even if there's left over extra budget
        for debt in snowball_debt_list:
            if debt.balance > 0 and current_extra_pool > 0:
                extra_pay = min(debt.balance, current_extra_pool)
                debt.balance -= extra_pay
                #   Remaining extra pool 
                current_extra_pool -= extra_pay 
                print('extraaaaaa ', debt.balance)
                break

        remaining_debt_total = 0
        for debt in snowball_debt_list:
            remaining_debt_total += debt.balance
            
        monthly_history.append({
            'month': total_months,
            'remaining_balance': remaining_debt_total
        })

    # print(monthly_history)
        print('###########################')


    return {
        #   avalanche_debt_list
        'strategy': 'Avalanche',
        'total_months': total_months,
        'total_interest_paid': total_interest_paid,
        'monthly_history': monthly_history
    }

# def case_test():
#     assert calculate_monthly_interest(1000, 20) == 16.67

# a = collect_debt_details()
# print(a.name, a.type, a.balance, a.apr)

debt1 = Debt('debt1', 1000, 6, 100)
debt2 = Debt('debt2', 5000, 12, 200)
# debt3 = Debt('debt3', 3500, 23, 120)
# debt4 = Debt('debt4', 1000, 7, 50)
# debt5 = Debt('debt5', 7000, 4, 150)
# debt6 = Debt('debt6', 100, 4, 130)

debt_list = [debt1, debt2]
# debt_list = [debt1, debt2, debt3, debt4, debt5, debt6]

#################
# avalanche_debt = calculate_avalanche(debt_list, 500)
# print(avalanche_debt)
##################

snowball_debt_list = calculate_snowball(debt_list, 200)
print(snowball_debt_list)

# print('Debt List')
# for d in debt_list:
#     print(d.name, d.balance, d.apr, d.min_payment)
# print('\nAvalance')
# for d in avalanche_debt_list:
#     print(d.name, d.balance, d.apr, d.min_payment)
# print('\nSnowball')
# for d in snowball_debt_list:
#     print(d.name, d.balance, d.apr, d.min_payment)

# print(calculate_monthly_interest(1000,20))
# case_test()


