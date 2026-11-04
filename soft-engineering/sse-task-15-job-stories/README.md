# SSE Task 15 — Job Stories

**Subject:** Soft Engineering · **Course:** 2026 HR S5 Soft Engineering

## Task

Write job stories for the chosen system. Each story follows the form *"When [situation], I want
to [motivation], so I can [expected outcome]"* — no role in the template, the situation does
the work.

---

## The system

The **self-service book-loan kiosk** from Tasks 1–14 (city public library). The happy path is
already well described in the earlier tasks, so most of these stories are about the moments
around it: the queue, the book that will not scan, the damaged return, the Monday report.

## Why job stories here

A user story would say "as a reader I want to borrow a book". That is true but it hides the
reason the kiosk matters: *when* the reader arrives. A job story puts the trigger first, so
the same person can appear in several stories with different needs — the reader in a hurry is
not the reader with a stroller, and neither is the reader whose book will not scan.

## The stories

**J1 — The evening queue**
> When I come to the branch after work with three books and a queue at the desk, I want to
> borrow them at the kiosk in under a minute, so I can catch my bus and still have the books
> for the weekend.

*Implies:* the borrow flow stays short, the screen starts from the welcome state, and the due
date is visible without scrolling.

**J2 — The late return**
> When I finish a book at eleven at night, I want to return it at the outside drop point and
> get confirmation that it is checked in, so I know the loan is closed and I will not be fined
> for a book I already brought back.

*Implies:* the return path must confirm the specific copy, not just "item received", and the
confirmation has to reach the reader outside the branch (slip or message).

**J3 — The book that will not scan**
> When a book will not scan at the kiosk and the screen only says "unknown item", I want to be
> told what to do next — try the barcode, take it to the desk, or leave it — so I do not block
> the queue and do not walk out with an unrecorded book.

*Implies:* every error state needs a next action and a named fallback, not an error code.

**J4 — One free hand**
> When I come with a stroller and can only use one hand, I want large buttons at a reachable
> height and a session that does not time out while I park the stroller, so I can finish the
> loan without asking a stranger to hold the book.

*Implies:* accessibility is a first-class path: reachable controls, adjustable text, a longer
idle timeout before the session resets.

**J5 — The damaged return**
> When a reader hands me a wet book, I want to record the damage and the fine in the same loan
> record the kiosk created, so the reader's account is correct and I am not keeping a paper
> note that gets lost by Friday.

*Implies:* the librarian's desk view and the kiosk write to one loan record; damage and fines
are attributes of the loan, not a separate ledger.

**J6 — Closing the desk**
> When the branch closes, I want a short list of what the kiosk did today that needs a human —
> exceptions, unpaid fines, failed scans — so I can close the desk in ten minutes instead of
> checking every loan one by one.

*Implies:* exceptions must be logged as a queue with a reason, not just as failed transactions.

**J7 — The monthly report**
> When the report to the municipality is due, I want loan counts, peak-hour load and the
> exception rate exported in one file, so I can report without rebuilding the numbers in Excel
> the night before.

*Implies:* the kiosk records timestamps and exception reasons, and the export is part of the
system, not a manual chore.

**J8 — The kiosk that is down**
> When a kiosk is offline twenty minutes before opening, I want to see its status, its last
> error and whether the terminal or the loan service is down, so I can fix it remotely or send
> the right person before the first readers arrive.

*Implies:* health status and the last error are visible remotely, and the message distinguishes
"no network" from "service down" from "hardware fault".

## What the set shows

Four of the eight stories (J3, J5, J6, J8) happen when something goes wrong. That is not an
accident: the normal loan is a solved problem, and the kiosk earns or loses trust in the
recovery paths — where the reader is stuck, the librarian is cleaning up, and IT is guessing.
It also shows that "reader" and "librarian" are not separate worlds: J5 starts with a reader's
mistake and ends with a librarian's record, which is exactly the hand-over Task 11 called the
slow path. Job stories make that hand-over visible, because each one names the situation in
which the two roles meet.

---

## Conclusion

Eight job stories cover the kiosk from both sides of the desk: a fast borrow, a late return,
four recovery situations and two reporting needs. Written as situations rather than roles,
they point directly at the design consequences — clear next steps in errors, one shared loan
record, a visible exception queue and remote health status.
