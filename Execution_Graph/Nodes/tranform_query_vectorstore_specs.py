from pydantic import BaseModel,Field

class TransformQueryForVectorStoreSpecs(BaseModel):
    transformed_query: str=Field(description="""
    The document with similar semantic meaning that of original query.
    """)