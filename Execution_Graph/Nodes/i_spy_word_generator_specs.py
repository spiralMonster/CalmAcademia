from pydantic import BaseModel,Field

class ISpyWordGeneratorSpecs(BaseModel):
    word: str=Field(description="""
    The generated word which the user has to guess.
    """)