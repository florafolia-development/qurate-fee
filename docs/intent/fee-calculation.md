# Intent: fee calculation

## Purpose

Reproduce the fee structure in the Qurate engagement letter, exactly, so a
prospect sees the same numbers the letter commits to.

## Rules

1. The engagement letter is the authority. The intended home for the schedule
   is `qurate-qvos-skills/firm/fee-schedule.md`, still a placeholder, so until
   that is populated `src/lib/feeCalculations.ts` is the working copy. If the
   two ever differ, raise it before changing either.
2. The success fee is cumulative and banded, in the way income tax brackets
   are: each band is charged at its own rate rather than one rate applying to
   the whole value.
3. The transaction structuring fee is a flat amount per band, with exclusive
   lower bounds taken from the terms and conditions, so an enterprise value of
   exactly $10,000,000 sits in the $10M to $15M band.
4. The retainer rebate is capped and conditional. It applies only above the
   rebate threshold and never exceeds the cap.
5. Every rate, threshold and cap is a named constant at the top of
   `src/lib/feeCalculations.ts`. No literal rate appears in a component.
6. AUD, en-AU formatting, Australian English.

## Not in scope

No persistence, no client data, no database. The calculator holds nothing
after the tab closes beyond the PDF the user chooses to export.
