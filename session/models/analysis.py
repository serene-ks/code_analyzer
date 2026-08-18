"""
SQLAlchemy ORM Models
======================
Defines all database tables.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum
from sqlalchemy.sql import func
import enum
from backend.db.database import Base


class LanguageEnum(str, enum.Enum):
    python = "python"
    javascript = "javascript"
    typescript = "typescript"
    java = "java"
    cpp = "cpp"
    c = "c"
    go = "go"
    rust = "rust"
    php = "php"
    ruby = "ruby"
    other = "other"


class AnalysisRecord(Base):
    """
    Stores every code analysis performed by the user.
    Each row = one analysis session.
    """
    __tablename__ = "analysis_records"

    id            = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title         = Column(String(255), nullable=False, default="Untitled Analysis")
    language      = Column(String(50), nullable=False, default="python")

    # User's original code
    original_code = Column(Text, nullable=False)

    # AI-generated outputs
    corrected_code   = Column(Text, nullable=True)   # Bug-fixed code
    optimized_code   = Column(Text, nullable=True)   # Performance-optimized code
    errors_found     = Column(Text, nullable=True)   # JSON list of errors
    suggestions      = Column(Text, nullable=True)   # AI suggestions (plain text)
    explanation      = Column(Text, nullable=True)   # What was wrong & why

    # Metrics
    error_count      = Column(Integer, default=0)
    quality_score    = Column(Float, nullable=True)  # 0-100 score from AI
    lines_of_code    = Column(Integer, default=0)

    # Status: pending | processing | completed | failed
    status        = Column(String(20), default="pending")

    # Timestamps (auto-managed)
    created_at    = Column(DateTime(timezone=True), server_default=func.now())
    updated_at    = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<AnalysisRecord id={self.id} lang={self.language} status={self.status}>"
