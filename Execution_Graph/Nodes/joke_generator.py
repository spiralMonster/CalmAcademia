import os
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools import TavilySearchResults
from langchain_core.output_parsers import StrOutputParser
load_dotenv()


def JokeGenerator(state):
    problem=state["key"]["problem"]

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
    You have to cheer up the user by hearing them a joke.
    Try to generate a joke related to their problem but not by hurting them.
    Use the following jokes as reference:
    {reference_jokes}
    """

    prompt=ChatPromptTemplate.from_template(template=template,
                                            input_variable=['problem','reference_jokes'])

    reference_jokes=tool.invoke({"query":f"Jokes related to {problem}"})

    joke_generator_chain=prompt|llm|StrOutputParser()

    joke=joke_generator_chain.invoke({
        'problem':problem,
        'reference_jokes':reference_jokes
    })

    state["key"]["ai_response"]=joke
    return state


