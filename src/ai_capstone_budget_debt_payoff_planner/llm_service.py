import ollama
import json

MODEL_NAME = 'llama3.2'
CATEGORIES = ['Food', 'Housing', 'Utilities', 'Transportation', 'Entertainment', 'Personal Care', 'Clothing', 'Education', 'Other']

def check_ollama_status():
    """ Verifies that local Ollama server is running    """
    try: 
        ollama.list()
        return True
    except Exception as e:
        print(f'Ollama connection failed: {e}')


def categorize_expense(description):
    """ Categorize expenses based on description or name of vendor into JSON format """

    #   System prompt with explicit category rules
    system_prompt = f"""You are an expert financial classifier. Your task is to categorize an expense into EXACTLY ONE category from 
        this list: {CATEGORIES} based on a description or the name of the vendor. 
        Important rules:
        -   "Food" includes any mention of food, drinks, alcohol and beverages.
        -   "Utilities" includes electricity, water, gas, internet, and phone/cellular bills (such as Verizon, AT&T, T-Mobile, Lycamobile, Mint Mobile).
        -   "Transportation" is strictly for gas stations, public transit, car payments, tolls, and auto insurance.
        -   "Other" if you are not sure
        You must respond with ONE valid JSON object in this schema: {{'category': "<selected_category>"}}
        """

    #   N-shot examples 
    messages = [
        {"role": "system", "content": system_prompt},
        # Example 1
        {"role": "user", "content": "Cake, drinks, beer, soda"},
        {"role": "assistant", "content": '{"category": "Food"}'},
        # Example 2
        {"role": "user", "content": "Expense description: 'Trader Joe's groceries'"},
        {"role": "assistant", "content": '{"category": "Food"}'},
        # Example 3
        {"role": "user", "content": "Expense description: 'Bolla'"},
        {"role": "assistant", "content": '{"category": "Transportation"}'},
        # Example 4
        {"role": "user", "content": "Expense description: 'T-Mobile monthly bill'"},
        {"role": "assistant", "content": '{"category": "Utilities"}'},
        # Example 5        
        {"role": "user", "content": "Expense description: 'AMC Movie Tickets'"},
        {"role": "assistant", "content": '{"category": "Entertainment"}'},
        # Target
        {"role": "user", "content": f"Expense description: '{description}'"}
    ]

    try: 
        response = ollama.chat(
            model = 'llama3.2',
            messages=messages,
            # messages = [
            #     {'role': 'system', 'content': system_prompt},
            #     {'role': 'user', 'content': f"Expense description or vendor: {description}"}
            # ],
            format = 'json'
        )

        #   Parse structured JSON 
        content = response.get('message', {}).get('content', '')
        data = json.loads(content)
        #   Lookup for key 'category'. If none, 'Other' is default
        category = data.get('category', 'Other')
        #   Verify that category assigned by model is in the list
        return category if category in CATEGORIES else 'Other'
        
    except Exception as e:
        print(f"Failed to categorize expense '{description}: {e}")


def generate_strategy_summary(snowball_result, avalanche_result):
    """ Generate a natural language summary explaining the advantages and disadvantages of the snowball and avalanche methods   """

    #   Calculates savings in time and cash
    interest_saved = round(snowball_result['total_interest_paid'] - avalanche_result['total_interest_paid'] , 2)
    time_saved = round(snowball_result['total_months'] - avalanche_result['total_months'] , 2)

    prompt = f"""You are a financial advisor reviewing pre-calculated debt payoff strategies. 
        Do NOT perform any math calculations yourself. Use ONLY these figures:

        Debt Snowball (Smallest Balance First):
        - Time to payoff: {snowball_result['total_months']} months
        - Total interest paid: ${snowball_result['total_interest_paid']}

        Debt Avalanche (Highest APR First):
        - Time to payoff: {avalanche_result['total_months']} months
        - Total interest paid: ${avalanche_result['total_interest_paid']}

        Key Differences:
        - Avalanche saves ${interest_saved} in interest.
        - Avalanche saves {time_saved} months compared to Snowball.

        Task:
        Write a concise 2 to 3 paragraph summary comparing these outcomes. 
        Explain the psychological momentum of the Snowball method vs. the financial savings of the Avalanche method.
    """

    try:
        response = ollama.chat(
            model='llama3.2',
            messages=[{"role": "user", "content": prompt}]
        )
        return response.get("message", {}).get("content", "Unable to generate strategy summary.")

    except Exception as err:
        print(f"Failed to generate strategy summary: {err}")
        return "AI summary service is currently unavailable. Check that Ollama is running locally."