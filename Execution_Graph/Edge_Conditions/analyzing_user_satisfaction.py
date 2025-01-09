def AnalyzingUserSatisfaction(state):
    user_sat=state["key"]["user_satisfaction"]

    if user_sat=="Yes":
        return "yes"

    else:
        return "no"
