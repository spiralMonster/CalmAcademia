import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.fun_game_manger_specs import FunGameManagerSpecs
load_dotenv()

def FunGameManager(state):
    question=state["key"]["fun_game"]["question"]
    answer=state["key"]["user_response"]
    fun_game=state["key"]["fun_game"]["type"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(FunGameManagerSpecs)

    template="""
    Given the question asked by an AI agent during {fun_game} game and the answer given by user.
    Depending upon the user response decide whether the user want o continue the game or exit it.
    Question:
    {question}
    Answer:
    {answer}
    """

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['fun_game','question','answer'])

    fun_game_manager_chain=prompt|llm
    fun_game_state=fun_game_manager_chain.invoke(
        {
            'fun_game':fun_game,
            'question':question,
            'answer':answer
        }
    ).fun_game_state

    state["key"]["fun_game_state"]=fun_game_state
    return state