from typing import Literal
from pydantic import BaseModel,Field

class UserResponseAnalyserSpecs(BaseModel):
    user_response_analysis: Literal["activity","no_activity"]=Field(description="""
    Whether the user want activity or not.
    """)