from pydantic import BaseModel, Field

# ── Tool Schemas (Pydantic-validated) ──

class ClassifyAssetInput(BaseModel):
    asset_name: str = Field(description="Name of the data asset")
    asset_type: str = Field(description="Type: column, table, or dataset")
    sample_values: list[str] = Field(default=[], description="Sample data values")

class ClassifyAssetOutput(BaseModel):
    classification: str = Field(description="CDE, PII, or NON_SENSITIVE")
    confidence: float = Field(ge=0.0, le=1.0)
    reasoning: str = Field(description="Step-by-step reasoning")

class CatalogQueryInput(BaseModel):
    query: str = Field(description="Search query for catalog")

class BusinessTermInput(BaseModel):
    asset_name: str
    domain: str = Field(description="Business domain context")


# ── Mock Tool Implementations ──
# In production: these call enterprise catalog APIs via MCP

MOCK_CATALOG = {
    "customer_ssn": {"classification": "PII", "domain": "customer", "sensitivity": "high"},
    "order_total": {"classification": "NON_SENSITIVE", "domain": "sales", "sensitivity": "low"},
    "card_number": {"classification": "CDE", "domain": "payment", "sensitivity": "critical"},
    "email_address": {"classification": "PII", "domain": "customer", "sensitivity": "high"},
}

def classify_asset(input: ClassifyAssetInput) -> ClassifyAssetOutput:
    """Mock classification based on asset naming patterns."""
    name = input.asset_name.lower()
    if any(k in name for k in ["ssn", "passport", "email", "phone", "address"]):
        return ClassifyAssetOutput(classification="PII", confidence=0.95,
            reasoning=f"Asset '{input.asset_name}' matches PII patterns (personal identifiers)")
    elif any(k in name for k in ["card", "cvv", "account_number", "routing"]):
        return ClassifyAssetOutput(classification="CDE", confidence=0.92,
            reasoning=f"Asset '{input.asset_name}' matches CDE patterns (cardholder data)")
    else:
        return ClassifyAssetOutput(classification="NON_SENSITIVE", confidence=0.88,
            reasoning=f"Asset '{input.asset_name}' does not match sensitive data patterns")

def query_catalog(input: CatalogQueryInput) -> dict:
    """Mock catalog lookup."""
    match = MOCK_CATALOG.get(input.query.lower(), None)
    if match:
        return {"found": True, "result": match}
    return {"found": False, "result": None}

def generate_business_term(input: BusinessTermInput) -> dict:
    """Mock business term generation."""
    return {"term": f"{input.domain}_{input.asset_name}",
            "definition": f"Business term for {input.asset_name} in {input.domain} domain"}
