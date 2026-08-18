"""
History Router
===============
Endpoints for browsing past analysis records.
"""

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.db.database import get_db
from session.models.analysis import AnalysisRecord
from session.schemas.analysis import HistoryResponse, HistoryItem

router = APIRouter()


# ─────────────────────────────────────────────
# GET /api/history/ — Paginated history list
# ─────────────────────────────────────────────

@router.get(
    "/",
    response_model=HistoryResponse,
    summary="Get paginated analysis history",
)
def get_history(
    page:     int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=50, description="Items per page"),
    language: str = Query(default=None, description="Filter by language"),
    status:   str = Query(default=None, description="Filter by status"),
    db:       Session = Depends(get_db),
):
    """
    Returns paginated list of all past analyses.
    Supports filtering by language and status.
    """
    query = db.query(AnalysisRecord).order_by(desc(AnalysisRecord.created_at))

    # Apply filters
    if language:
        query = query.filter(AnalysisRecord.language == language.lower())
    if status:
        query = query.filter(AnalysisRecord.status == status.lower())

    total = query.count()
    records = query.offset((page - 1) * per_page).limit(per_page).all()

    items = [
        HistoryItem(
            id=r.id,
            title=r.title,
            language=r.language,
            error_count=r.error_count,
            quality_score=r.quality_score,
            lines_of_code=r.lines_of_code,
            status=r.status,
            created_at=r.created_at,
        )
        for r in records
    ]

    return HistoryResponse(items=items, total=total, page=page, per_page=per_page)


# ─────────────────────────────────────────────
# DELETE /api/history/ — Clear all history
# ─────────────────────────────────────────────

@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete all history records",
)
def clear_history(db: Session = Depends(get_db)):
    db.query(AnalysisRecord).delete()
    db.commit()
    return None


# ─────────────────────────────────────────────
# GET /api/history/stats — Summary stats
# ─────────────────────────────────────────────

@router.get(
    "/stats",
    summary="Get overall history statistics",
)
def get_stats(db: Session = Depends(get_db)):
    total     = db.query(func.count(AnalysisRecord.id)).scalar()
    avg_score = db.query(func.avg(AnalysisRecord.quality_score)).scalar()
    total_err = db.query(func.sum(AnalysisRecord.error_count)).scalar()
    languages = [
        row[0] for row in
        db.query(AnalysisRecord.language).distinct().all()
    ]
    return {
        "total_analyses":     total or 0,
        "avg_quality_score":  round(avg_score, 1) if avg_score else None,
        "total_errors_fixed": total_err or 0,
        "languages_used":     languages,
    }
