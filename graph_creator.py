from graph_state import GraphState
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




def GraphCreator():
    graph = StateGraph(GraphState)

    # Nodes:

    graph.add_node("problem_finder", ProblemFinder)
    graph.add_node("context_decider", ContextDecider)
    graph.add_node("context_from_vectorstore", ContextUsingVectorStore)
    graph.add_node("transform_query_web_search", TransformQueryForWebSearch)
    graph.add_node("transform_query_vectorstore", QueryTransformationForVectorStore)
    graph.add_node("web_search", WebSearch)
    graph.add_node("generation", ResponseGeneration)
    graph.add_node("fallback", Fallback)
    graph.add_node("helping_user_by", HelpingUserBy)
    graph.add_node("activity_suggestor", ActivitySuggestor)
    graph.add_node("user_response_analyzer", UserResponseAnalyser)
    graph.add_node("activity_decider", ActivityDecider)
    graph.add_node("joke_generator", JokeGenerator)
    graph.add_node("motivation_generator", MotivationGenerator)
    graph.add_node("external_help", ExternalHelp)
    graph.add_node("fun_game_generator", FunGameGenerator)
    graph.add_node("fun_game_decider", FunGameDecider)
    graph.add_node("fun_game_manager", FunGameManager)
    graph.add_node("would_you_rather_question_generator", WouldYouRatherFunGameQuestionAsking)
    graph.add_node("i_spy_word_generator", ISpyWordGenerator)
    graph.add_node("i_spy_question_generator", ISpyQuestionGenerator)
    graph.add_node("i_spy_manager", ISpyManger)
    graph.add_node("analyzing_user_response_during_game", AnalyzingUserResponseDuringGame)
    graph.add_node("i_spy_replayer", ISpyReplayer)
    graph.add_node("i_spy_replay_decider", ISpyReplayerDecider)
    graph.add_node("service_initiator", ServiceInitiator)

    # Edges:

    graph.add_conditional_edges(
        START,
        DecidingFlowOfCalmAcademia,
        {
            "fun_game_initializer": "fun_game_decider",
            "starting_activity": "user_response_analyzer",
            "query_answering": "problem_finder",
            "managing_fun_game": "fun_game_manager",
            "deciding_replaying_i_spy": "i_spy_replay_decider"
        }
    )

    graph.add_conditional_edges(
        "i_spy_replay_decider",
        DecidingReplayISpy,
        {
            "replaying_i_spy": "i_spy_word_generator",
            "not_replaying_i_spy": "service_initiator"
        }
    )

    graph.add_conditional_edges(
        "fun_game_manager",
        ExitOrContinueFunGame,
        {
            "continuing_to_I_spy_game": "i_spy_manager",
            "continuing_to_other_games": "analyzing_user_response_during_game",
            "exit": "service_initiator"
        }

    )

    graph.add_conditional_edges(
        "i_spy_manager",
        DecidingFlowOfISpy,
        {
            "word_guessed": "i_spy_replayer",
            "word_not_guessed": "analyzing_user_response_during_game"
        }
    )
    graph.add_edge("i_spy_replayer", END)

    graph.add_conditional_edges(
        "analyzing_user_response_during_game",
        FunGameCycle,
        {
            "would_you_rather_cycle": "would_you_rather_question_generator",
            "i_spy_cycle": "i_spy_question_generator"

        }
    )

    graph.add_conditional_edges(
        "fun_game_decider",
        FunGameChooser,
        {
            "Would_you_rather": "would_you_rather_question_generator",
            "I_spy": "i_spy_word_generator"
        }
    )

    graph.add_edge("i_spy_word_generator", "i_spy_question_generator")
    graph.add_edge("i_spy_question_generator", END)

    graph.add_edge("would_you_rather_question_generator", END)

    graph.add_conditional_edges(
        "user_response_analyzer",
        AnalyzingUserResponse,
        {
            "asking_for_activity": "activity_decider",
            "no_activity": "service_initiator"
        }
    )

    graph.add_conditional_edges(
        "activity_decider",
        ActivityChooser,
        {
            "joke": "joke_generator",
            "motivation": "motivation_generator",
            "fun_game": "fun_game_generator"
        }
    )

    graph.add_edge("joke_generator", "service_initiator")
    graph.add_edge("motivation_generator", "service_initiator")
    graph.add_edge("fun_game_generator", END)

    graph.add_edge("external_help", "service_initiator")

    graph.add_conditional_edges(
        "problem_finder",
        ProblemChooser,
        {
            "fallback": "fallback",
            "problem": "context_decider"
        }
    )

    graph.add_conditional_edges(
        "context_decider",
        ContextChooser,
        {
            "web_search": "transform_query_web_search",
            "vectorstore": "transform_query_vectorstore"
        }

    )
    graph.add_edge("transform_query_web_search", "web_search")
    graph.add_edge("web_search", "generation")
    graph.add_edge("transform_query_vectorstore", "context_from_vectorstore")
    graph.add_edge("context_from_vectorstore", "generation")

    graph.add_conditional_edges(
        "generation",
        EvaluatingUser,
        {
            "user_evaluation": "helping_user_by",
            "end": END
        }
    )

    graph.add_conditional_edges(
        "helping_user_by",
        ChoosingHelp,
        {
            "activity": "activity_suggestor",
            "external_help": "external_help",
            "No_help_needed": END
        }
    )

    graph.add_edge("activity_suggestor", END)
    graph.add_edge("fallback", END)
    graph.add_edge("service_initiator", END)

    # Memory:
    memory = MemorySaver()

    app = graph.compile(checkpointer=memory)

    return app



