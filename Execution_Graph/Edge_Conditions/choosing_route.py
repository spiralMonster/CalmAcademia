def RouteChoosing(state):
    user_response_type=state["key"]["user_response_type"]

    if user_response_type=="Question":
        return "asking_question"

    else:
        return "answering_asked_question"