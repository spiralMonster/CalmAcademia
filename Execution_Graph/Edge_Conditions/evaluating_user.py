def EvaluatingUser(state):
    num_questions=state["num_questions_asked"]

    if num_questions%7==0:
        return "user_evaluation"
    else:
        return "end"