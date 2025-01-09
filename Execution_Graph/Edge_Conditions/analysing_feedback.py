def FeedbackAnalyzer(state):
    activity_feedback=state["key"]["activity_feedback"]

    if activity_feedback=="satisfied":
        return "satisfied"

    else:
        return "not_satisfied"
