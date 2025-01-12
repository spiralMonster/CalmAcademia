import os

from click import prompt
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def ISpyQuestionGenerator(state):
    word=state["key"]["i_spy_word"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY'])

    template=""""
    The user has to guess {word} word.
    Generate a question regarding that word such that it will help the user to guess that word.
    """
    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=["word"])

    question_gen_chain=prompt|llm|StrOutputParser()
    question=question_gen_chain.invoke({"word":word})

    state["key"]["i_spy_question"]=question
    return state