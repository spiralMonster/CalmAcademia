from typing import Literal
from pydantic import BaseModel,Field

class FunGameDeciderSpecs(BaseModel):
    fun_game_type: Literal["Would_you_rather","I_spy","Never_have_I_ever"]=Field(description="""
    The fun game user want to play.
    """)