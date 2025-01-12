import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from Execution_Graph.Nodes.helping_user_by_specs import HelpingUserBySpecs
load_dotenv()

def HelpingUserBy(state):
    interactions=state["key"]["interaction"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    ).with_structured_output(HelpingUserBySpecs)

    template="""
    Analyze the interaction between the user and ai agent.
    Then decide the state of the mind of user.
    If you feel that a simple fun activity can cheer up the user then recommend activity.
    If you feel that the user is not in right state of mind and activity cannot help them.Then recommend external help.
    Or else if you feel that everything is fine then don't recommend anything.
    The interactions are as follows:
    {interactions}
    """

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['interactions'])

    helping_chain=prompt|llm
    help=helping_chain.invoke({'interactions':interactions}).help

    state["key"]["help"]=help
    return state