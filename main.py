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
from Execution_Graph.Nodes.fallback import Fallback
from Execution_Graph.Nodes.helping_user_by import HelpingUserBy
from Execution_Graph.Nodes.activity_suggestor import ActivitySuggestor
from Execution_Graph.Nodes.user_response_analyser import UserResponseAnalyser
from Execution_Graph.Nodes.activity_decider import ActivityDecider
from Execution_Graph.Nodes.joke_generator import JokeGenerator
from Execution_Graph.Nodes.motivation_generator import MotivationGenerator
from Execution_Graph.Nodes.fun_game_generator import FunGameGenerator
from Execution_Graph.Nodes.fun_game_decider import FunGameDecider
from Execution_Graph.Nodes.providing_external_help import ExternalHelp
from Execution_Graph.Nodes.fun_game_manager import FunGameManager
from Execution_Graph.Nodes.would_you_rather_fun_game_question_asking import WouldYouRatherFunGameQuestionAsking
from Execution_Graph.Nodes.i_spy_word_generator import ISpyWordGenerator
from Execution_Graph.Nodes.i_spy_question_generator import ISpyQuestionGenerator
from Execution_Graph.Nodes.i_spy_manager import ISpyManger
from Execution_Graph.Nodes.i_spy_replayer import ISpyReplayer
from Execution_Graph.Nodes.i_spy_replayer_decider import ISpyReplayerDecider
from Execution_Graph.Nodes.analysing_user_response_in_fun_game import AnalyzingUserResponseDuringGame
from Execution_Graph.Nodes.service_initiator import ServiceInitiator
from Execution_Graph.Edge_Conditions.choosing_help import ChoosingHelp
from Execution_Graph.Edge_Conditions.evaluating_user import EvaluatingUser
from Execution_Graph.Edge_Conditions.choosing_context import ContextChooser
from Execution_Graph.Edge_Conditions.choosing_problem import ProblemChooser
from Execution_Graph.Edge_Conditions.analyzing_user_response import AnalyzingUserResponse
from Execution_Graph.Edge_Conditions.choosing_activity import ActivityChooser
from Execution_Graph.Edge_Conditions.deciding_flow_of_CalmAcademia import DecidingFlowOfCalmAcademia
from Execution_Graph.Edge_Conditions.deciding_to_exit_continue_fun_game import ExitOrContinueFunGame
from Execution_Graph.Edge_Conditions.fun_game_chooser import FunGameChooser
from Execution_Graph.Edge_Conditions.fun_game_cycle import FunGameCycle
from Execution_Graph.Edge_Conditions.deciding_flow_of_i_spy import DecidingFlowOfISpy
from Execution_Graph.Edge_Conditions.deciding_replay_i_spy import DecidingReplayISpy

from retriever import Retriever
from load_data_source import LoadDataSource
load_dotenv()



class GraphState(TypedDict):
    key: Dict[str,any]
    history: Annotated[list,add_messages]
    num_questions_asked: int

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
graph.add_node("helping_user_by",HelpingUserBy)
graph.add_node("activity_suggestor",ActivitySuggestor)
graph.add_node("user_response_analyzer",UserResponseAnalyser)
graph.add_node("activity_decider",ActivityDecider)
graph.add_node("joke_generator",JokeGenerator)
graph.add_node("motivation_generator",MotivationGenerator)
graph.add_node("external_help",ExternalHelp)
graph.add_node("fun_game_generator",FunGameGenerator)
graph.add_node("fun_game_decider",FunGameDecider)
graph.add_node("fun_game_manager",FunGameManager)
graph.add_node("would_you_rather_question_generator",WouldYouRatherFunGameQuestionAsking)
graph.add_node("i_spy_word_generator",ISpyWordGenerator)
graph.add_node("i_spy_question_generator",ISpyQuestionGenerator)
graph.add_node("i_spy_manager",ISpyManger)
graph.add_node("analyzing_user_response_during_game",AnalyzingUserResponseDuringGame)
graph.add_node("i_spy_replayer",ISpyReplayer)
graph.add_node("i_spy_replay_decider",ISpyReplayerDecider)
graph.add_node("service_initiator",ServiceInitiator)


#Edges:


graph.add_conditional_edges(
    START,
    DecidingFlowOfCalmAcademia,
    {
        "fun_game_initializer":"fun_game_decider",
        "starting_activity":"user_response_analyzer",
        "query_answering":"problem_finder",
        "managing_fun_game":"fun_game_manager",
        "deciding_replaying_i_spy":"i_spy_replay_decider"
    }
)



graph.add_conditional_edges(
    "i_spy_replay_decider",
    DecidingReplayISpy,
    {
      "replaying_i_spy":"i_spy_word_generator",
      "not_replaying_i_spy":"service_initiator"
    }
)

graph.add_conditional_edges(
    "fun_game_manager",
    ExitOrContinueFunGame,
    {
        "continuing_to_I_spy_game":"i_spy_manager",
        "continuing_to_other_games":"analyzing_user_response_during_game",
        "exit":"service_initiator"
    }

)

graph.add_conditional_edges(
    "i_spy_manager",
    DecidingFlowOfISpy,
    {
        "word_guessed":"i_spy_replayer",
        "word_not_guessed":"analyzing_user_response_during_game"
    }
)
graph.add_edge("i_spy_replayer",END)

graph.add_conditional_edges(
    "analyzing_user_response_during_game",
    FunGameCycle,
    {
        "would_you_rather_cycle":"would_you_rather_question_generator",
        "i_spy_cycle":"i_spy_question_generator"

    }
)

graph.add_conditional_edges(
    "fun_game_decider",
    FunGameChooser,
    {
        "Would_you_rather":"would_you_rather_question_generator",
        "I_spy":"i_spy_word_generator"
    }
)

graph.add_edge("i_spy_word_generator","i_spy_question_generator")
graph.add_edge("i_spy_question_generator",END)

graph.add_edge("would_you_rather_question_generator",END)


graph.add_conditional_edges(
    "user_response_analyzer",
    AnalyzingUserResponse,
    {
        "asking_for_activity":"activity_decider",
        "no_activity":"service_initiator"
    }
)

graph.add_conditional_edges(
    "activity_decider",
    ActivityChooser,
    {
        "joke":"joke_generator",
        "motivation":"motivation_generator",
        "fun_game":"fun_game_generator"
    }
)

graph.add_edge("joke_generator","service_initiator")
graph.add_edge("motivation_generator","service_initiator")
graph.add_edge("fun_game_generator",END)


graph.add_edge("external_help","service_initiator")

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
    EvaluatingUser,
    {
        "user_evaluation":"helping_user_by",
        "end":END
    }
)

graph.add_conditional_edges(
    "helping_user_by",
    ChoosingHelp,
    {
        "activity":"activity_suggestor",
        "external_help":"external_help",
        "No_help_needed":END
    }
)


graph.add_edge("activity_suggestor",END)
graph.add_edge("fallback",END)
graph.add_edge("service_initiator",END)

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

fun_game_initializer=False
fun_game_type=None
fun_game_question=None
fun_game_phase=False
i_spy_replayer=False
activity_phase=False
interactions=[]
problem=None
while True:
    user_response=input("User:")

    if ind%7==0:
        thread_id+=1
        interactions=[]

    config = {"configurable": {"thread_id": thread_id}}
    inputs={"key":{
        "user_response":user_response,
        "retriever":retriever,
        "user_problem":problem,
        "fun_game_initializer":fun_game_initializer,
        "activity_phase":activity_phase,
        "fun_game_phase":fun_game_phase,
        "i_spy_replayer":i_spy_replayer,
        "fun_game":{
            'type':fun_game_type,
            'question':fun_game_question
        },
        "interaction":interactions
    },
    "history":[("user",user_response)],
    "num_questions_asked":ind
    }


    for output in app.stream(inputs,config,stream_mode="values"):
        for key,value in output.items():
            if key in ["generation","fallback"]:
                interactions.append(value["key"]["history"])
                problem=value["key"]["problem"]
                ind+=1

            if key in ["generation","fallback","activity_suggestor","joke_generator","motivation_generator","external_help","i_spy_replayer","service_initiator"]:
                print(f"AI:{value['key']['ai_response']}")


            if key=="activity_suggestor":
                activity_phase=True

            if key=="fun_game_generator":
                print(f"AI:{value['key']['fun_game_generator']}")
                fun_game_initializer=True
                activity_phase=False

            if key=="fun_game_manager":
                fun_game_state=value["key"]["fun_game_state"]
                if fun_game_state=="Exit":
                    fun_game_phase=False

            if key=="i_spy_manager":
                user_answer=value["key"]["i_spy_user_answer"]
                if user_answer=="guessed":
                    i_spy_replayer=True

            if key=="i_spy_replay_decider":
                decider=value["key"]["i_spy_replay_decider"]
                if decider=="not_replay":
                    i_spy_replayer=False

            if key=="would_you_rather_question_generator":
                fun_game_initializer=False
                fun_game_phase=True
                fun_game_type="Would_you_rather"
                fun_game_question=value["key"]["would_you_rather_question"]
                print(f"AI:{value['key']['would_you_rather_question']}")

            elif key=="i_spy_question_generator":
                fun_game_initializer=False
                fun_game_phase=True
                fun_game_type="I_spy"
                word=value["key"]["i_spy_word"]
                asked_question=value["key"]["i_spy_question"]
                question=f"""
                The word to be guessed is: {word}.
                And the asked question is: {asked_question}
                         """
                fun_game_question=question
                print(f"AI:{asked_question}")


            time.sleep(3)

