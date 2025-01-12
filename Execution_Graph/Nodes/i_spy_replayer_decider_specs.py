from typing import Literal
from pydantic import BaseModel,Field

class ISpyReplayerDeciderSpecs(BaseModel):
    replay_decider:Literal["replay","not_replay"]=Field(description="""
    Whether to replay the I spy game or not.
    """)