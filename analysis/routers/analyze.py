"""
Analyze Router
===============
Endpoints for submitting code for analysis and retrieving results.
"""

import json
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.db.database import get_db
from session.models.analysis import AnalysisRecord
from session.schemas.analysis import AnalyzeRequest, AnalyzeResponse, ErrorDetail
from models.services.gemini_service import analyze_with_gemini

router = APIRouter()

# ─────────────────────────────────────────────
# POST /api/analyze/ — Submit code for analysis
# ─────────────────────────────────────────────

@router.post(
    "/",
    response_model=AnalyzeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Submit code for AI analysis",
)
async def submit_analysis(payload: AnalyzeRequest, db: Session = Depends(get_db)):
    """
    Accepts code + language, runs Gemini AI analysis,
    saves result to DB, returns full AnalyzeResponse.
    """

    # Count lines
    lines_of_code = len([l for l in payload.code.splitlines() if l.strip()])

    # Create a DB record in "processing" state
    record = AnalysisRecord(
        title=payload.title,
        language=payload.language,
        original_code=payload.code,
        lines_of_code=lines_of_code,
        status="processing",
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    # Run Gemini analysis
    try:
        ai_result = await analyze_with_gemini(
            code=payload.code,
            language=payload.language,
            title=payload.title,
        )
    except Exception as e:
        record.status = "failed"
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis failed: {str(e)}",
        )

    # Parse errors list from AI result
    errors_raw = ai_result.get("errors", [])
    errors_json = json.dumps(errors_raw)

    # Update the record with AI results
    record.corrected_code = ai_result.get("corrected_code")
    record.optimized_code = ai_result.get("optimized_code")
    record.errors_found   = errors_json
    record.suggestions    = ai_result.get("suggestions")
    record.explanation    = ai_result.get("explanation")
    record.error_count    = len(errors_raw)
    record.quality_score  = ai_result.get("quality_score")
    record.status         = "completed"

    db.commit()
    db.refresh(record)

    return _build_response(record)


# ─────────────────────────────────────────────
# GET /api/analyze/{id} — Fetch a single result
# ─────────────────────────────────────────────

@router.get(
    "/{analysis_id}",
    response_model=AnalyzeResponse,
    summary="Get analysis result by ID",
)
def get_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with id={analysis_id} not found.",
        )
    return _build_response(record)


# ─────────────────────────────────────────────
# DELETE /api/analyze/{id} — Delete a record
# ─────────────────────────────────────────────

@router.delete(
    "/{analysis_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete an analysis record",
)
def delete_analysis(analysis_id: int, db: Session = Depends(get_db)):
    record = db.query(AnalysisRecord).filter(AnalysisRecord.id == analysis_id).first()
    if not record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Analysis with id={analysis_id} not found.",
        )
    db.delete(record)
    db.commit()
    return None


# ─────────────────────────────────────────────
# Helper: Convert DB model → Pydantic response
# ─────────────────────────────────────────────

def _build_response(record: AnalysisRecord) -> AnalyzeResponse:
    """Parse JSON errors from DB and build AnalyzeResponse."""
    errors: list[ErrorDetail] = []
    if record.errors_found:
        try:
            raw = json.loads(record.errors_found)
            errors = [ErrorDetail(**e) for e in raw]
        except (json.JSONDecodeError, TypeError):
            errors = []

    return AnalyzeResponse(
        id=record.id,
        title=record.title,
        language=record.language,
        original_code=record.original_code,
        corrected_code=record.corrected_code,
        optimized_code=record.optimized_code,
        errors_found=errors,
        suggestions=record.suggestions,
        explanation=record.explanation,
        error_count=record.error_count,
        quality_score=record.quality_score,
        lines_of_code=record.lines_of_code,
        status=record.status,
        created_at=record.created_at,
    )
