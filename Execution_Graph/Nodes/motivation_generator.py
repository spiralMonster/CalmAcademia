import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


def MotivationGenerator(state):
    problem=state["key"]["user_problem"]

    llm=ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
        api_key=os.environ['GOOGLE_GEMINI_API_KEY']
    )
    tool=TavilySearchResults(
        max_results=3,
        search_depth="advanced",
        include_raw_content=True,
        include_answer=True,
        include_images=False,
        api_key=os.environ["TAVILY_API_KEY"]
    )

    template="""
    The user is dealing with {problem} problem.
    You have to motivate the user by giving them some motivational tips and stories.
    Try giving motivational stories related to their problem.
    Use the following motivational stories as reference
    {reference_motivation}
    """

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['problem','reference_jokes'])

    reference_motivation=tool.invoke({"query":f"Motivational stories about people dealing with {problem} problem."})

    motivation_generator_chain=prompt|llm|StrOutputParser()

    motivation=motivation_generator_chain.invoke({
        'problem':problem,
        'reference_jokes':reference_motivation
    })

    state["key"]["ai_response"]=motivation
    return state


