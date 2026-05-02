# Outline Write Edit Workflow

Use this protocol only when the orchestrator explicitly chooses the full artifact workflow.

## Purpose

This workflow is for substantial manuscript passages where the logic is subtle enough that prose should not be generated in one burst.

## Sequence

1. Extract or build an outline.
2. Evaluate the outline until it is complete enough to draft from.
3. Ask the Writer Agent to draft bounded chunks from the accepted outline.
4. Ask the Conceptual Evaluator to check each chunk for fidelity, unearned claims, and useful divergences.
5. Ask the Editor Agent to tighten accepted prose.
6. Ask the Proofreader Agent only for final mechanical cleanup.

## Artifact Policy

- Save artifacts only when the orchestrator requests saved artifacts or when the user asks for a new note/draft.
- Typical artifacts are an outline note, claim map, draft note, and edited note.
- Live inline manuscript work should not automatically create artifacts.

## Writer Constraint

The Writer Agent remains role-pure. It writes prose. It does not decide whether to open files, save artifacts, call evaluators, or run the full workflow.
