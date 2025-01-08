import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.tranform_query_vectorstore_specs import TransformQueryForVectorStoreSpecs
load_dotenv()

def QueryTransformationForVectorStore(state):
    query=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(TransformQueryForVectorStoreSpecs)
    sys_msg="""
    Generate a document of length 150-250 words from the given query without changing the semantic meaning of the query.
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{query}")
        ]
    )
    transformed_query_chain=prompt|llm
    transformed_query=transformed_query_chain.invoke({'query':query}).transformed_query

    state["key"]["transformed_query"]=transformed_query
    return state
