from typing import TypedDict, Annotated
from operator import add


class ClassificationState(TypedDict):
    """Full state flowing through the classification graph."""
    messages: Annotated[list, add]  # append reducer — messages accumulate
    asset_name: str
    classification: str            # CDE | PII | NON_SENSITIVE
    confidence: float              # 0.0 - 1.0
    reasoning: str
    human_approved: bool
    retry_count: int
