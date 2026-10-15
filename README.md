# CAP 942 Capstone Implementation Plan: AI Budget & Debt Payoff Planner (`ai_capstone_budget_debt_payoff_planner`)

An AI-powered, privacy-first personal finance dashboard built for macOS Apple Silicon. This application combines deterministic Python financial math with a local open-source LLM via Ollama to categorize expenses, calculate debt payoff schedules, and generate clear financial strategy insights.

## How to run 
```bash
uv run streamlit run src/ai_capstone_budget_debt_payoff_planner/app.py
```

---

## Table of Contents
1. [Project Overview](#1-project-overview)
2. [Problem Statement](#2-problem-statement)
3. [Capstone Requirement Alignment](#3-capstone-requirement-alignment)
4. [Project Scope](#4-project-scope)
5. [Technology Stack](#5-technology-stack)
6. [Target Directory Structure](#6-target-directory-structure)
7. [Application Workflow](#7-application-workflow)
8. [Application Architecture](#8-application-architecture)
9. [Development Milestones](#9-development-milestones)
10. [Guided Code Examples](#10-guided-code-examples)
11. [Prompt-Engineering Plan](#11-prompt-engineering-plan)
12. [Testing Plan](#12-testing-plan)
13. [Privacy, Security & Responsible AI](#13-privacy-security--responsible-ai)
14. [Local Setup & Execution Guide with `uv`](#14-local-setup--execution-guide-with-uv)
15. [Documentation & GitHub Plan](#15-documentation--github-plan)
16. [Presentation Plan](#16-presentation-plan)
17. [Definition of Done](#17-definition-of-done)

---

## 1. Project Overview

* **Project Title:** AI Budget & Debt Payoff Planner
* **Package Name:** `ai_capstone_carolina`
* **Description:** A desktop dashboard application that allows users to track monthly income, categorize expenses, and manage active debts. The system executes exact mathematical calculations for Debt Snowball and Debt Avalanche strategy comparisons, uses a local LLM to categorize ambiguous expense descriptions, and generates natural-language strategy summaries.
* **Value Proposition:** Empowers users to eliminate debt through error-free financial calculations coupled with privacy-focused AI insights running 100% locally on Apple Silicon hardware.


## 2. Problem Statement

Commercial financial planning applications frequently suffer from two core limitations:
1. **Privacy Concerns:** They require sending sensitive personal financial data to external cloud servers.
2. **AI Calculation Hallucinations:** Generative AI tools used for financial advice often generate mathematically incorrect figures when attempting arithmetic.

**Target Audience:** Consumers, students, and working professionals seeking an accessible, privacy-preserving desktop application to compare debt elimination strategies without monthly subscription fees or cloud data sharing.

## 3. Capstone Requirement Alignment

| Capstone Requirement | Implementation Strategy | Deliverable / Evidence |
| :--- | :--- | :--- |
| **Open-Source LLM** | Runs `llama3.2` (3B) locally using Ollama on Apple Silicon via Metal acceleration. | Ollama connection block in code; local inference logs. |
| **Accept User Input** | Streamlit interactive forms and editable tables for income, expenses, and debt inputs. | Interactive UI input components with type validation. |
| **LLM-Generated Output** | Zero-shot expense categorization and natural-language comparative strategy breakdowns. | UI view displaying categorized tables and AI feedback panels. |
| **Deterministic Code** | Computes interest accretion, monthly balances, and strategy timelines using pure Python. | `pytest` suite verifying calculation accuracy. |
| **Data Persistence** | Persists user profile, expenses, and debt lists locally using SQLite. | Local `planner.db` file and DDL schema script. |
| **Application Format** | Interactive desktop dashboard rendered via Streamlit. | Launchable `app.py` script running on localhost. |
| **Zero Paid APIs** | Built exclusively with free open-source libraries (`ollama`, `streamlit`, `sqlite3`). | Clean `pyproject.toml` with zero proprietary dependencies. |

## 4. Project Scope

### Minimum Viable Product (MVP) - Required
* **Interactive Data Entry:** Streamlit tables to manage income, expenses, and active debts (balance, APR, minimum payment).
* **Deterministic Financial Engine:** Pure Python algorithms for Debt Snowball (lowest balance first) and Debt Avalanche (highest interest rate first).
* **LLM Expense Categorization:** Zero-shot text classification mapping vague expense descriptions to standard categories.
* **LLM Strategy Explainer:** Natural-language comparative analysis detailing trade-offs between Snowball and Avalanche outcomes.
* **Local Persistence:** SQLite database storing inputs and calculated plans across app restarts.

### Out of Scope (Initial Release)
* Cloud data sync or user authentication services.
* Direct integration with external bank APIs (e.g., Plaid).
* Custom machine learning model training or fine-tuning.

### Optional Enhancements (Post-MVP)
* CSV bank statement upload and automated line-item parsing.
* Dynamic "What-if" budget allocation sliders.
* PDF report exporter using `ReportLab`.

## 5. Technology Stack

* **Language:** Python 3.11+
* **Environment & Package Manager:** `uv` (Fast, modern Python project manager)
* **Platform:** macOS (Apple Silicon optimized)
* **Local LLM Engine:** Ollama running `llama3.2` (3B)
* **LLM Client:** `ollama-python`
* **Dashboard Framework:** Streamlit
* **Database Engine:** SQLite3 (`planner.db`)
* **Testing:** `pytest`


## 6. Target Directory Structure

The project strictly follows a standard Python `src`-layout managed by `uv`:

```text
.
├── README.md                  # Project overview & capstone documentation
├── gitnotes.md                # Git command notes, commit log strategies, & rebasing notes
├── pyproject.toml             # uv dependency and package configuration
└── src
    └── ai_capstone_carolina
        ├── __init__.py        # Package initialization
        ├── app.py             # Main Streamlit dashboard application
        ├── database.py        # SQLite persistence and database queries
        ├── financial_engine.py# Deterministic Python math (Snowball & Avalanche)
        └── llm_service.py     # Ollama API interaction and prompt formatting
```

## 7. Application Workflow
```Code snippetgraph TD
    A[User Inputs Data via Streamlit UI in app.py] --> B{Expense Uncategorized?}
    B -- Yes --> C[Pass Description to Ollama LLM via llm_service.py]
    C --> D[LLM Returns Structured JSON Category]
    D --> E[Save Record to SQLite Database via database.py]
    B -- No --> E
    E --> F[Execute Financial Engine in financial_engine.py]
    F --> G[Calculate Debt Snowball Strategy]
    F --> H[Calculate Debt Avalanche Strategy]
    G --> I[Construct Prompt with Strategy Metrics]
    H --> I
    I --> J[Invoke Ollama for Strategy Narrative]
    J --> K[Render Comparison Dashboard & Charts in Streamlit]
```

## 8. Application Architecture
* Presentation Layer (src/ai_capstone_carolina/app.py): Handles UI rendering, user input capture, metric display, and Streamlit session state management.
* Financial Computation Engine (src/ai_capstone_carolina/financial_engine.py): Pure Python module executing debt amortization, interest calculations, and payoff ordering. Contains zero AI or LLM imports.
* Database Service Layer (src/ai_capstone_carolina/database.py): Manages SQLite connections, schema creation, and database CRUD operations (planner.db).
* AI Service Layer (src/ai_capstone_carolina/llm_service.py): Encapsulates Ollama client calls, enforces structured JSON output, and handles model exception fallbacks.

## 9. Development Milestones
### Milestone 1: Environment & Workspace Setup (uv)
* Learning Objective: Initialize a Python src-layout package using uv and establish local communication with Ollama.
* Tasks:
    1. Install Ollama and pull model: ollama pull llama3.2.
    2. Initialize project with uv: uv init --package src/ai_capstone_carolina.
    3. Install core dependencies: uv add streamlit ollama pytest.
    4. Create gitnotes.md to log setup notes and git workflows.
* Testing Checkpoint: Verify local Ollama response via a standalone test execution.
* Acceptance Criteria: Local script returns an LLM text response within 3 seconds offline.

### Milestone 2: Deterministic Financial Engine
* Learning Objective: Build verifiable personal finance algorithms in financial_engine.py using pure Python.
* Tasks:
    1. Implement calculate_snowball(debts, extra_payment) sorting debts by balance ascending.
    2. Implement calculate_avalanche(debts, extra_payment) sorting debts by APR descending.
    3. Accrue interest monthly: $\text{Interest} = \text{Balance} \times \left(\frac{\text{APR}}{12}\right)$.
* Testing Checkpoint: Execute uv run pytest comparing calculations against verified reference schedules.
* Acceptance Criteria: Tests pass with zero arithmetic error or floating-point drift.

### Milestone 3: Database Persistence Layer
* Learning Objective: Manage local application state in database.py using SQLite.
* Tasks:
    1. Define schema tables for expenses and debts.
    2. Write CRUD helper functions in database.py.
* Testing Checkpoint: Perform write-read-delete cycle tests using pytest.
* Acceptance Criteria: Data persists in planner.db across complete process restarts.

### Milestone 4: Ollama JSON Expense Categorization
* Learning Objective: Constrain local LLM responses in llm_service.py to structured JSON formats.
* Tasks:
    1. Write system prompt mapping vague items to fixed category names.
    2. Implement exception handling for JSON parsing failures.
* Testing Checkpoint: Pass ambiguous descriptions (e.g., "Uber trip", "Target") and inspect output types.
* Acceptance Criteria: 100% of tested inputs return valid category strings without application crashes.

### Milestone 5: Dashboard UI Assembly
* Learning Objective: Create an interactive UI in app.py using Streamlit components.
* Tasks:
    1. Build input controls for income, budget allocations, and debt records.
    2. Embed interactive data tables using st.data_editor.
    3. Integrate line charts (st.line_chart) displaying payoff curves over time.
* Testing Checkpoint: Perform end-to-end user workflows in the browser via uv run streamlit run src/ai_capstone_carolina/app.py. 
* Acceptance Criteria: Modifying a value triggers an instant calculation and layout update. 

## 10. Guided Code Examples
### Example 1: Monthly Interest Calculation (financial_engine.py)
```Python
def calculate_monthly_interest(balance: float, annual_percentage_rate: float) -> float:
    """Calculates accrued monthly interest without relying on AI."""
    if balance <= 0 or annual_percentage_rate < 0:
        return 0.0
    
    monthly_rate = (annual_percentage_rate / 100.0) / 12.0
    return round(balance * monthly_rate, 2)

# TODO: Write a function `apply_monthly_payment(balance, apr, payment)`
# that adds monthly interest to balance and subtracts the payment amount.
```

* Explanation: All arithmetic must remain inside standard Python functions to prevent model hallucination.
* Practice Task: Complete the TODO block to calculate remaining balance post-payment.

### Example 2: Structured Ollama JSON Classification (llm_service.py)
```Python
import json
import ollama

def categorize_expense(description: str) -> str:
    """Uses local Ollama to map expense descriptions to a standard category."""
    allowed_categories = ["Housing", "Food", "Transportation", "Utilities", "Entertainment", "Other"]
    
    system_prompt = f"""You are a financial classifier. 
Categorize the expense into EXACTLY one category from this list: {allowed_categories}.
Return ONLY a valid JSON object matching this structure: {{"category": "<selected_category>"}}"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Expense description: {description}"}
        ],
        format="json"
    )
    
    # TODO: Parse response['message']['content'] using json.loads()
    # Extract and return the category string, falling back to "Other" on failure.
    return "Other"
```

* Explanation: Utilizing format="json" forces Ollama to generate strict structured outputs.
* Practice Task: Implement a safe try...except JSON parsing block inside the function.

### Example 3: Database Data Fetching (database.py)
```Python
import sqlite3
from typing import List, Tuple

def fetch_all_debts(db_path: str = "planner.db") -> List[Tuple]:
    """Retrieves recorded debts from local SQLite database."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS debts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            balance REAL NOT NULL,
            apr REAL NOT NULL,
            min_payment REAL NOT NULL
        )
    """)
    
    # TODO: Execute SELECT query to fetch all debt records.
    # Use cursor.fetchall(), close the connection, and return data.
    
    conn.close()
    return []
```
* Explanation: SQLite manages local state without requiring external database servers.
* Practice Task: Write the standard SQL query needed to fetch and return table rows.

## 11. Prompt-Engineering Plan
* Role: Empowering financial assistant providing educational context.
* Inputs Passed to Model: Pre-computed metrics from financial_engine.py (snowball_months, snowball_interest, avalanche_months, avalanche_interest, savings).
* Format: Markdown text containing comparative commentary.
* Prompt Template:
```Plaintext
System: You are an empathetic financial mentor. You do NOT perform math calculations. Use ONLY the provided numbers.

Context:
- Debt Snowball: Payoff time = {snowball_months} months | Total Interest = ${snowball_interest}
- Debt Avalanche: Payoff time = {avalanche_months} months | Total Interest = ${avalanche_interest}
- Total Savings with Avalanche: ${savings}

Task: Write a 3-paragraph summary comparing these outcomes. Contrast the psychological momentum of Snowball against the financial efficiency of Avalanche.
```

## 12. Testing Plan
### Unit Tests (pytest)
* Validate interest accrual algorithms using known financial parameters.
* Test SQLite CRUD operations and database initializations.
* Verify JSON extraction handles corrupted LLM outputs gracefully.

### Integration Test Matrix
| Test Case | System Input | Expected Math Engine Result | Expected LLM Behavior |
| :---------- | :---------- | :---------- | :---------- |
| 1. Zero Balance Debt | Balance: $0 | Excluded from calculation schedules. | Excludes item from strategy narrative. |
| 2. Single Active Debt | Card: $1,000, 18% APR | Snowball and Avalanche produce identical timelines. | Notes strategy outcomes are identical. |
|3. Divergent Strategies | Debt A: $500 @ 10%; Debt B: $5,000 @ 25% | Snowball targets Debt A first; Avalanche targets Debt B first. | Highlights interest savings of Avalanche. |
| 4. Unclear Expense | Description: "SQ *COFFEE SHOP" | N/A | Categorizes item into "Food".|
| 5. Invalid Number Input | APR: -10% | Validation error caught in UI before calculation. | N/A |

## 13. Privacy, Security & Responsible AI
* Data Privacy: Financial inputs remain localized inside planner.db. Inferences run locally via Ollama on Apple Silicon without outbound network requests.
* Calculation Safety: Generative AI models are strictly barred from calculating interest rates or payoff dates to ensure absolute mathematical accuracy.
* Disclaimer: The interface explicitly features the disclaimer: "This application is an educational prototype and does not constitute certified financial advice."

## 14. Local Setup & Execution Guide with uv
### Prerequisites
* macOS running on Apple Silicon (M1/M2/M3/M4).
* Ollama installed.
* uv installed (brew install uv).

### Setup & Launch Commands
```Bash
# 1. Initialize project directory structure (if starting fresh)
uv init --package src/ai_capstone_carolina

# 2. Add dependencies to pyproject.toml
uv add streamlit ollama pytest

# 3. Pull required open-source LLM
ollama pull llama3.2

# 4. Synchronize environment dependencies
uv sync

# 5. Run application tests
uv run pytest

# 6. Launch local Streamlit application
uv run streamlit run src/ai_capstone_carolina/app.py
```

## 15. Documentation & GitHub Plan
* README.md: Comprehensive capstone project documentation, setup instructions, architecture breakdown, and workflow diagrams.
* gitnotes.md: Contains developer log entries, feature branch strategies, rebase history notes, and terminal commands used during project iterations.
* pyproject.toml: Fully documented package file specifying dependencies, Python requirements, and build configuration.

## 16. Presentation Plan
### 5-10 Minute Presentation Outline
1. Introduction & Problem (1.5 mins): Overview of debt elimination challenges and the risk of AI calculation hallucinations.
2. System Architecture (2 mins): Explanation of deterministic Python math paired with local Ollama inference.
3. Live System Demonstration (4 mins):
    * Input income, expenses, and active debts into Streamlit UI.
    * Demonstrate real-time LLM expense categorization.
    * Render Snowball vs. Avalanche comparison charts and inspect the AI-generated strategy summary.
4. Conclusion & Lessons Learned (1.5 mins): Reflections on local model orchestration and technical trade-offs.

## 17. Definition of Done
[ ] Runs 100% locally on macOS without paid APIs.

[ ] Financial calculations performed deterministically in financial_engine.py.

[ ] Uncategorized expenses processed accurately via local Ollama instance (llama3.2) in llm_service.py.

[ ] Strategic summary generated based on pre-calculated financial outcomes.

[ ] User state persists across app restarts inside local SQLite database (planner.db) managed by database.py.

[ ] Interactive dashboard operates smoothly inside app.py via Streamlit UI.

[ ] Unit tests pass via uv run pytest.

[ ] Directory structure strictly matches required layout with README.md, gitnotes.md, pyproject.toml, and src/ai_capstone_carolina/.

[ ] Complete codebase pushed to GitHub.