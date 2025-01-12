import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.i_spy_manager_specs import ISpyManagerSpecs

load_dotenv()

def ISpyManger(state):
    question=state["key"]["fun_game"]["question"]
    answer=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(ISpyManagerSpecs)

    template="""
    Use the given context and user response and decide whether the word is correctly guessed or not.
    Context:
    {question}
    User_response:
    {user_response}
    """
    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=["question","user_response"])

    manager_chain=prompt|llm
    user_answer=manager_chain.invoke({
        'question':question,
        'user_response':answer
    }).user_answer

    state["key"]["i_spy_user_answer"]=user_answer
    return state