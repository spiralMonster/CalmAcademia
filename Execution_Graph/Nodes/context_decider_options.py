from typing import Literal
from pydantic import BaseModel,Field

class ContextDeciderOptions(BaseModel):
    context_decider: Literal['web_search','vectorstore'] = Field(description="""
    Choose the context either from web search or vectorstore
    """)