def RouteChoosing(state):
    user_response_type=state["key"]["user_response_type"]

    if user_response_type=="Question":
        return "answering_query_route"

    else:
        return "activity_route"