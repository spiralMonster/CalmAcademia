from typing import Literal
from pydantic import BaseModel,Field

class ProblemFinderOptions(BaseModel):
    problem: Literal['Exam_pressure','Low_marks','Family_pressure',
                     'Performance_anxiety',' Homesickness','Relationship_problems',
                     'Money_issues','Future_anxiety','Others'] = Field(description="""
                     The problems faced by the student.
                     """)