from typing import Literal
from pydantic import BaseModel,Field

class UserResponseAnalyserSpecs(BaseModel):
    user_response_analysis: Literal["Asking_for_activity","Feedback","Others"]=Field(description="""
    Whether the user response is about asking for an activity,giving feedback to performed activity
    or just any other response.
    """)