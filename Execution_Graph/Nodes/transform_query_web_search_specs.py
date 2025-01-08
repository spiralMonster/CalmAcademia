from pydantic import BaseModel,Field

class TransformQueryForWebSearchSpecs(BaseModel):
    transformed_query:str =Field(description="""
    Query to get relevant results from web search
    """)