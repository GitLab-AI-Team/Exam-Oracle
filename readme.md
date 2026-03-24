# MR Risk Scout (MVP)

A tiny FastAPI webhook service that listens for GitLab Merge Request events,
computes a basic risk score from diffs, and posts/updates a single MR comment.

## Setup

1) Create a GitLab Personal Access Token with API scope.
2) Copy `.env.example` to `.env` and fill it out.

## Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt