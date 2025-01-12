def FunGameCycle(state):
    fun_game=state["key"]["fun_game"]["type"]

    if fun_game=="Would_you_rather":
        return "would_you_rather_cycle"

    elif fun_game=="I_spy":
        return "i_spy_cycle"

    else:
        return "never_have_i_ever_cycle"