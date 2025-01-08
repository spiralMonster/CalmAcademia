import os
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
load_dotenv()

def WebSearch(state):
    query=state["key"]["transformed_query"]
    tool=TavilySearchResults(
        max_results=3,
        search_depth="advanced",
        include_raw_content=True,
        include_answer=True,
        include_images=False,
        api_key=os.environ["TAVILY_API_KEY"]
    )
    docs=tool.invoke({"query":query})
    docs=[d.content for d in docs]
    state["key"]["retrieved_docs"]=docs
    print("Context retrieved from Web")
    return state