import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.context_decider_options import ContextDeciderOptions
load_dotenv()

def ContextDecider(state):
    question=state["key"]["user_response"]

    llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(ContextDeciderOptions)

    sys_msg="""
    Depending upon the question asked by the user decide whether the context should be retrieved from web_search or vectorstore.
    The vectorstore contains the information and tips to tackle various issues related to:
     - Exam Pressure
     - Scoring low marks in exam
     - Family Pressure
     - Performance Anxiety
     - Homesickness
     - Relationship Problems
     - Money issues
     - Anxiety of Future
    """

    prompt=ChatPromptTemplate.from_messages([
        ("system",sys_msg),
        ("human","{question}")
    ])

    context_decider_chain=prompt|llm
    context_decider=context_decider_chain.invoke({"question":question}).context_decider
    state["key"]["context_decider"]=context_decider
    print("Method of Context achieved..")
    return state
