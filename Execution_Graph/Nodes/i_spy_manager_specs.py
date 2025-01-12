from typing import Literal
from pydantic import BaseModel,Field

class ISpyManagerSpecs(BaseModel):
    user_answer: Literal["guessed","not_guessed"]=Field(description="""
    Whether the user has guessed or not guessed the word.
    """)