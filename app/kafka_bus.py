"""Best-effort event adapter. Kafka is optional in local/demo mode."""
import json
from pathlib import Path
from app.config import settings


def publish_event(event_type: str, payload: dict) -> None:
    event = {"type": event_type, "payload": payload}
    try:
        from confluent_kafka import Producer
        producer = Producer({"bootstrap.servers": settings.kafka_bootstrap_servers})
        producer.produce(settings.kafka_topic, json.dumps(event).encode("utf-8"))
        producer.flush(5)
    except Exception:
        # Keep local development functional without a running broker.
        path = Path(settings.output_dir) / "events.jsonl"
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")
