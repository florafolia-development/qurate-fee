# Intent: access gate

What this subsystem is meant to do, so a later reader can tell drift from
design. Written against the code, not from memory.

## Purpose

The calculator exposes Qurate's fee schedule. It is shown to a named
prospect, not to the public, and access is by a token the firm issues.

## Rules

1. A deployed build always requires a valid token. There is no exception,
   including on the `dev` preview: tokens for preview testing come from the
   QVOS `create-calculator-token` function like any other.
2. The `?dev=true` bypass works in a development build only. The rule is
   `devBypassAllowed` in `src/lib/tokenUtils.ts`, pure and tested in
   `src/test/tokenAccess.test.ts` so it can be checked rather than trusted.
3. Validation happens in the QVOS backend, not here. This repo holds no
   signing secret and must never hold one. The endpoint is
   `validate-calculator-token` on Supabase project `wzzucfuixqbjowztqzbr`,
   named in `src/hooks/useTokenValidation.ts`.
4. A failed or absent token renders `AccessDenied`, and nothing behind the
   gate is fetched or rendered first.

## Known history

`?dev=true` alone skipped validation in every build until 19 September 2026.
Anyone who guessed the parameter reached the calculator and the fee schedule
without a token. Closed in this change.

A `TOKEN_SECRET` constant sat in `src/lib/tokenUtils.ts` between 27 January
2026 and its removal. It is still reachable in git history, so the value
should be treated as burned wherever it was used. Nothing in the current
code references it.
