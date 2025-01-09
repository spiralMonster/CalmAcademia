from typing import Literal
from pydantic import BaseModel,Field

class FeedbackDeciderSpecs(BaseModel):
    activity_feedback: Literal["satisfied","not_satisfied"]=Field(description="""
    Whether the user is satisfied or not by the activity performed by the ai agent.
    """)