import os
from typing import Any

import pandas as pd
from llama_index.query_engine import PandasQueryEngine
from llama_index.llms import AzureOpenAI

azure_openai_key = os.environ["OPENAI_API_KEY"]

large_language_model=AzureOpenAI(
    model="gpt-4-1106-preview",
    deployment_name="gpt-4-turbo",
    api_key=os.environ["OPENAI_API_KEY"],
    azure_endpoint='https://aihub-dev-openai.openai.azure.com/',
    api_version="2023-07-01-preview",
)


def produce_chatbot_response(vessel_data: pd.DataFrame, query: str) -> Any:
    print(vessel_data.columns)
    query_engine = PandasQueryEngine(df=vessel_data, llm=large_language_model)
    response = query_engine.query(query)
    print(response.response)
    return response

