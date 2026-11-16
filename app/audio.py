from pathlib import Path
from app.config import settings


def generate_voiceover(draft_id: str, narration: str) -> str | None:
    if not settings.enable_tts:
        return None
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is missing; cannot generate narration")
    outdir = Path(settings.output_dir)
    outdir.mkdir(parents=True, exist_ok=True)
    audio_path = outdir / f"{draft_id}.mp3"
    from openai import OpenAI
    client = OpenAI(api_key=settings.openai_api_key)
    response = client.audio.speech.create(
        model=settings.tts_model,
        voice=settings.tts_voice,
        input=narration,
        response_format="mp3",
    )
    response.stream_to_file(str(audio_path))
    return str(audio_path)
