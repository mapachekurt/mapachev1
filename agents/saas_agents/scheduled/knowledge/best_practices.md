# Scheduled Best Practices

Recommended patterns and practices for operating the Scheduled AI scheduling agent.

## Privacy & Data Handling

- Scheduled stores **no email content or calendar events** on external servers
- All raw data stays within Google's ecosystem (Gmail + Calendar)
- Only learned preferences (e.g., preferred meeting times, writing style signals) are persisted

## Draft-Only by Default

- Always run in **draft mode** initially — Scheduled writes drafts you review before sending
- Enable autopilot only after validating that draft quality meets your standards
- Keep a review habit for the first few weeks to catch edge cases

## Scheduling Preferences

- Allow the onboarding module to bootstrap from at least 2 months of Gmail history for best results
- Explicitly configure buffers (e.g., 30-minute gaps between meetings) in the settings UI
- Block recurring unavailability (e.g., "no meetings on Fridays") in Google Calendar directly

## Self-Hosting Security

- Store `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, and `ANTHROPIC_API_KEY` in environment variables — never hard-code them
- Use a secrets manager (e.g., GCP Secret Manager, AWS Secrets Manager) in production
- Restrict OAuth scopes to the minimum required (Gmail + Calendar read/write)

## Reliability

- Run the email watcher (`scheduler.watcher`) as a supervised process (e.g., systemd, Cloud Run, or Kubernetes)
- Set up health check monitoring on the control plane endpoint (`/health`)
- Use GCP Pub/Sub webhooks for low-latency email event delivery rather than polling
