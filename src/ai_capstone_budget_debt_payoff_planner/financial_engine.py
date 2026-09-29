class Debt:
    def __init__(self, name, type, balance, apr):
        self.name = name
        self.type = type
        self.balance = balance
        self.apr = apr

def collect_debt_details():
    """Collects details (name, current balance, APR and type) about user's debts"""
    name = input('Enter account name: ')
    type = input('Enter debt type: ')
    balance = input('Enter balance owed: ')
    apr = input('Enter debt APR: ')
    debt = Debt(name, type, balance, apr)
    return debt

def calculate_avalance(debt_list):
    """Receives a list of debt objects and sorts them out in place from lowest to highest balance"""
    debt_list.sort(key=lambda debt: debt.balance)
    return None


# a = collect_debt_details()
# print(a.name, a.type, a.balance, a.apr)

debt1 = Debt('debt1', 'Credit Card', 120, 15)
debt2 = Debt('debt2', 'Personal Loan', 35, 8)
debt3 = Debt('debt3', 'Credit Card', 35, 23)
debt4 = Debt('debt4', 'Mortgage', 100, 7)
debt5 = Debt('debt5', 'Student Loan', 10, 4)

debt_list = [debt1, debt2, debt3, debt4, debt5]

for d in debt_list:
    print(d.name, d.type, d.balance, d.apr)

calculate_avalance(debt_list)
for d in debt_list:
    print(d.name, d.type, d.balance, d.apr)