# Scheduled Common Workflows

Typical use cases and workflows for the Scheduled AI scheduling agent.

## 1. Inbound Scheduling Request

When a contact emails you to set up a meeting:

1. Scheduled detects the scheduling intent in the email thread
2. Checks your Google Calendar for open slots in your preferred windows
3. Drafts a reply suggesting 2-3 available times (with timezone awareness)
4. You review the draft in Gmail and hit Send

## 2. Follow-Up Handling

When a proposed time is rejected or ignored:

1. Scheduled detects the follow-up or counter-proposal
2. Re-checks calendar for alternative availability
3. Drafts an updated reply with new time options

## 3. Group Meeting Coordination

When scheduling a meeting with multiple attendees:

1. Scheduled identifies all recipients and their roles
2. Proposes times that accommodate the group's known preferences
3. Drafts a reply that addresses each attendee by name if appropriate

## 4. Onboarding / Preference Bootstrap

On initial setup:

1. Run `python -m scheduler.onboarding`
2. Scheduled reads the last 2 months of Gmail history
3. Learns your typical meeting patterns, preferred times, and writing style
4. Stores preferences for future drafts (no raw emails stored on servers)

## 5. Autopilot Mode

For fully automated scheduling:

1. Enable autopilot in the web frontend settings
2. Scheduled will send draft replies automatically without manual review
3. You receive a notification of each auto-sent scheduling reply
