import os
import time
from dotenv import load_dotenv
from typing import Dict,TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,START,END
from Execution_Graph.Nodes.problem_finder import ProblemFinder
from Execution_Graph.Nodes.context_decider import ContextDecider
from Execution_Graph.Nodes.context_using_vectorstore import ContextUsingVectorStore
from Execution_Graph.Nodes.transform_query_web_search import TransformQueryForWebSearch
from Execution_Graph.Nodes.transform_query_vectorstore import QueryTransformationForVectorStore
from Execution_Graph.Nodes.web_search import WebSearch
from Execution_Graph.Nodes.response_generation import ResponseGeneration
from Execution_Graph.Edge_Conditions.choosing_context import ContextChooser
from Execution_Graph.Nodes.fallback import Fallback
from Execution_Graph.Edge_Conditions.choosing_problem import ProblemChooser
from retriever import Retriever
from load_data_source import LoadDataSource
load_dotenv()



class GraphState(TypedDict):
    key: Dict[str,any]
    history: Annotated[list,add_messages]

graph=StateGraph(GraphState)

#Nodes:
graph.add_node("problem_finder",ProblemFinder)
graph.add_node("context_decider",ContextDecider)
graph.add_node("context_from_vectorstore",ContextUsingVectorStore)
graph.add_node("transform_query_web_search",TransformQueryForWebSearch)
graph.add_node("transform_query_vectorstore",QueryTransformationForVectorStore)
graph.add_node("web_search",WebSearch)
graph.add_node("generation",ResponseGeneration)
graph.add_node("fallback",Fallback)
graph.set_entry_point("problem_finder")

#Edges:
graph.add_edge(START,"problem_finder")
graph.add_conditional_edges(
    "problem_finder",
    ProblemChooser,
    {
        "fallback":"fallback",
        "problem":"context_decider"
    }
)

graph.add_conditional_edges(
    "context_decider",
    ContextChooser,
    {
        "web_search":"transform_query_web_search",
        "vectorstore":"transform_query_vectorstore"
    }

)
graph.add_edge("transform_query_web_search","web_search")
graph.add_edge("web_search","generation")
graph.add_edge("transform_query_vectorstore","context_from_vectorstore")
graph.add_edge("context_from_vectorstore","generation")
graph.add_edge("generation",END)
graph.add_edge("fallback",END)

#Memory:
memory=MemorySaver()

app=graph.compile(checkpointer=memory)
config={"configurable":{"thread_id":1}}


try:
    if os.path.exists("graph.png"):
        print("Image already existed")

    else:
        img = app.get_graph().draw_mermaid_png()
        with open("graph.png", "wb") as file:
            file.write(img)
        print("Image stored successfully!!!")

except Exception as e:
    print(e)


urls=LoadDataSource(filepath="web_urls.txt")
retriever=Retriever(urls)
while True:
    user_response=input("User:")

    inputs={"key":{
        "user_response":user_response,
        "retriever":retriever
    },
    "history":[("user",user_response)]
    }

    for output in app.stream(inputs,config,stream_mode="values"):
        for key,value in output.items():
            if key in ["generation","fallback"]:
                print(f"AI:{value['key']['ai_response']}")

            time.sleep(3)

