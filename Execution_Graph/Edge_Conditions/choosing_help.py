def ChoosingHelp(state):
    help=state["key"]["help"]

    if help=="By_activity":
        return "activity"

    elif help=="By_external_help":
        return "external_help"

    else:
        return "No_help_needed"
