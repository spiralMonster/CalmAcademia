def DecidingFlowOfISpy(state):
    user_answer=state["key"]["i_spy_user_answer"]

    if user_answer=="guessed":
        return "word_guessed"

    else:
        return "word_not_guessed"