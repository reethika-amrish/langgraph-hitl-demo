# LangGraph HITL Demo — Data Classification Pattern

> Demonstrates the **agentic AI orchestration pattern** I built for an enterprise data classification system — using LangGraph state machines, HITL workflows, and tool calling with Pydantic validation.

## What This Showcases

This is a simplified, self-contained prototype of the **Agentic AI–Powered Data Classification System** I designed for enterprise data integrity — no API keys or LLMs required.

### Patterns Demonstrated

| Pattern | Implementation |
|---|---|
| **LangGraph State Machine** | Graph with nodes, conditional edges, and state transitions |
| **HITL (Human-in-the-Loop)** | Graph pauses at review gate, resumes on human decision |
| **Checkpointing** | Full state persistence for pause/resume across sessions |
| **Tool Calling** | Pydantic-validated tool schemas for classification, catalog query |
| **Context Reset** | Clears agent context on rejection to prevent bias on retry |
| **Conditional Routing** | Dynamic edge selection based on confidence and approval |

## Architecture

```mermaid
graph TD
    A[👤 User Request] --> B[Intent Resolution]
    B --> C[Classification Agent]
    C --> D{Confidence Check}
    D -->|High Confidence| E[HITL Review Gate]
    D -->|Low Confidence| C
    
    C --> T[🔧 Tool Calling<br/>Pydantic Schemas]
    T --> CAT[(Enterprise Catalog)]
    
    E -->|✅ Approved| F[Commit to Catalog]
    E -->|❌ Rejected| G[Context Reset]
    G --> C
    
    F --> H[✅ Classification Complete]

    style A fill:#1e3a5f,stroke:#64ffda,color:#e2e8f0
    style C fill:#2d1b69,stroke:#a78bfa,color:#e2e8f0
    style E fill:#4a3000,stroke:#fbbf24,color:#e2e8f0
    style F fill:#064e3b,stroke:#34d399,color:#e2e8f0
    style G fill:#4c0519,stroke:#f87171,color:#e2e8f0
    style T fill:#1e293b,stroke:#94a3b8,color:#e2e8f0
    style CAT fill:#1e293b,stroke:#94a3b8,color:#e2e8f0
```

## Running

```bash
pip install langgraph langchain-core pydantic
python -m src.graph
```

No API keys needed — all LLM calls are mocked with deterministic responses.

## Project Structure

```
src/
├── state.py       # TypedDict state definition with reducers
├── tools.py       # Pydantic-schema tool definitions (mocked)
├── nodes.py       # Node functions — classify, review, commit, reset
├── routing.py     # Conditional edge logic
└── graph.py       # Full graph assembly + demo runner
```

## From My Resume

> *"Designed a multi-agent AI system using LangGraph state-machine orchestration for automated CDE/PII classification — with intent resolution, scope validation, checkpoint-based HITL review, and MCP-based enterprise catalog integration."*

This repo distills that production system into a runnable pattern.
