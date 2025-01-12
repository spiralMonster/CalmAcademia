import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.i_spy_word_generator_specs import ISpyWordGeneratorSpecs
load_dotenv()

def ISpyWordGenerator(state):
    fun_game=state["key"]["fun_game_type"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']).with_structured_output(ISpyWordGeneratorSpecs)

    template="""
    The user want to play {fun_game} game.
    So generate any word which the user has to guess.
    """


    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['fun_game'])

    question_asking_chain=prompt|llm
    question=question_asking_chain.invoke({"fun_game":fun_game}).word

    state["key"]["i_spy_word"]=question
    return state


