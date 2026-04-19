# Distill Chat Prompt

Use this prompt with a long ChatGPT conversation when you want to convert it into a durable summary for this repository.

```text
Please distill this conversation into a structured summary for a technical writing agent.

Focus only on durable guidance that should influence future writing. Ignore filler, repetition, pleasantries, and one-off side comments unless they reveal stable preferences.

Return Markdown using exactly these sections:

# Title
- date:
- source:

## Project

## Audience

## Principles

## Structural Decisions

## Terminology Preferences

## Reusable Phrasing

## Open Questions

## Evidence Notes

Rules:
- Prefer bullets over paragraphs unless a paragraph is clearer.
- Capture tensions or disagreements explicitly.
- Separate durable principles from temporary decisions.
- If the conversation contains contradictions, note them in Open Questions or Evidence Notes.
- Do not include the full original chat.
```
