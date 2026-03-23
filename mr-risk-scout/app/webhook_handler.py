from .risk_engine import analyze

def fetch_mr_changes(project_id, mr_iid):
    """
    Prototype stub for GitLab diff fetching.
    In production, this would call the GitLab Merge Requests API.
    """
    return [
        {"new_path": "auth/login.py", "diff": "+ changed auth logic"},
        {"new_path": ".gitlab-ci.yml", "diff": "+ updated pipeline"},
    ]

def handle_webhook(payload):
    if payload.get("object_kind") != "merge_request":
        return {"error": "unsupported event"}

    title = payload.get("object_attributes", {}).get("title", "Unknown MR")
    project_id = payload.get("project", {}).get("id")
    mr_iid = payload.get("object_attributes", {}).get("iid")

    changes = payload.get("changes")

    if changes is None:
        if project_id is not None and mr_iid is not None:
            changes = fetch_mr_changes(project_id, mr_iid)
        else:
            response = {
                "title": title,
                "risk_score": 0,
                "reasons": ["No change data available and insufficient MR metadata to fetch diffs."],
            }
            response["comment"] = format_mr_comment(response)
            return response

    result = analyze(changes)

    response = {
        "title": title,
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