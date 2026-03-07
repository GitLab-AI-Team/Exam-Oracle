import httpx
from typing import Any, Dict, Optional


class GitLabClient:
    def __init__(self, base_url: str, token: str):
        self.base_url = base_url.rstrip("/")
        self.token = token

    def _headers(self) -> Dict[str, str]:
        return {"PRIVATE-TOKEN": self.token}

    async def get_mr(self, project_id: int, mr_iid: int) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def get_mr_changes(self, project_id: int, mr_iid: int) -> Dict[str, Any]:
        # Includes `changes`: [{old_path, new_path, diff, ...}, ...]
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/changes"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def list_mr_notes(self, project_id: int, mr_iid: int) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.get(url, headers=self._headers())
            r.raise_for_status()
            return r.json()

    async def create_mr_note(self, project_id: int, mr_iid: int, body: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.post(url, headers=self._headers(), data={"body": body})
            r.raise_for_status()
            return r.json()

    async def update_mr_note(self, project_id: int, mr_iid: int, note_id: int, body: str) -> Dict[str, Any]:
        url = f"{self.base_url}/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes/{note_id}"
        async with httpx.AsyncClient(timeout=30) as client:
            r = await client.put(url, headers=self._headers(), data={"body": body})
            r.raise_for_status()
            return r.json()