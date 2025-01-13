from typing import TypedDict,Dict,Annotated
from langgraph.graph.message import add_messages

class GraphState(TypedDict):
    key: Dict[str,any]
    history: Annotated[list,add_messages]
    num_questions_asked: int