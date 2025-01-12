def DecidingFlowOfCalmAcademia(state):
    fun_game_initializer=state["key"]["fun_game_initializer"]
    fun_game_phase=state["key"]["fun_game_phase"]
    i_spy_replayer=state["key"]["i_spy_replayer"]
    activity_phase=state["key"]["activity_phase"]

    if fun_game_initializer:
        return "fun_game_initializer"

    elif activity_phase:
        return "starting_activity"

    elif fun_game_phase:
        return "managing_fun_game"

    elif i_spy_replayer:
        return "deciding_replaying_i_spy"



    else:
        return "query_answering"
