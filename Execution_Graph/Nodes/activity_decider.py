import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.activity_decider_specs import ActivityDeciderSpecs

def ActivityDecider(state):
    user_response=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(ActivityDeciderSpecs)

    sys_msg="""
    Based upon the user response decide whether the user want to:
     - hear a joke
     - get some motivational tips
     - indulge in some fun-game
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{user_response}")
        ]
    )

    activity_decider_chain=prompt|llm
    activity_decider=activity_decider_chain.invoke({"user_response":user_response}).activity_decider

    state["key"]["activity_decider"]=activity_decider
    return state