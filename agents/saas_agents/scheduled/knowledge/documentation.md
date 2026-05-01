# Scheduled Documentation

Official documentation and API reference.

Scheduled is an open-source AI scheduling agent from Fergana Labs that integrates with Gmail and Google Calendar to automate meeting scheduling workflows.

## Key Resources

- **GitHub Repository**: https://github.com/Fergana-Labs/scheduled
- **Self-Hosting Guide**: https://github.com/Fergana-Labs/scheduled/blob/main/docs/self-hosting.md
- **Blog Post**: https://x.com/samzliu/status/2034412249201443116

## Architecture

Scheduled consists of:

- **Email Watcher** (`scheduler.watcher`) — monitors Gmail for scheduling emails and creates drafts
- **Onboarding Module** (`scheduler.onboarding`) — backfills scheduling preferences from the last 2 months of Gmail history
- **Control Plane** (`scheduler.controlplane.server`) — FastAPI-based REST API for managing the agent
- **Frontend** (`web/`) — Next.js frontend for reviewing drafts and managing preferences

## Authentication

Scheduled uses Google OAuth 2.0 with the following scopes:
- Gmail read/write (for reading threads and writing drafts)
- Google Calendar read (for checking availability)

## Self-Hosted Quick Start

```bash
# Install
pip install -e ".[dev]"

# Configure
cp .env.example .env
# Fill in: GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, ANTHROPIC_API_KEY, DATABASE_URL

# Authenticate with Google
python -m scheduler.auth.google_auth

# Run onboarding (backfill calendar from last 2 months of Gmail)
python -m scheduler.onboarding

# Start the email watcher
python -m scheduler.watcher

# Start the control plane (API)
uvicorn scheduler.controlplane.server:app --host 0.0.0.0 --port 8080

# Start the frontend
cd web && NEXT_PUBLIC_CONTROL_PLANE_URL=http://localhost:8080 npm run dev
```
