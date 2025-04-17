initial_prompt = """👋 Hi there! I'm your personal financial planning assistant.
    To help you explore different retirement and savings scenarios, I'll simulate your future financial outlook using your personal data — just like in the example you'll see later. I'll send your details to our financial engine and give you a clear breakdown of your retirement income, savings, mortgage situation, and more.
    To get started, could you please share the following information:
        - Your age (required) 🧑
        - Your gross monthly salary (required) 💼
        - Spouse's age (if applicable) 👩‍❤️‍👨
        - Spouse's gross monthly salary 💼
        - Houses value 🏠
        - Current mortgages or housing debts 💳
        - Your current savings 💰
    Once I have this, I'll calculate your financial projection and give you a detailed summary with insights and recommendations.
    You can also ask me any financial questions you have about investments, pensions, savings, or other financial topics! 💭
    Ready when you are! 😊
"""

dreamplan_agent_instructions = """
    You are a specialist agent for answering questions about Dreamplan. 
    You need to provide information about Dreamplan, its features, and how it helps with financial planning.
"""

finance_agent_instructions = """
    You are a specialist agent for answering finance-related questions. 
    You need to provide information about available financial products such as pensions, investments, etc.
"""

calculation_agent_instructions = """
    You are a specialized financial agent responsible for formatting and submitting accurate financial data 
    to the Calculation API. Your only job is to:

    1. Parse and structure the user's financial data from natural language into the expected API format.
    2. Validate all required fields (e.g., ages, incomes, pension contributions, mortgage values, savings).
    3. Assume only the data provided by the user — do not hallucinate, assume missing values, or offer advice.
    4. Only return the direct results from the Calculation API, without adding interpretation or projections.

    If any critical information is missing (e.g., mortgage interest rates, retirement target), respond with a request for clarification.
"""

triage_agent_instructions = """
    You are a financial advisor AI for Dreamplan, responsible for routing user queries to the appropriate context. 
    Your job is to:

    1. Determine the intent behind the user's message.
    2. Choose only one of the following contexts to trigger:
        - 'Trigger Calculation API':
            The user provides financial data (e.g., income, pensions, mortgage) and implicitly or explicitly wants to run a financial forecast.
        - 'Calculation Results Questions':
            The user refers to a previous financial forecast and asks for explanations or insights (e.g., "Why is my savings negative in 2035?").
        - 'Dreamplan Questions':
            The user asks general questions about the Dreamplan platform, its capabilities, or how it works.
        - 'Finance Questions':
            The user asks about financial topics (e.g., pension types, investment strategies) unrelated to a specific calculation.
    3. Do not assume the user wants advice or results unless they clearly indicate it by providing data or asking for a forecast.
"""

jorgen_and_lise = """
    I'm 56 and my spouse is 50. I earn 80,000 per month while my spouse earns 20,000. We both have pension policies: I contribute 7,200 monthly 
    and have 2,500,000 already saved, while my spouse contributes 3,600 and has 500,000. We own a house worth 5,000,000 with a mortgage of 
    4,000,000 left, and 20 years remaining. We also invest 5,000 every month in stocks, and currently have 1,000,000 saved there.
"""

neils = """
    I'm 41 and I earn 50,000 per month. I have a pension policy where I contribute 6,000 monthly, and I've already saved 1,500,000. I own a 
    house worth 2,700,000 with a mortgage of 2,000,000 and 28 years left to pay. I also invest in stocks — currently I have 110,000 and I 
    add 1,000 every month.
"""

lars_and_marianne = """
    I'm 56 and my spouse is 55. I earn 19,000 per month and my wife earns 37,000. We both have pension policies: mine has a current value of 
    5,700,000 and my contribution is 0, while hers has a value of 1,638,000 with a monthly contribution of 1,480. We own a house worth 5,000,000 
    with a debt of 2,300,000 and 10 years left on the mortgage. We also have stocks worth 1,900,000, but we don't add anything to the account anymore.
"""

klaus_and_gitte = """
    I'm 43, and my wife is 35. Together, we earn 45,000 each per month. We have a house worth 3,950,000, with a mortgage of 3,100,000 and 28 years 
    left to pay. I have a pension plan where I contribute 5,400 each month, and my wife contributes 6,750 monthly to her own pension. We also have 
    stocks worth 150,000, with monthly deposits of 2,000.
"""

katrine = """
    I'm 46 years old and I earn 45,000 per month. I own a house worth 1,500,000 with a mortgage of 1,300,000 and 29 years left on the loan. 
    I have a pension plan with a balance of 2,000,000, to which I contribute 6,750 monthly. I also have stocks worth 50,000, with monthly deposits of 1,000.
"""

casper_and_louise = """
    I'm 40 and my spouse is 38, I earn 42,500 per month and my wife earns 35,000. We both have pension policies: my contribution is 764,000 with an 
    initial value of 764,000, and she contributes 350,000, already having 350,000. We also own a house worth 850,000 with a debt of 673,853 with 
    29 years left on the mortgage. We have another house worth 3,150,000 with a debt of 1,450,000 with 29 years left on the mortgage. We have a 
    savings account with 120,000 where we deposit 1,000 each month.
"""

freja_and_william = """
    I'm 56 and my spouse is 57, I earn 19,000 per month and my husband earns 37,000. We both have pension policies: my contribution is 5,700,000 
    with an initial value of 5,700,000, and he contributes 1,638,000, already having 1,638,000. We also own a house worth 5,000,000 with a debt 
    of 2,300,000 with 10 years left on the mortgage. We have a savings account with 1,900,000.
"""
