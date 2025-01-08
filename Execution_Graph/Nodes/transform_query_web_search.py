import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.transform_query_web_search_specs import TransformQueryForWebSearchSpecs
load_dotenv()

def TransformQueryForWebSearch(state):
    query=state["key"]["user_response"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(TransformQueryForWebSearchSpecs)

    sys_msg="""
    Transform the user query in such a way such that relevant results are retrieved from the web search.
    """
    prompt=ChatPromptTemplate.from_messages([
        ("system",sys_msg),
        ("human","{user_query}")
    ])

    transformed_query_chain=prompt|llm
    transformed_query=transformed_query_chain.invoke({"user_query":query}).transformed_query
    state["key"]["transformed_query"]=transformed_query
    print("Query transformed for web search")
    return state
