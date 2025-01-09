def AnalyzingUserResponse(state):
    user_response_analysis=state["key"]["user_response_analysis"]

    if user_response_analysis=="Asking_for_activity":
        return "asking_for_activity"

    elif user_response_analysis=="Feedback":
        return "giving_feedback"

    else:
        return "general_response"