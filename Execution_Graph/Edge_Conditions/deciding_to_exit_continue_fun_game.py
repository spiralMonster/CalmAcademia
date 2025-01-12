def ExitOrContinueFunGame(state):
    fun_game_state=state["key"]["fun_game_state"]
    fun_game_type=state["key"]["fun_game"]["type"]

    if fun_game_state=="Continue":
        if fun_game_type=="I_spy":
            return "continuing_to_I_spy_game"

        else:
            return "continuing_to_other_games"

    else:
        return "exit"