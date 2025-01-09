def ActivityChooser(state):
    activity_decider=state["key"]["activity_decider"]

    if activity_decider=="Joke":
        return "joke"

    elif activity_decider=="Motivation":
        return "motivation"

    else:
        return "fun_game"