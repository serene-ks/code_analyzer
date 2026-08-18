"""
Pydantic Schemas
=================
Request/Response data validation using Pydantic v2.
Separates API contract from DB model.
"""

from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


# ─────────────────────────────────────────────
# Request Schemas (what the client sends)
# ─────────────────────────────────────────────

class AnalyzeRequest(BaseModel):
    """Sent by frontend when user submits code for analysis."""
    title:    str  = Field(default="Untitled Analysis", max_length=255)
    language: str  = Field(..., description="Programming language of the code")
    code:     str  = Field(..., min_length=1, description="Code to analyze")

    @field_validator("language")
    @classmethod
    def normalize_language(cls, v: str) -> str:
        """Lowercase & strip whitespace from language name."""
        return v.strip().lower()

    @field_validator("code")
    @classmethod
    def code_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Code cannot be empty or whitespace only.")
        return v

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Bubble Sort Fix",
                "language": "python",
                "code": "def bubble_sort(arr):\n    for i in range(len(arr)):\n        for j in range(len(arr)-i):\n            if arr[j] > arr[j+1]:\n                arr[j], arr[j+1] = arr[j+1], arr[j]"
            }
        }
    }


# ─────────────────────────────────────────────
# Response Schemas (what the API returns)
# ─────────────────────────────────────────────

class ErrorDetail(BaseModel):
    """Represents a single error found in code."""
    line:        Optional[int]  = None
    type:        str            = ""   # e.g. "IndexError", "SyntaxError"
    message:     str            = ""
    severity:    str            = "error"   # error | warning | info


class AnalyzeResponse(BaseModel):
    """Full analysis result returned to the client."""
    id:               int
    title:            str
    language:         str
    original_code:    str
    corrected_code:   Optional[str]  = None
    optimized_code:   Optional[str]  = None
    errors_found:     List[ErrorDetail] = []
    suggestions:      Optional[str]  = None
    explanation:      Optional[str]  = None
    error_count:      int            = 0
    quality_score:    Optional[float] = None
    lines_of_code:    int            = 0
    status:           str
    created_at:       datetime

    model_config = {"from_attributes": True}


class HistoryItem(BaseModel):
    """Lightweight record shown in the history list."""
    id:            int
    title:         str
    language:      str
    error_count:   int
    quality_score: Optional[float]
    lines_of_code: int
    status:        str
    created_at:    datetime

    model_config = {"from_attributes": True}


class HistoryResponse(BaseModel):
    """Paginated history response."""
    items:    List[HistoryItem]
    total:    int
    page:     int
    per_page: int


class HomeStats(BaseModel):
    """Dashboard stats shown on the Home page."""
    total_analyses:     int
    total_errors_fixed: int
    languages_used:     List[str]
    avg_quality_score:  Optional[float]
    recent_analyses:    List[HistoryItem]
