def ContextChooser(state):
    context=state["key"]["context_decider"]
    if context=='web_search':
        return "web_search"
    else:
        return "vectorstore"