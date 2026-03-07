from typing import Optional, Dict, Any, List
from .config import settings
from .gitlab_client import GitLabClient
from .risk_engine import RiskResult


def format_comment(mr_title: str, result: RiskResult) -> str:
    marker = settings.risk_scout_comment_marker
    lines: List[str] = []
    lines.append(marker)
    lines.append("## MR Risk Scout 🤖")
    lines.append(f"**Risk:** {result.score}/10 ({result.level})")
    lines.append("")
    lines.append("**Top signals**")
    for r in result.reasons[:5]:
        lines.append(f"- {r}")
    lines.append("")
    lines.append("**What I checked (MVP)**")
    lines.append(f"- MR title: {mr_title}")
    lines.append(f"- Files changed: {result.stats.get('file_count')}")
    lines.append(f"- Approx churn: {result.stats.get('approx_churn')}")
    lines.append(f"- Risky files matched: {result.stats.get('risky_files_count')}")
    lines.append("")
    lines.append("_This is MVP rules-only. Next: pipeline status, CODEOWNERS, and LLM reasoning._")
    return "\n".join(lines)


async def upsert_risk_comment(
    gl: GitLabClient,
    project_id: int,
    mr_iid: int,
    body: str,
) -> Dict[str, Any]:
    # Find existing note containing marker
    notes = await gl.list_mr_notes(project_id, mr_iid)
    marker = settings.risk_scout_comment_marker

    existing_note_id: Optional[int] = None
    for note in notes:
        if marker in (note.get("body") or ""):
            existing_note_id = note.get("id")
            break

    if existing_note_id is None:
        return await gl.create_mr_note(project_id, mr_iid, body)
    return await gl.update_mr_note(project_id, mr_iid, existing_note_id, body)