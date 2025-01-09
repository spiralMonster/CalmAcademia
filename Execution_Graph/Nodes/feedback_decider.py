import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.feedback_decider_specs import FeedbackDeciderSpecs

def FeedbackDecider(state):
    user_response=state["key"]["user_response"]

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(FeedbackDeciderSpecs)

    sys_msg="""
    Given the user response decide whether the user is satisfied or not by the activity performed by the ai agent.
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{user_response}")
        ]
    )

    feedback_decider_chain=prompt|llm
    activity_feedback=feedback_decider_chain.invoke({"user_response":user_response}).activity_feedback

    state["key"]["activity_feedback"]=activity_feedback
    return state