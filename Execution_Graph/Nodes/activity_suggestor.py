import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def ActivitySuggestor(state):
    problem=state["key"]["problem"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )
    temp="""
    The user is under stress due to {problem} problem.
    Frame a question asking user whether he want to:
     - hear a funny joke 
     - get some motivational tips
     - indulge in some fun activity.
    """
    prompt=ChatPromptTemplate.from_template(template=temp,
                                            input_variable=['problem'])

    activity_suggestor_chain=prompt|llm|StrOutputParser()
    activity_suggestor=activity_suggestor_chain.invoke({'problem':problem})

    state["key"]["activity_suggestor"]=activity_suggestor
    return state


