def AnalyzingUserResponse(state):
    user_response_analysis=state["key"]["user_response_analysis"]

    if user_response_analysis=="activity":
        return "asking_for_activity"

    else:
        return "no_activity"