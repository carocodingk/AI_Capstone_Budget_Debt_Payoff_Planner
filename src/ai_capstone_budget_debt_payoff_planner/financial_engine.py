import pytest

class Debt:
    def __init__(self, name, balance, apr):
        self.name = name
        self.balance = balance
        self.apr = apr


def collect_debt_details():
    """Collects details (name, current balance, APR and type) about user's debts"""
    name = input('Enter account name: ')
    type = input('Enter debt type: ')
    balance = input('Enter balance owed: ')
    apr = input('Enter debt APR: ')
    debt = Debt(name, balance, apr)
    return debt

def calculate_monthly_interest(balance, apr):
    """Calculate accrued monthly interest rounded to two decimals"""
    if balance <= 0 or apr == 0:
        return 0
    return round(balance * (apr / 12) / 100, 2)


def calculate_avalanche(debt_list):
    """Receives a list of debt objects and returns a sorted list in ascending order based on APR. Pay debts from highest interest rate (apr) to lowest"""
    avalanche_debt_list = sorted(debt_list, key=lambda debt: debt.balance)
    return avalanche_debt_list

def calculate_snowball(debt_list):
    """Receives a list of debt objects and returns a sorted list in descending order based on balance. Pay debts from lowest balance to highest"""
    snowball_debt_list = sorted(debt_list, key=lambda debt: debt.apr, reverse=True)
    return snowball_debt_list

def case_test():
    assert calculate_monthly_interest(1000, 20) == 16.67

# a = collect_debt_details()
# print(a.name, a.type, a.balance, a.apr)

debt1 = Debt('debt1', 120, 15)
debt2 = Debt('debt2', 35, 8)
debt3 = Debt('debt3', 35, 23)
debt4 = Debt('debt4', 100, 7)
debt5 = Debt('debt5', 10, 4)
debt6 = Debt('debt6', 100, 4)

debt_list = [debt1, debt2, debt3, debt4, debt5, debt6]

avalanche_debt_list = calculate_avalanche(debt_list)

snowball_debt_list = calculate_snowball(debt_list)

print('Debt List')
for d in debt_list:
    print(d.name, d.balance, d.apr)
print('\nAvalance')
for d in avalanche_debt_list:
    print(d.name, d.balance, d.apr)
print('\nSnowball')
for d in snowball_debt_list:
    print(d.name, d.balance, d.apr)

print(calculate_monthly_interest(1000,20))
case_test()


