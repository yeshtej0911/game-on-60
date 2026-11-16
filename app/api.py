from datetime import datetime, timezone
from zoneinfo import ZoneInfo
from pathlib import Path
from uuid import UUID
import subprocess, sys
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select, func
from app.db import SessionLocal
from app.models import ContentDraft, ProductionRun
from app.config import settings

app = FastAPI(title="GAME ON 60 Studio", version="0.2.0", description="Local approval-first gaming content studio")
STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return FileResponse(STATIC_DIR / "index.html")

@app.get("/health")
def health():
    return {"status": "ok", "service": "game-on-60-review-api", "mode": "demo" if settings.demo_mode else "live"}

@app.get("/summary")
def summary():
    with SessionLocal() as db:
        pending = db.scalar(select(func.count()).select_from(ContentDraft).where(ContentDraft.review_status == "PENDING_REVIEW")) or 0
        approved = db.scalar(select(func.count()).select_from(ContentDraft).where(ContentDraft.review_status == "APPROVED")) or 0
        rejected = db.scalar(select(func.count()).select_from(ContentDraft).where(ContentDraft.review_status == "REJECTED")) or 0
        latest = db.scalar(select(ProductionRun).order_by(ProductionRun.started_at.desc()).limit(1))
        return {"pending": pending, "approved": approved, "rejected": rejected, "latest_run": {"id": str(latest.id), "date": str(latest.run_date), "status": latest.status, "produced": latest.produced_count, "error": latest.error} if latest else None}

@app.post("/runs/start")
def start_run():
    today = datetime.now(ZoneInfo(settings.timezone)).date()
    with SessionLocal() as db:
        existing = db.scalar(select(ProductionRun).where(ProductionRun.run_date == today))
        if existing and existing.status == "COMPLETED":
            raise HTTPException(409, "Today's production run is already complete.")
        if existing and existing.status == "STARTED":
            raise HTTPException(409, "Today's production run is already running.")
    root = Path(__file__).resolve().parents[1]
    log_path = root / settings.output_dir / "daily-run.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log = log_path.open("a", encoding="utf-8")
    subprocess.Popen([sys.executable, "-m", "app.daily_run"], cwd=root, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
    return {"status": "STARTED", "message": "Production job started. Refresh this dashboard in a few minutes."}

@app.get("/drafts")
def list_drafts(status: str = "PENDING_REVIEW"):
    with SessionLocal() as db:
        query = select(ContentDraft).order_by(ContentDraft.created_at.desc())
        if status.upper() != "ALL":
            query = query.where(ContentDraft.review_status == status.upper())
        rows = db.scalars(query).all()
        return [_serialize(x) for x in rows]

def _serialize(x):
    return {"id": str(x.id), "title": x.title, "hook": x.hook, "script": x.script, "video_path": x.video_path, "video_url": f"/media/{Path(x.video_path).name}" if x.video_path else None, "fact_check": x.fact_check, "platform_metadata": x.platform_metadata, "review_status": x.review_status, "created_at": x.created_at.isoformat() if x.created_at else None, "rejection_reason": x.rejection_reason}

@app.get("/drafts/{draft_id}")
def get_draft(draft_id: UUID):
    with SessionLocal() as db:
        x = db.get(ContentDraft, draft_id)
        if not x: raise HTTPException(404, "Draft not found")
        return _serialize(x)

@app.get("/media/{filename}")
def get_media(filename: str):
    # Only serve generated MP4 files from the configured output directory.
    if Path(filename).name != filename or not filename.endswith(".mp4"):
        raise HTTPException(400, "Invalid media filename")
    path = (Path(settings.output_dir) / filename).resolve()
    base = Path(settings.output_dir).resolve()
    if base not in path.parents or not path.is_file():
        raise HTTPException(404, "Video not found")
    return FileResponse(path, media_type="video/mp4")

@app.post("/drafts/{draft_id}/approve")
def approve_draft(draft_id: UUID):
    with SessionLocal() as db:
        x = db.get(ContentDraft, draft_id)
        if not x: raise HTTPException(404, "Draft not found")
        if x.review_status != "PENDING_REVIEW": raise HTTPException(409, "Draft is not pending review")
        if not x.video_path or not Path(x.video_path).is_file(): raise HTTPException(409, "Video asset is missing")
        x.review_status = "APPROVED"
        x.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        return {"id": str(x.id), "status": "APPROVED", "message": "Approval recorded. Publishing remains disabled until platform integrations are configured."}

@app.post("/drafts/{draft_id}/reject")
def reject_draft(draft_id: UUID, reason: str = "Rejected by owner"):
    with SessionLocal() as db:
        x = db.get(ContentDraft, draft_id)
        if not x: raise HTTPException(404, "Draft not found")
        if x.review_status != "PENDING_REVIEW": raise HTTPException(409, "Draft is not pending review")
        x.review_status = "REJECTED"
        x.rejection_reason = reason[:1000]
        x.reviewed_at = datetime.now(timezone.utc)
        db.commit()
        return {"id": str(x.id), "status": "REJECTED"}
