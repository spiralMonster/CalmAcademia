def FunGameChooser(state):
    fun_game_type=state["key"]["fun_game_type"]

    if fun_game_type=="Would_you_rather":
        return "Would_you_rather"

    elif fun_game_type=="I_spy":
        return "I_spy"

    else:
        return "Never_have_I_ever"