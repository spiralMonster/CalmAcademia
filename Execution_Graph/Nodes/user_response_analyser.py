import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.user_response_analyser_specs import UserResponseAnalyserSpecs

def UserResponseAnalyser(state):
    user_response=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(UserResponseAnalyserSpecs)

    sys_msg="""
    Depending upon the user response decide whether the user want to perform the activity or not.
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{user_response}")
        ]
    )

    user_response_analyser_chain=prompt|llm
    user_response_analysis=user_response_analyser_chain.invoke({"user_response":user_response}).user_response_analysis

    state["key"]["user_response_analysis"]=user_response_analysis
    return state