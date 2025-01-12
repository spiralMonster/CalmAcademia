import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
load_dotenv()

def ExternalHelp(state):
    problem=state["key"]["problem"]
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )
    tool = TavilySearchResults(
        max_results=3,
        search_depth="advanced",
        include_raw_content=True,
        include_answer=True,
        include_images=False,
        api_key=os.environ["TAVILY_API_KEY"]
    )

    template="""
    The user is dealing with {problem} problem.
    You have to provide the contact and details about the organizations and services that will help the user
    to overcome the problem.
    You the following reference:
    {external_help_reference}
    """

    external_help_ref=tool.invoke({"query":f"Organizations and services helping to overcome {problem} problems."})

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['problem','external_help_reference'])

    external_help_chain=prompt|llm|StrOutputParser()
    external_help=external_help_chain.invoke({
        "problem":problem,
        "external_help_reference":external_help_ref
    })

    state["key"]["ai_response"]=external_help
    return state