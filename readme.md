# MR Risk Scout (MVP)

Built for GitLab Duo / Hackathon Prototype

A lightweight FastAPI service that analyzes GitLab Merge Requests, assigns a simple risk score based on file changes, and posts a single summary comment back to the MR.

## Features
- Detects high-risk changes (e.g. CI configs, migrations)
- Computes a cumulative risk score
- Posts/updates a single MR comment
- Debug endpoint for local testing (`/debug/analyze`)

## Setup
1. Create a GitLab Personal Access Token with `api` scope
2. Copy `.env.example` → `.env` and fill in values

## Install
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

## Run
python server.py

## Test (local)
POST to:
http://127.0.0.1:8000/debug/analyze
