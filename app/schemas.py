from pydantic import BaseModel, Field
from typing import Literal

class TopicCandidate(BaseModel):
    title: str
    angle: str
    category: str
    trend_score: float = Field(ge=0, le=100)
    freshness_hours: int = 24
    sources: list[str] = []

class TopicBatch(BaseModel):
    topics: list[TopicCandidate]

class VideoScript(BaseModel):
    topic_title: str
    title: str
    hook: str
    narration: str
    duration_seconds: int = Field(ge=25, le=60)
    visual_beats: list[str]
    youtube_description: str
    instagram_caption: str
    facebook_caption: str
    hashtags: list[str]

class ScriptBatch(BaseModel):
    scripts: list[VideoScript]

class ClaimCheck(BaseModel):
    claim: str
    status: Literal["VERIFIED", "UNVERIFIED", "FALSE", "OPINION"]
    evidence_url: str | None = None
    note: str

class FactCheckReport(BaseModel):
    approved_for_draft: bool
    claims: list[ClaimCheck]
    rights_flags: list[str]
    corrections: list[str]
    overall_note: str

class FactCheckBatch(BaseModel):
    reports: list[FactCheckReport]
