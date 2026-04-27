# Iterative Outline Writing Workflow

## Outline Phase

- The outliner does not produce a full polished outline in one shot.
- It extends the outline in bounded increments.
- An increment may add breadth, depth, or a mix of both.
- After each increment, the outliner adds a compressed machine-to-machine rationale:
  - what this increment is trying to establish
  - what it assumes
  - what it must not overclaim
- The outline evaluator reviews that increment and returns:
  - `accept`
  - `revise`
- The outliner revises and continues until the outline is complete enough to draft from.

## Writing Phase

- Only after the outline phase is accepted as complete enough does the writer begin.
- The writer drafts in bounded chunks, not one long burst.
- Each chunk is scoped to trusted writing length.
- If the writer realizes something that seems better than the outline, that divergence must be made explicit.

## Conceptual Review Phase

- The conceptual evaluator compares the prose chunk to the accepted outline chunk.
- It returns:
  - `accept`
  - `rewrite_to_match_outline`
  - `accept_delta`
- If it returns `accept_delta`, the accepted divergence is patched back into the outline so the outline remains canonical.

## Final Cleanup

- After conceptual acceptance, the editor tightens for logical economy.
- After the editor, the punctuation/grammar agent fixes only mechanical errors.

## Core Principle

- The system should never ask prose to solve more logic than the outline has already earned.
