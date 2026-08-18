"""
Home Router
============
Returns dashboard stats for the home page.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, desc

from backend.db.database import get_db
from session.models.analysis import AnalysisRecord
from session.schemas.analysis import HomeStats, HistoryItem

router = APIRouter()


@router.get(
    "/stats",
    response_model=HomeStats,
    summary="Dashboard statistics for the home page",
)
def get_home_stats(db: Session = Depends(get_db)):
    """Returns aggregate stats + recent 5 analyses for the home page dashboard."""

    total_analyses = db.query(func.count(AnalysisRecord.id)).scalar() or 0
    total_errors   = db.query(func.sum(AnalysisRecord.error_count)).scalar() or 0
    avg_score_raw  = db.query(func.avg(AnalysisRecord.quality_score)).scalar()
    avg_score      = round(avg_score_raw, 1) if avg_score_raw else None

    languages = [
        row[0] for row in
        db.query(AnalysisRecord.language).distinct().all()
    ]

    recent_records = (
        db.query(AnalysisRecord)
        .order_by(desc(AnalysisRecord.created_at))
        .limit(5)
        .all()
    )

    recent = [
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
        for r in recent_records
    ]

    return HomeStats(
        total_analyses=total_analyses,
        total_errors_fixed=total_errors,
        languages_used=languages,
        avg_quality_score=avg_score,
        recent_analyses=recent,
    )
