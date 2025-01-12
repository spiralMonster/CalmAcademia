import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def FunGameGenerator(state):
    problem=state["key"]["user_problem"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )

    template="""
    The user is dealing with the {problem} problem.
    You asked user to take part in a fun game and user agrees to it.
    Frame a question asking user which fun game they want to take part in.
    The fun game includes:
     - Would you rather..
     - I spy
     - Never have I ever
    """

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=["problem"])

    fun_game_generator_chain=prompt|llm|StrOutputParser()

    fun_game_generator=fun_game_generator_chain.invoke({"problem":problem})

    state["key"]["fun_game_generator"]=fun_game_generator
    return state