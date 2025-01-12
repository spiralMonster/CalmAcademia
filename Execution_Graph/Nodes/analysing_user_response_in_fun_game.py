import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def AnalyzingUserResponseDuringGame(state):
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
    )

    template="""
    Given the question asked by an AI agent during {fun_game} game and the answer given by user.
    Generate a funny comment by by analysing the user response that will make user laugh.
    You can also use sarcastic comments.
    Question:
    {question}
    Answer:
    {answer}
    """
    prompt=ChatPromptTemplate.from_template(tenplate=template,
                                            input_variable=['fun_game','question','answer'])

    analyzing_chain=prompt|llm|StrOutputParser()
    ai_response=analyzing_chain.invoke(
        {
            'fun_game':fun_game,
            'question':question,
            'answer':answer
        }
    )

    state["key"]["ai_response"]=ai_response
    return state




