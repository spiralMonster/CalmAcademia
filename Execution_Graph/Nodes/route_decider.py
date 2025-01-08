import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.route_decider_specs import RouteDeciderSpecs
load_dotenv()

def RouteDecider(state):
    user_response=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(RouteDeciderSpecs)

    sys_msg="""
    Depending upon user response predict whether the user is asking a question or giving answer to the question.
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{user_response}")
        ]
    )

    route_decider_chain=prompt|llm
    user_response_type=route_decider_chain.invoke({'user_response':user_response}).user_response_type

    state["key"]["user_response_type"]=user_response_type
    return state


