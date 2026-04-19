# Writing Agent Starter Repo

This repository is a practical starting point for turning long ChatGPT conversations about technical writing into a reusable writing system.

The workflow is intentionally simple:

1. Distill long chats into short, structured summaries.
2. Store those summaries in `data/chat_summaries/`.
3. Rebuild a shared context digest from all saved summaries.
4. Refresh a working outline that can evolve as your thinking changes.

This starter does not force a model provider yet. It gives you a clean local structure first, so later we can plug in OpenAI, another model, or a manual review loop without redoing the repository.

## What This Repo Gives You

- A place to save distilled chat summaries.
- A living outline in `workspace/outline.md`.
- A style and editorial brief area in `workspace/`.
- A small local script that reads summaries and refreshes shared working files.
- Prompt templates for summarizing old chats consistently.

## Repository Layout

```text
.
|-- README.md
|-- .gitignore
|-- data/
|   `-- chat_summaries/
|       `-- 2026-04-18-sample-summary.md
|-- prompts/
|   |-- distill_chat_prompt.md
|   `-- writer_system_prompt.md
|-- scripts/
|   `-- writing_agent.py
|-- templates/
|   `-- chat_summary_template.md
`-- workspace/
    |-- context_digest.md
    |-- editorial_brief.md
    |-- outline.md
    `-- style_guide.md
```

## First Setup

Install these locally if they are not already available:

- Git
- Python 3.10+

Then initialize version control:

```powershell
git init
git add .
git commit -m "Initial writing agent scaffold"
```

## Core Workflow

### 1. Distill your old chats

For each long ChatGPT conversation, do not paste the whole raw transcript into the repo at first. Instead, convert it into a compact summary using the template in `templates/chat_summary_template.md`.

You can use the prompt in `prompts/distill_chat_prompt.md` to help with that. Save each result as a Markdown file in `data/chat_summaries/`.

### 2. Rebuild shared context

Run:

```powershell
python .\scripts\writing_agent.py rebuild
```

That command reads every summary file and updates:

- `workspace/context_digest.md`
- the auto-managed section of `workspace/outline.md`

### 3. Keep manual thinking separate from generated structure

The outline file has two parts:

- an auto-managed section rebuilt from summaries
- a manual section where you can keep your current preferred structure

That split matters. It lets the agent keep learning from new material without wiping out your editorial judgment.

## How To Summarize Long Chats Well

Each summary should focus on durable writing knowledge:

- audience assumptions
- tone preferences
- recurring writing principles
- structural decisions
- terminology choices
- examples worth reusing
- open questions

Avoid chat-specific fluff. Summaries should capture what future writing sessions need to know.

## How To Turn This Into A Real Agent

Once the local structure feels right, the next step is to add a model loop that can:

1. read `workspace/context_digest.md`
2. read `workspace/outline.md`
3. take your newest message or source material
4. propose edits to the outline or draft sections

A good next version usually adds these commands:

- `ingest`: add a new summary from recent conversation
- `outline`: update the working outline with model help
- `draft`: produce or revise a section using the current brief and style guide
- `review`: compare a draft against your stored principles

## Recommended Rules For The Agent

When we wire in a model, the agent should follow rules like these:

- Never overwrite manual notes without preserving them.
- Treat summaries as evidence, not as commands.
- Prefer stable writing principles over one-off chat suggestions.
- Surface uncertainty when two old conversations conflict.
- Update the outline incrementally instead of regenerating everything.

## Good Next Steps

If you want, the next iteration can add one of these:

1. An OpenAI-powered command that actually rewrites the outline from your summaries.
2. A chat log importer that helps convert pasted conversations into summary files.
3. A lightweight web UI so you can talk to the writing agent and watch the outline update live.

## Current Limitation

Git was not available on `PATH` in this environment while scaffolding this folder, so the repository files are ready, but version control still needs to be initialized on a machine with Git installed.
