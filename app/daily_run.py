"""Generate an approval-ready daily batch. Demo mode works without paid API credentials."""
import asyncio, uuid
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
from sqlalchemy import select
from app.config import settings
from app.db import SessionLocal
from app.models import ProductionRun, Topic, ContentDraft
from app.kafka_bus import publish_event
from app.render import render_short
from app.audio import generate_voiceover
from app.demo import get_demo_batch, demo_report

async def generate_with_agents(run_id):
    from agents import Runner
    from app.agents import trend_scout, script_writer, fact_checker, video_producer, managing_editor
    today = datetime.now(ZoneInfo(settings.timezone)).date()
    trend = await Runner.run(trend_scout, f"Find at least {settings.shorts_per_day * 2} timely, verified gaming topics for today ({today}). Target audience: gaming fans in India and worldwide. Include GTA 6, gaming industry, EA FC, WWE games and Football Manager. Include source URLs. Avoid topics requiring unlicensed footage.")
    topics = trend.final_output.topics
    if not topics:
        raise RuntimeError("Trend Scout returned no usable topics")
    with SessionLocal() as db:
        for t in topics:
            db.add(Topic(run_id=run_id, title=t.title, angle=t.angle, category=t.category, trend_score=t.trend_score, freshness_hours=t.freshness_hours, sources=t.sources))
        db.commit()
    chosen = topics[:settings.shorts_per_day]
    result = await Runner.run(script_writer, f"Create exactly {len(chosen)} Shorts scripts from these candidates. Return 25-60 second narration, visual beats and metadata. Candidates: {[t.model_dump() for t in chosen]}")
    scripts = result.final_output.scripts
    checked = await Runner.run(fact_checker, "Independently fact-check every material claim. Verify source URLs and rights risks. Scripts: " + str([s.model_dump() for s in scripts]))
    reports = checked.final_output.reports
    pairs = [(s, reports[i]) for i, s in enumerate(scripts) if i < len(reports) and reports[i].approved_for_draft and not reports[i].rights_flags]
    if not pairs:
        raise RuntimeError("No scripts passed fact and rights checks")
    produced = await Runner.run(video_producer, "Prepare render-ready original typography/diagram visuals for these scripts. " + str([s.model_dump() for s, _ in pairs]))
    editorial = await Runner.run(managing_editor, "Check distinctness, truthfulness and rights-safe visuals. Never publish. Batch: " + str([s.model_dump() for s in produced.final_output.scripts]))
    # Keep matching by topic title; no draft is made without a passing fact-check report.
    report_map = {s.topic_title.casefold(): r for s, r in pairs}
    return [(s, report_map.get(s.topic_title.casefold())) for s in produced.final_output.scripts]

async def main():
    today = datetime.now(ZoneInfo(settings.timezone)).date()
    with SessionLocal() as db:
        existing = db.scalar(select(ProductionRun).where(ProductionRun.run_date == today))
        if existing and existing.status == "COMPLETED":
            print(f"Run already completed for {today}: {existing.id}")
            return
        run = existing or ProductionRun(run_date=today, requested_count=settings.shorts_per_day, status="STARTED")
        run.status = "STARTED"
        db.add(run); db.commit(); db.refresh(run)
        run_id = run.id

    try:
        if settings.demo_mode:
            batch = [(s, demo_report(s)) for s in get_demo_batch(settings.shorts_per_day)]
        else:
            if not settings.openai_api_key:
                raise RuntimeError("OPENAI_API_KEY is missing. Add it to .env or enable DEMO_MODE.")
            batch = await generate_with_agents(run_id)
        created = 0
        with SessionLocal() as db:
            for script, report in batch:
                if not report or not report.approved_for_draft or report.rights_flags:
                    continue
                draft_id = str(uuid.uuid4())
                audio_path = generate_voiceover(draft_id, script.narration)
                video_path = render_short(draft_id, script.title, script.narration, script.visual_beats, audio_path)
                draft = ContentDraft(
                    id=uuid.UUID(draft_id), run_id=run_id, title=script.title, hook=script.hook,
                    script=script.narration, duration_target_seconds=script.duration_seconds,
                    platform_metadata={"youtube_description": script.youtube_description, "instagram_caption": script.instagram_caption, "facebook_caption": script.facebook_caption, "hashtags": script.hashtags, "visual_beats": script.visual_beats},
                    fact_check=report.model_dump() if hasattr(report, "model_dump") else report.__dict__,
                    rights_status="ORIGINAL_ONLY", review_status="PENDING_REVIEW", video_path=video_path, audio_path=audio_path
                )
                db.add(draft); db.flush()
                publish_event("draft.created", {"draft_id": draft_id, "run_id": str(run_id), "video_path": video_path})
                created += 1
            run = db.get(ProductionRun, run_id)
            run.produced_count = created
            run.status = "COMPLETED" if created else "FAILED"
            run.completed_at = datetime.now(timezone.utc)
            db.commit()
        print(f"Created {created} drafts for human review. Nothing was published.")
    except Exception as exc:
        with SessionLocal() as db:
            run = db.get(ProductionRun, run_id)
            if run:
                run.status = "FAILED"
                run.error = str(exc)[:4000]
                run.completed_at = datetime.now(timezone.utc)
                db.commit()
        raise

if __name__ == "__main__":
    asyncio.run(main())
