# AGENTS.md

Instructions for future Codex runs and repository automation.

## Hard Rules

- Do not rewrite finished PDFs.
- Do not delete source PDFs.
- Do not generate new manuals unless explicitly asked.
- Do not make trading recommendations.
- Preserve the educational-only purpose of the repository.

## Storage Rules

- Store final PDFs in `manuals/pdf/<category>/`.
- Store companion Markdown notes in `manuals/markdown/<category>/`.
- PDFs are finished artifacts.
- Markdown files are companion lookup notes.

## Manual Tracking

- Assign LOTQ IDs sequentially.
- Every manual should eventually receive a LOTQ ID.
- Every PDF should eventually have a matching Markdown note.
- Preserve naming consistency across PDFs, Markdown notes, and index entries.

## Index Maintenance

Update indexes whenever manuals are added:

- `indexes/master_index.md`
- `indexes/topic_index.md`
- `indexes/difficulty_index.md`
- `indexes/formula_index.md`
- `indexes/implementation_traps_index.md`
- `indexes/system_design_index.md`

If metadata cannot be verified, mark it as `Needs review`.
