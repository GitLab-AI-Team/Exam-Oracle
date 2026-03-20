# webhook_handler.py
from .risk_engine import analyze

def handle_webhook(payload):
    if payload.get("object_kind") != "merge_request":
        return {"error": "unsupported event"}

    changes = payload.get("changes", [])
    result = analyze(changes)

    return {
        "title": payload.get("object_attributes", {}).get("title", "Unknown MR"),
        "risk_score": result.score,
        "reasons": result.reasons,
    }