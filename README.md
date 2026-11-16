# GAME ON 60 — Approval-first content studio

**Status:** local MVP verified in demo mode. Five original short-form video drafts have been generated, stored in SQLite, and served by the local review dashboard. No videos have been published.

## What is implemented

- Six specialist agent definitions: Managing Editor, Trend Scout, Script Writer, Fact Checker/Rights Gate, Video Producer, Growth Analyst.
- Demo mode that runs without an API key and generates five original editorial scripts.
- OpenAI Agents SDK live-mode pipeline (requires API key, API billing, and current model access).
- Original typography-based 9:16 MP4 rendering with FFmpeg/Pillow.
- Optional OpenAI TTS integration.
- SQLite local database by default; PostgreSQL schema and Docker Compose for a later deployment.
- Kafka-compatible event adapter; local JSONL fallback when Kafka is not installed/running.
- Local FastAPI review dashboard with preview, captions, fact-check report, approve and reject.
- Approval only records the human decision. Publishing adapters are intentionally not implemented/enabled.

## Quick start — Windows (PowerShell)

Prerequisites: Python 3.11+, FFmpeg on PATH. Docker is not required for demo mode.

```powershell
Copy-Item .env.example .env
# Keep DEMO_MODE=true and ENABLE_TTS=false for a no-API-cost smoke test.
.\scripts\run-local.ps1
```

Then open **http://127.0.0.1:8090**. The script installs dependencies, creates the local database, generates five draft MP4s and starts the dashboard. It binds to loopback only; do not expose this unauthenticated development dashboard to the internet.

Manual commands:

```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e .
python -m app.db_init
python -m app.daily_run
uvicorn app.api:app --host 127.0.0.1 --port 8090
```

## Enable live AI agents

1. Set `DEMO_MODE=false` in `.env`.
2. Add an API key in `OPENAI_API_KEY`.
3. Set `OPENAI_MODEL` to a model available to your API project.
4. Install the declared dependencies with `pip install -e .` (includes `openai-agents` and OpenAI client).
5. Run `python -m app.daily_run`.

ChatGPT subscriptions and API billing are separate. Set project-level API spend limits before enabling live runs. TTS is separately controlled by `ENABLE_TTS=true` and consumes API budget.

## Local Kafka / PostgreSQL (optional)

`docker compose up -d` starts PostgreSQL and Redpanda for integration testing. To use PostgreSQL, change `DATABASE_URL` in `.env` to the connection string shown in `.env.example`'s previous PostgreSQL setup or your own credentials. Set `KAFKA_BOOTSTRAP_SERVERS=localhost:19092`.

SQLite and JSONL are the default low-friction local mode. The event adapter falls back to `output/events.jsonl` if Kafka is unavailable.

## Daily automation

For laptop-based testing, use Windows Task Scheduler to run `python -m app.daily_run` daily while the laptop is awake and the virtual environment is available. The dashboard must be running separately when you review drafts. For unattended cloud runs, deploy a scheduled ECS task or Lambda/EventBridge + SQS architecture; that deployment is not yet provisioned.

## Content rights and platform controls

- Default visuals are original text/diagram cards. No game footage or creator clips are downloaded.
- Do not assume Rockstar fan-content guidance grants commercial monetization rights. Obtain written commercial permission or use independently licensed material.
- Every current factual claim needs source verification. Demo scripts are evergreen editorial examples, not verified breaking news.
- Human approval is mandatory. There is no publisher implementation and no OAuth token handling yet.
- Before cloud deployment: add authentication, authorization, CSRF protection, secrets management, encrypted storage, signed media URLs, rate limits, audit logs, idempotency, retries, dead-letter handling and cost alarms.

## Known MVP limitations

- Demo videos use original animated typography/scene cards; they are not gameplay captures or cinematic AI video.
- Demo narration is silent unless TTS is enabled with an API key.
- Live agent orchestration requires API credentials and network access.
- Cloud infrastructure, platform OAuth, analytics ingestion and auto-publishing remain future milestones.
- Five/day is a target, not a reason to lower factual, originality or rights standards.

## Budget strategy

Keep development local and demo-mode free. Add API usage only after the format is validated. For the first cloud pilot, use EventBridge + SQS + S3 + short-lived compute rather than Amazon MSK; continuously running Kafka infrastructure is incompatible with a ₹2,000/month target. Set AWS Budgets and API spend caps before deployment. Check regional pricing and free-tier eligibility before provisioning.
