import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.fun_game_decider_specs import FunGameDeciderSpecs

def FunGameDecider(state):
    user_response=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(FunGameDeciderSpecs)

    sys_msg="""
    Depending upon the user response decide which fun game the user want to play.
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{user_response}")
        ]
    )

    fun_game_decider_chain=prompt|llm
    fun_game_type=fun_game_decider_chain.invoke({"user_response":user_response}).fun_game_type

    state["key"]["fun_game_type"]=fun_game_type
    return state