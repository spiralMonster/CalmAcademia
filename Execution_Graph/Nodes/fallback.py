import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def Fallback(state):
    print("Fallback mechanism:")
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )
    user_query=state["key"]["user_response"]
    template="""
    You are a helpful chat assistant.Depending upon the user query answer appropriately.
    User query:
    {query}
    """
    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['query'])

    fallback_chain=prompt|llm|StrOutputParser()
    ai_response=fallback_chain.invoke({'query':user_query})

    state["key"]["ai_response"]=ai_response
    state["history"] = [("ai", ai_response)]

    return state