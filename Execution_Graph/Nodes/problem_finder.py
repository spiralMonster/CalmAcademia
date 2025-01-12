import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.problem_finder_options import ProblemFinderOptions
load_dotenv()

def ProblemFinder(state):
    user_response=state['key']['user_response']


    llm=ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0,
    max_tokens=None,
    timeout=None,
    max_retries=2,
    api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(ProblemFinderOptions)

    system_msg="""
    Classify the user response into appropriate problem.
    """
    prompt=ChatPromptTemplate.from_messages([
        ("system",system_msg),
        ("human","{question}")
    ])

    problem_finder_chain=prompt|llm
    problem=problem_finder_chain.invoke({'question':user_response}).problem
    state['key']['problem']=problem
    print("Problem Identified...")
    return state



