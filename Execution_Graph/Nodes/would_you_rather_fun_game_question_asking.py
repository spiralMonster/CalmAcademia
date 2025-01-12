import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

def WouldYouRatherFunGameQuestionAsking(state):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY'])

    template="""
    The user want to play "Would you rather" fun game.
    In this game you will present user with two scenarios and see which one user will choose if given a choice.
    Use can use the following set of questions as a reference:
    {reference}
    """
    reference=[
        "Would you rather travel 100 years in the future or 100 years in the past?",
        "Would you rather be Ironman or Captain America?",
        "Would you rather live in Paris or Bangkok? "
    ]

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['reference'])

    question_asking_chain=prompt|llm|StrOutputParser()
    question=question_asking_chain.invoke({"reference":reference})

    state["key"]["would_you_rather_question"]=question
    return state


