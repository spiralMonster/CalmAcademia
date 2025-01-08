import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def ResponseGeneration(state):
    problem=state["key"]["problem"]
    user_query=state["key"]["user_response"]
    retrieved_docs=state["key"]["retrieved_docs"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )
    template="""
    The user is a student who is suffering through {problem} problem.
    Depending upon the user query and with the help of context provided answer appropriately.
    User Query:
    {user_query}
    Context:
    {retrieved_docs}
    """
    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['problem','user_query','retrieved_docs'])

    response_generation_chain=prompt|llm|StrOutputParser()
    ai_response=response_generation_chain.invoke({
        'problem':problem,
        'user_query':user_query,
        'retrieved_docs':retrieved_docs
    })

    state["key"]["ai_response"]=ai_response
    state["history"]=[("ai",ai_response)]

    print("AI response generated..")
    return state