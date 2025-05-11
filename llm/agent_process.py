# -*- coding: utf-8 -*-
"""
@Time    : 2025/4/29 12:55
@Author  : ShenXinjie
@Email   : 
@Desc    : 
"""

from langchain.agents import tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI

import os
import pandas as pd
from config import get_project_root, ali_api_key

df_resource = pd.read_csv(
    os.path.join(get_project_root(), "Data/after_process/base.csv"),
    encoding="utf-8"
)
# df_resource.info()

# %% -------------------tools-------------------

from fuzzywuzzy import fuzz

@tool("fuzzy_match_company_name", description="Fuzzy Match Company Name.")
def fuzzy_match_company_name(company_name: str) -> str:
    """
    Fuzzy Match Company Name
    :param company_name:
    :return:
    """
    df_copy = df_resource[
        ['Name']
    ].copy()
    df_copy['match_score'] = df_copy['Name'].apply(lambda x: fuzz.ratio(company_name, x))

    # Returns the company name with the highest matching score
    best_match = df_copy.loc[df_copy['match_score'].idxmax()]['Name']
    best_score = df_copy['match_score'].max()
    if best_score > 60:  # setting a threshold for matching
        return best_match
    else:
        return "No relevant data found"


@tool("search_company_data", description="Find data by company name")
def search_company_data(company_name: str) -> str:
    """
    Find data by company name
    :param company_name: company name
    :return: related data of the company
    """
    # Check if the company name exists in the DataFrame
    if company_name not in df_resource['Name'].values:
        return "No relevant data found"
    result = df_resource[df_resource['Name'].str.contains(company_name, na=False)]
    if not result.empty:
        return result.to_string(index=False)
    else:
        return "No relevant data found"


@tool("ranking_of_column", description="obtain the names of the top-ranked companies based on the specified column")
def ranking_of_column(column: str, return_number: int, ascending: bool = False) -> str:
    """
    obtain the names of the top-ranked companies based on the specified column
    :param column: specified column name
    :param return_number: number of top companies to return
    :param ascending: sort order, default is descending
    """
    df_copy = df_resource.copy()
    # Check if the column exists in the DataFrame
    if column not in df_copy.columns:
        return f"Column '{column}' does not exist in the DataFrame."

    # check if the column is numeric
    if not pd.api.types.is_numeric_dtype(df_copy[column]):
        return f"Column '{column}' is not numeric."

    # Sort the DataFrame based on the specified column
    sorted_df = df_copy.sort_values(by=column, ascending=ascending)
    # Get the top N companies based on the specified column
    top_companies = sorted_df.head(return_number)

    # return the list of company names
    return top_companies['Name'].to_string(index=False)


@tool("explain_search_company_data",
      description="Obtain explanations of the column names returned by search_company_data")
def explain_search_company_data() -> str:
    """Obtain explanations of the column names returned by search_company_data"""
    return """
    1. Symbol: Stock symbol
    2. Name: company name
    3. Address: company address
    4. Sector: company sector
    5. Industry: company industry
    6. Full Time Employees: the number of employees
    7. Description: company description
    8. Total ESG Risk score: total ESG risk score
    9. Environment Risk Score: environmental risk score
    10. Governance Risk Score: governance risk score
    11. Social Risk Score: social risk score
    12. Controversy Level: controversy level
    13. Controversy Score: controversy score
    14. ESG Risk Percentile: ESG risk percentile
    15. ESG Risk Level: ESG risk level            
    16. SDG Score: SDG Score is a quantitative metric designed to evaluate a company's alignment with and commitment to the United Nations Sustainable Development Goals (SDGs).
    17. topic: 
    18. keywords: keywords of the company annual report
    """


# %% -------------------agent-------------------
tools = [search_company_data, fuzzy_match_company_name, ranking_of_column, explain_search_company_data]
llm = ChatOpenAI(
    model="qwen-max-2025-01-25",  # qwen-max-2025-01-25
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=ali_api_key,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# test
# print(agent.invoke({"input": "Xylem Inc"})["output"])
# print(agent.invoke({"input": "数据库中有叫做Zoetis Inc的公司吗?"})["output"])
# print(agent.invoke({"input": "Governance Risk Score排名靠前的5个公司名称"})["output"])
