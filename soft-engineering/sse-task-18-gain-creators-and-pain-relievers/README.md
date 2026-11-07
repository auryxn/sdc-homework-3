# SSE Task 18 — Gain Creators and Pain Relievers

**Subject:** Soft Engineering · **Course:** 2026 HR S5 Soft Engineering

## Task

Take the pains and gains from Task 17 and describe what the product does to relieve each pain
and create each gain. Then check where the fit is real and where it is only claimed.

---

## The system

Same **self-service book-loan kiosk** (city public library), same reader jobs U1–U3 from
Task 16 and the same list P1–P9 / G1–G8 from Task 17. This task is the product side of the
value proposition canvas: pain relievers and gain creators, one per item.

## 1. Pain relievers

| Pain | Pain reliever | How it works |
|---|---|---|
| P1 queue at the desk | self-service loan at the terminal | card + book scan, no staff step, M1–M6 in Task 6 |
| P2 catalogue says available, shelf empty | *none yet* — only a "last seen" flag on the copy | the kiosk sees the loan DB, not the shelf; showing "in sorting / last seen 2 days ago" would at least warn the reader |
| P3 forgotten due date | visible due date + reminder before it becomes a fine | due date on screen and slip (M6), reminder 3 days before via the account |
| P4 no proof of return | return receipt tied to the copy | confirmation names the copy and the timestamp, not just "item received" |
| P5 error with no next step | error states that carry an action | every failure screen names retry / desk / leave it, per Task 15 J3 |
| P6 fumbling while others wait | one-hand flow and a session that waits | large targets, step prompts, longer idle timeout before reset (J4) |
| P7 previous reader's list on screen | session reset | screen clears on end of session, nothing personal stays |
| P8 damage recorded on paper | damage and fine on the loan record | librarian desk view writes to the same record the kiosk created (J5) |
| P9 outage found by readers | remote health status and alert | heartbeat plus last error class, so IT sees the fault before opening (J8) |

The relievers are uneven: P1, P5, P6, P7 are the kiosk's own behaviour; P2, P8 and P9 need
another component (catalogue, desk view, monitoring) to exist before the kiosk can help.

## 2. Gain creators

| Gain | Gain creator | How it works |
|---|---|---|
| G1 book in hand the same day | loan without appointment | terminal at the entrance, borrow in under a minute |
| G2 due date I can see | due date + reminder | slip, screen, and a reminder before the due date |
| G3 proof the loan is closed | synchronous return confirmation | the copy is matched to the open loan before the screen says "returned" |
| G4 no conversation about what I read | self-service, privacy by default | no staff interaction; the screen shows nothing after the session |
| G5 machine tells me what to do next | actionable error copy | same rule as P5, seen from the gain side |
| G6 staff free for real cases | routine loans moved to the terminal | desk handles only exceptions and damage |
| G7 report without Excel | timestamped events and one export | loan and exception events are recorded as data, not as counts typed later |
| G8 fixed before readers arrive | monitoring and remote diagnostics | status page, last error, restart or dispatch decision |

## 3. Where the fit is real

| Item | Fit | What is missing |
|---|---|---|
| P1, P5, P6, P7 / G1, G4, G5 | **strong** | nothing structural — this is the kiosk's own flow |
| P3, P4 / G2, G3 | **partial** | the signal stops at the branch: reminders and receipts need the account/notification service |
| P8 / G6, G7 | **partial** | requires the desk view and the export to read the same loan record |
| P2 | **absent** | shelf accuracy is a catalogue and shelving problem, not a kiosk screen |
| P9 / G8 | **absent today** | needs a monitoring component that does not exist in the current system |

So four pains are relieved by the product as designed, three are relieved only if a second
component is added, and two are outside it. The same split appeared in Task 17, which is a
good sign: the canvas is not inventing fit that the system does not have.

## 4. The one reliever I would build next

**P3/P4 — carry the confirmation past the door.** The kiosk already knows the copy, the
timestamp and the due date at the moment of the transaction; the missing piece is delivery
(reminder before the due date, receipt after the return). It is the cheapest fix with the
largest effect on trust, and it turns G2 and G3 from "partial" into "strong" without new
hardware.

---

## Conclusion

The kiosk's strong fit is speed and privacy; its weak fit is everything that happens after
the screen goes back to the welcome state. The pain relievers that matter next are the ones
that deliver a signal the reader can keep — a reminder and a receipt — rather than another
screen at the terminal.
