from .state import ClassificationState

MAX_RETRIES = 3


def route_after_validation(state: ClassificationState) -> str:
    last_msg = state["messages"][-1] if state["messages"] else ""
    if "FAILED" in str(last_msg):
        return "context_reset" if state.get("retry_count", 0) < MAX_RETRIES else "commit"
    return "human_review"


def route_after_review(state: ClassificationState) -> str:
    if state.get("human_approved"):
        return "commit"
    return "context_reset" if state.get("retry_count", 0) < MAX_RETRIES else "commit"
