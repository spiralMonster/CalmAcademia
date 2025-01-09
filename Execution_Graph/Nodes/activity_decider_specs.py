from typing import Literal
from pydantic import BaseModel,Field

class ActivityDeciderSpecs(BaseModel):
    activity_decider: Literal["Joke","Motivation","Fun_game"]=Field(description="""
    Whether the user want to hear a joke, some motivation or just want to indulge in some fun activity.
    """)