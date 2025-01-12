def DecidingReplayISpy(state):
    decider=state["key"]["i_spy_replay_decider"]

    if decider=="replay":
        return "replaying_i_spy"

    else:
        return "not_replaying_i_spy"