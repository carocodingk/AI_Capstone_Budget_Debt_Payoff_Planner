class Debt:
    def __init__(self, name, type, amount, apr):
        self.name = name
        self.type = type
        self.amount = amount
        self.apr = apr

def collect_debt_details():
    """Collects details (name, current amount, APR and type) about user's debts"""
    name = input('Enter account name: ')
    type = input('Enter debt type: ')
    amount = input('Enter amount owed: ')
    apr = input('Enter debt APR: ')
    debt = Debt(name, type, amount, apr)
    return debt


a = collect_debt_details()
print(a.name, a.type, a.amount, a.apr)