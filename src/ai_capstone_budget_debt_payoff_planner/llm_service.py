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

    system_prompt = f"""You are a financial advisor. Your task is to categorize an expense into EXACTLY ONE category from 
        this list: {CATEGORIES} based on a description or the name of the vendor. You must respond with ONE valid JSON object 
        in this schema: {{'category': "<selected_category>"}}
        """

    try: 
        response = ollama.chat(
            model = 'llama3.2',
            messages = [
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': f"Expense description or vendor: {description}"}
            ],
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


print(categorize_expense('Buying stuff for face and hair'))

    




