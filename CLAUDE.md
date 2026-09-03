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

Topic branch to `dev` by PR. `main` is Richard's. Done: merged to `dev` with `npm run lint`,
`npm run test` and `npm run build` green, seen on the `dev` preview.

## Hard rules

- Fee logic must match the Qurate fee schedule. Its intended home is
  `qurate-qvos-skills/firm/fee-schedule.md`, still a placeholder; until it is populated the
  calculator is the working copy. If the two differ, raise it before changing either.
- Qurate brand values come from the Qurate skills; do not hand-roll hex or type.
- Australian English, AUD, en-AU formatting. No em dashes.
- No new dependencies without approval; `.lovable/plan.md` lists the ones already unused.
