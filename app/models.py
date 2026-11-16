from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Date, DateTime, Integer, Numeric, ForeignKey, JSON, func
from sqlalchemy.dialects.postgresql import UUID
import uuid

class Base(DeclarativeBase): pass

class ProductionRun(Base):
    __tablename__ = "production_runs"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_date: Mapped[object] = mapped_column(Date, unique=True, nullable=False)
    status: Mapped[str] = mapped_column(String(32), default="STARTED")
    requested_count: Mapped[int] = mapped_column(Integer, default=5)
    produced_count: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    started_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    completed_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)

class Topic(Base):
    __tablename__ = "topics"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("production_runs.id"))
    title: Mapped[str] = mapped_column(Text)
    angle: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(64))
    trend_score: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    freshness_hours: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sources: Mapped[list] = mapped_column(JSON, default=list)
    status: Mapped[str] = mapped_column(String(32), default="DISCOVERED")
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())

class ContentDraft(Base):
    __tablename__ = "content_drafts"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    run_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("production_runs.id"))
    topic_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True), ForeignKey("topics.id"))
    title: Mapped[str] = mapped_column(Text)
    hook: Mapped[str] = mapped_column(Text)
    script: Mapped[str] = mapped_column(Text)
    duration_target_seconds: Mapped[int] = mapped_column(Integer, default=40)
    platform_metadata: Mapped[dict] = mapped_column(JSON, default=dict)
    fact_check: Mapped[dict] = mapped_column(JSON, default=dict)
    rights_status: Mapped[str] = mapped_column(String(32), default="ORIGINAL_ONLY")
    review_status: Mapped[str] = mapped_column(String(32), default="PENDING_REVIEW")
    rejection_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    video_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    audio_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    thumbnail_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[object] = mapped_column(DateTime(timezone=True), server_default=func.now())
    reviewed_at: Mapped[object | None] = mapped_column(DateTime(timezone=True), nullable=True)
