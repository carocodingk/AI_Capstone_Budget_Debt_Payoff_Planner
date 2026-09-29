def collect_debt_details():
    """Collects details (name, current amount, APR and type) about user's debts"""
    
    debt_name = input('Enter account name: ')
    debt_type = input('Enter debt type: ')
    debt_amount = input('Enter amount owed: ')
    debt_APR = input('Enter debt APR: ')
    print(debt_name, debt_type, debt_amount, debt_APR)
    return 0

collect_debt_details()