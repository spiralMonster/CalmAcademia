import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.user_satisfaction_specs import UserSatisfactionSpecs
load_dotenv()

def UserSatisfaction(state):
    history=state["history"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(UserSatisfactionSpecs)

    template="""
    Given the history of interaction between the user and ai decide whether the user is satisfied or not.
    History of interaction:
    {history}
    """
    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['history'])

    user_satisfaction_chain=prompt|llm
    user_sat=user_satisfaction_chain.invoke({'history':history}).user_satisfaction

    state["key"]["user_satisfaction"]=user_sat
    return state
