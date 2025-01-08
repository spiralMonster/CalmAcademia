import os
import time
from dotenv import load_dotenv
from typing import Dict,TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,START,END
from Execution_Graph.Nodes.route_decider import RouteDecider
from Execution_Graph.Nodes.problem_finder import ProblemFinder
from Execution_Graph.Nodes.context_decider import ContextDecider
from Execution_Graph.Nodes.context_using_vectorstore import ContextUsingVectorStore
from Execution_Graph.Nodes.transform_query_web_search import TransformQueryForWebSearch
from Execution_Graph.Nodes.transform_query_vectorstore import QueryTransformationForVectorStore
from Execution_Graph.Nodes.web_search import WebSearch
from Execution_Graph.Nodes.response_generation import ResponseGeneration
from Execution_Graph.Nodes.fallback import Fallback
from Execution_Graph.Nodes.user_satisfaction import UserSatisfaction
from Execution_Graph.Nodes.activity_suggestor import ActivitySuggestor
from Execution_Graph.Edge_Conditions.choosing_route import RouteChoosing
from Execution_Graph.Edge_Conditions.user_evaluation import UserEvaluation
from Execution_Graph.Edge_Conditions.choosing_context import ContextChooser
from Execution_Graph.Edge_Conditions.choosing_problem import ProblemChooser
from Execution_Graph.Edge_Conditions.choosing_activity import ActivityChooser

from retriever import Retriever
from load_data_source import LoadDataSource
load_dotenv()



class GraphState(TypedDict):
    key: Dict[str,any]
    history: Annotated[list,add_messages]
    num_questions_asked: int

graph=StateGraph(GraphState)

#Nodes:
graph.add_node("route_decider",RouteDecider)
graph.add_node("problem_finder",ProblemFinder)
graph.add_node("context_decider",ContextDecider)
graph.add_node("context_from_vectorstore",ContextUsingVectorStore)
graph.add_node("transform_query_web_search",TransformQueryForWebSearch)
graph.add_node("transform_query_vectorstore",QueryTransformationForVectorStore)
graph.add_node("web_search",WebSearch)
graph.add_node("generation",ResponseGeneration)
graph.add_node("fallback",Fallback)
graph.add_node("user_satisfaction",UserSatisfaction)
graph.add_node("activity_suggestor",ActivitySuggestor)
graph.set_entry_point("route_decider")

#Edges:
graph.add_edge(START,"route_decider")

graph.add_conditional_edges(
    "route_decider",
    RouteChoosing,
    {
        "answering_query_route":"problem_finder",
        "activity_route":END
    }

)
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

graph.add_conditional_edges(
    "generation",
    UserEvaluation,
    {
        "user_evaluation":"user_satisfaction",
        "end":END
    }
)

graph.add_conditional_edges(
    "user_satisfaction",
    ActivityChooser,
    {
        "yes":END,
        "no":"activity_suggestor"
    }
)
graph.add_edge("activity_suggestor",END)
graph.add_edge("fallback",END)

#Memory:
memory=MemorySaver()

app=graph.compile(checkpointer=memory)



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
ind=1
thread_id=1

while True:
    user_response=input("User:")

    if ind%4==0:
        thread_id+=1

    config = {"configurable": {"thread_id": thread_id}}
    inputs={"key":{
        "user_response":user_response,
        "retriever":retriever
    },
    "history":[("user",user_response)],
    "num_questions_asked":ind
    }
    ind+=1

    for output in app.stream(inputs,config,stream_mode="values"):
        for key,value in output.items():
            if key in ["generation","fallback"]:
                print(f"AI:{value['key']['ai_response']}")

            if key=="activity_suggestor":
                print(f"AI:{value['key']['activity_suggestor']}")

            time.sleep(3)

