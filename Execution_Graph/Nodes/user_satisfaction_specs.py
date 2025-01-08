from typing import Literal
from pydantic import BaseModel,Field

class UserSatisfactionSpecs(BaseModel):
    user_satisfaction:Literal["Yes","No"]=Field(description="""
    Whether the user is satisfied or not in the interaction.
    """)