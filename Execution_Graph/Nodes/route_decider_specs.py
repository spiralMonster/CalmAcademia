from typing import Literal
from pydantic import BaseModel,Field

class RouteDeciderSpecs(BaseModel):
    user_response_type: Literal["Question","Answer"]=Field(description="""
    Whether the user is asking a question or giving answer to question.
    """)