import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def ISpyReplayer(state):
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )

    template="""
    The user has completed {game} game.
    Congratulate the user on completing the game and ask whether they want to play it again or not.
    """

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['game'])

    replayer_chain=prompt|llm|StrOutputParser()
    ai_response=replayer_chain.invoke({"game":"I spy"})

    state["key"]["ai_response"]=ai_response
    return state