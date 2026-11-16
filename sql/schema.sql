CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS production_runs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_date DATE NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'STARTED',
  requested_count INTEGER NOT NULL DEFAULT 5,
  produced_count INTEGER NOT NULL DEFAULT 0,
  error TEXT,
  started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  completed_at TIMESTAMPTZ,
  UNIQUE(run_date)
);

CREATE TABLE IF NOT EXISTS topics (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID REFERENCES production_runs(id) ON DELETE CASCADE,
  title TEXT NOT NULL,
  angle TEXT NOT NULL,
  category VARCHAR(64) NOT NULL,
  trend_score NUMERIC(5,2) NOT NULL DEFAULT 0,
  freshness_hours INTEGER,
  sources JSONB NOT NULL DEFAULT '[]'::jsonb,
  status VARCHAR(32) NOT NULL DEFAULT 'DISCOVERED',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS content_drafts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  run_id UUID REFERENCES production_runs(id) ON DELETE CASCADE,
  topic_id UUID REFERENCES topics(id) ON DELETE SET NULL,
  title TEXT NOT NULL,
  hook TEXT NOT NULL,
  script TEXT NOT NULL,
  duration_target_seconds INTEGER NOT NULL DEFAULT 40,
  platform_metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
  fact_check JSONB NOT NULL DEFAULT '{}'::jsonb,
  rights_status VARCHAR(32) NOT NULL DEFAULT 'ORIGINAL_ONLY',
  review_status VARCHAR(32) NOT NULL DEFAULT 'PENDING_REVIEW',
  rejection_reason TEXT,
  video_path TEXT,
  audio_path TEXT,
  thumbnail_path TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  reviewed_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS assets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  draft_id UUID REFERENCES content_drafts(id) ON DELETE CASCADE,
  asset_type VARCHAR(32) NOT NULL,
  asset_path TEXT NOT NULL,
  source_url TEXT,
  licence_url TEXT,
  rights_status VARCHAR(32) NOT NULL DEFAULT 'NEEDS_REVIEW',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS publishing_records (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  draft_id UUID NOT NULL REFERENCES content_drafts(id) ON DELETE CASCADE,
  platform VARCHAR(32) NOT NULL,
  status VARCHAR(32) NOT NULL DEFAULT 'NOT_CONFIGURED',
  platform_post_id TEXT,
  published_url TEXT,
  published_at TIMESTAMPTZ,
  error TEXT,
  UNIQUE(draft_id, platform)
);

CREATE TABLE IF NOT EXISTS analytics_snapshots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  draft_id UUID NOT NULL REFERENCES content_drafts(id) ON DELETE CASCADE,
  platform VARCHAR(32) NOT NULL,
  captured_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  views BIGINT NOT NULL DEFAULT 0,
  likes BIGINT NOT NULL DEFAULT 0,
  comments BIGINT NOT NULL DEFAULT 0,
  shares BIGINT NOT NULL DEFAULT 0,
  avg_view_seconds NUMERIC(8,2),
  raw_metrics JSONB NOT NULL DEFAULT '{}'::jsonb
);

CREATE INDEX IF NOT EXISTS idx_drafts_review ON content_drafts(review_status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_topics_run ON topics(run_id);
CREATE INDEX IF NOT EXISTS idx_analytics_draft ON analytics_snapshots(draft_id, captured_at DESC);
