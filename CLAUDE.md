# CLAUDE.md, Qurate fee calculator (qurate-fee)

Firm-wide rules (decision protocol, reporting, layering) live in
`qurate-qvos-skills/CLAUDE.md`. This file is repo facts.

## What it is

A client-side advisory fee calculator served at fee.qurate.com.au. No database of its own.
Access at the root is gated by a 30 day token, validated against the QVOS backend edge
function `validate-calculator-token` on project `wzzucfuixqbjowztqzbr`, or by the `?dev=true`
bypass. Lovable project, Vercel hosting. Lovable's own notes are in `.lovable/`.

## Stack

React 18, TypeScript, Vite, Tailwind, shadcn/ui, Vitest. Scripts: `dev`, `build`, `lint`, `test`.

## Branches and done

Topic branch to `dev` by PR. `main` is Richard's. Done: merged to `dev` with `npm run gate`
green and seen on the `dev` preview.

## The gate

`npm run gate` runs typecheck, lint, tests and build, in that order, and is exactly what CI
runs. Run it before every push. Add a check to the `gate` script, never to the workflow
alone. Install with `npm ci`, not `npm install`: `dev` was unbuildable for weeks because
package.json and the lockfile disagreed about jspdf and a clean install pruned it.

## Claude configuration

`.claude/settings.json` pre-approves the repo's own read-only and gate commands and keeps
push, install and deploy behind a prompt. `.claude/hooks/house-rules.py` refuses a write
carrying a banned brand hex or Calibri and reports em dashes without refusing.
`.claude/hooks/house-rules.json` lists the files still carrying the superseded palette; it
is a debt register and should only ever get shorter.

## Intent

`docs/intent/` says what each subsystem is meant to do. Read it before changing the
subsystem, and update it in the same change when the intent itself moves.

## Hard rules

- Fee logic must match the Qurate fee schedule. Its intended home is
  `qurate-qvos-skills/firm/fee-schedule.md`, still a placeholder; until it is populated the
  calculator is the working copy. If the two differ, raise it before changing either.
- Qurate brand values come from the Qurate skills; do not hand-roll hex or type. The app
  still ships the superseded `2E3D49` and `C19131`; correcting it is a visible change to a
  client-facing product and needs Richard's yes.
- A deployed build always requires a valid calculator token. See
  `docs/intent/access-gate.md`.
- Australian English, AUD, en-AU formatting. No em dashes.
- No new dependencies without approval; `.lovable/plan.md` lists the ones already unused.
