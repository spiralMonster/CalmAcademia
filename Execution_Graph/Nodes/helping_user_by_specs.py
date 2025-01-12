from typing import Literal
from pydantic import BaseModel,Field

class HelpingUserBySpecs(BaseModel):
    help: Literal["By_activity","By_external_help","None"]=Field(description="""
    How the user should be helped.
    """)