# webhook_handler.py
from .risk_engine import analyze

def handle_webhook(payload):
    if payload.get("object_kind") != "merge_request":
        return {"error": "unsupported event"}

    changes = payload.get("changes", [])
    result = analyze(changes)

    response = {
        "title": payload.get("object_attributes", {}).get("title", "Unknown MR"),
        "risk_score": result.score,
        "reasons": result.reasons,
    }

    response["comment"] = format_mr_comment(response)

    return response
    
def format_mr_comment(result):
    score = result["risk_score"]
    reasons = result["reasons"]

    comment = "🚨 MR Risk Analysis\n\n"
    comment += f"Risk Score: {score}\n\n"

    if reasons:
        comment += "Reasons:\n"
        for r in reasons:
            comment += f"- {r}\n"
    else:
        comment += "No significant risks detected.\n"

    return comment

