from typing import Literal
from pydantic import BaseModel,Field

class FunGameManagerSpecs(BaseModel):
    fun_game_state: Literal["Continue","Exit"]=Field(description="""
    Whether to continue the fun game or exit it.
    """)