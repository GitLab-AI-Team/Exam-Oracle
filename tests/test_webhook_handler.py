from app.risk_engine import analyze
from app.webhook_handler import handle_webhook

# webhook payload test

def test_handle_webhook_basic():
    payload = {
    "object_kind": "merge_request",
    "object_attributes": {
        "title": "Update auth logic",
        "iid": 42
    },
    "project": {
        "id": 123
    }
}

    result = handle_webhook(payload)

    assert result["risk_score"] >= 1
    assert "title" in result
    assert "reasons" in result
    
def test_handle_webhook_wrong_event():
    payload = {"object_kind": "push"}
    result = handle_webhook(payload)
    assert "error" in result
    
def test_handle_webhook_missing_fields():
    payload = {"object_kind": "merge_request"}
    result = handle_webhook(payload)
    assert result["risk_score"] == 0
    
    