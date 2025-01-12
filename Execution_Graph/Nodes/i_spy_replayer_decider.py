import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.i_spy_replayer_decider_specs import ISpyReplayerDeciderSpecs
load_dotenv()

def ISpyReplayerDecider(state):
    user_response=state["key"]["user_response"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(ISpyReplayerDeciderSpecs)

    sys_msg="""
    Depending upon the user response decide whether the user has to replay the I spy game again or not.
    """
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system",sys_msg),
            ("human","{user_response}")
        ]
    )

    replayer_decider_chain=prompt|llm
    i_spy_replay_decider=replayer_decider_chain.invoke({"user_response":user_response}).replay_decider

    state["key"]["i_spy_replay_decider"]=i_spy_replay_decider
    return state
