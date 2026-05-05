from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from .state import ClassificationState
from .nodes import (
    intent_resolution_node, classification_node, validation_node,
    human_review_node, commit_node, context_reset_node,
)
from .routing import route_after_validation, route_after_review


def build_graph():
    """Assemble the classification state machine."""
    graph = StateGraph(ClassificationState)

    graph.add_node("intent_resolution", intent_resolution_node)
    graph.add_node("classify", classification_node)
    graph.add_node("validate", validation_node)
    graph.add_node("human_review", human_review_node)
    graph.add_node("commit", commit_node)
    graph.add_node("context_reset", context_reset_node)

    graph.add_edge(START, "intent_resolution")
    graph.add_edge("intent_resolution", "classify")
    graph.add_edge("classify", "validate")
    graph.add_conditional_edges("validate", route_after_validation)
    graph.add_conditional_edges("human_review", route_after_review)
    graph.add_edge("context_reset", "classify")
    graph.add_edge("commit", END)

    return graph.compile(checkpointer=MemorySaver())


if __name__ == "__main__":
    app = build_graph()
    config = {"configurable": {"thread_id": "demo-001"}}

    print("\n🤖 LangGraph HITL Classification Demo")
    print("Type an asset name to classify (e.g., customer_ssn, order_total, card_number)\n")

    asset = input("Asset to classify: ").strip() or "customer_ssn"
    result = app.invoke({"messages": [asset], "retry_count": 0}, config)

    print("\n✅ Final State:")
    print(f"   Classification: {result['classification']}")
    print(f"   Confidence:     {result['confidence']}")
    print(f"   Approved:       {result['human_approved']}")
    print(f"\n📋 Message Trail:")
    for msg in result["messages"]:
        print(f"   {msg}")
