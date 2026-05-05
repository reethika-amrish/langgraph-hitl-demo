from .state import ClassificationState
from .tools import classify_asset, ClassifyAssetInput, query_catalog, CatalogQueryInput

MAX_RETRIES = 3


def intent_resolution_node(state: ClassificationState) -> dict:
    """Parse user request and extract classification target."""
    last_msg = state["messages"][-1] if state["messages"] else ""
    asset = last_msg if isinstance(last_msg, str) else str(last_msg)
    return {
        "asset_name": asset,
        "messages": [f"[Intent] Resolving classification request for: {asset}"]
    }


def classification_node(state: ClassificationState) -> dict:
    """Run classification with tool calling (mocked — no LLM needed)."""
    # Step 1: Check catalog first
    catalog_result = query_catalog(CatalogQueryInput(query=state["asset_name"]))

    # Step 2: Run classification tool
    result = classify_asset(ClassifyAssetInput(
        asset_name=state["asset_name"],
        asset_type="column",
        sample_values=[]
    ))

    catalog_note = ""
    if catalog_result["found"]:
        catalog_note = f" (catalog match: {catalog_result['result']['domain']} domain)"

    return {
        "classification": result.classification,
        "confidence": result.confidence,
        "reasoning": result.reasoning + catalog_note,
        "messages": [f"[Classify] {result.classification} (confidence: {result.confidence}){catalog_note}"]
    }


def validation_node(state: ClassificationState) -> dict:
    """Multi-checkpoint validation of classification output."""
    errors = []
    if state["classification"] not in ("CDE", "PII", "NON_SENSITIVE"):
        errors.append(f"Invalid classification: {state['classification']}")
    if not (0.0 <= state["confidence"] <= 1.0):
        errors.append(f"Invalid confidence: {state['confidence']}")
    if len(state.get("reasoning", "")) < 10:
        errors.append("Reasoning too short")

    if errors:
        return {"messages": [f"[Validation] FAILED: {'; '.join(errors)}"]}
    return {"messages": [f"[Validation] PASSED — {state['classification']} at {state['confidence']}"]}


def human_review_node(state: ClassificationState) -> dict:
    """HITL gate — in production this calls LangGraph interrupt().
    Here we simulate with console input."""
    print("\n" + "=" * 50)
    print("  HUMAN-IN-THE-LOOP REVIEW GATE")
    print("=" * 50)
    print(f"  Asset:          {state['asset_name']}")
    print(f"  Classification: {state['classification']}")
    print(f"  Confidence:     {state['confidence']}")
    print(f"  Reasoning:      {state['reasoning']}")
    print("=" * 50)

    decision = input("  Decision (approve/reject): ").strip().lower()
    approved = decision == "approve"

    return {
        "human_approved": approved,
        "messages": [f"[HITL] Human {'approved' if approved else 'rejected'} classification"]
    }


def commit_node(state: ClassificationState) -> dict:
    """Commit approved classification to catalog."""
    return {
        "messages": [f"[Commit] {state['asset_name']} → {state['classification']} committed to enterprise catalog"]
    }


def context_reset_node(state: ClassificationState) -> dict:
    """Clear context to prevent bias on retry."""
    new_retry = state.get("retry_count", 0) + 1
    return {
        "messages": [f"[Reset] Context cleared. Retry {new_retry}/{MAX_RETRIES}"],
        "classification": "",
        "confidence": 0.0,
        "reasoning": "",
        "human_approved": False,
        "retry_count": new_retry
    }
