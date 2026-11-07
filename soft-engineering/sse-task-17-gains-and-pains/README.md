# SSE Task 17 — Gains and Pains

**Subject:** Soft Engineering · **Course:** 2026 HR S5 Soft Engineering

## Task

For the jobs identified in Task 16, list the pains the user has while doing them and the gains
they are looking for, then show which of them the system actually addresses.

---

## The system and the jobs

Same **self-service book-loan kiosk** (city public library), and the same main executor: the
reader. The jobs are the ones from Task 16 — borrow a book (U1), know what is held and when
it is due (U2), close a loan and be sure of it (U3). U7 and U8 belong to the librarian and IT
and appear at the end, because the kiosk's pains are not only the reader's.

## 1. Pains

| # | Pain | Related job | Type |
|---|---|---|---|
| P1 | The desk queue at peak hours; the loan takes longer than finding the book | U1 | functional |
| P2 | The catalogue says "available", the shelf says otherwise | U1 | functional |
| P3 | The due date is forgotten, and the first reminder is already a fine | U2 | functional |
| P4 | After the drop point, no proof that the return was registered | U3 | emotional |
| P5 | An error screen ("unknown item") with no next step | U4 | emotional |
| P6 | Fumbling with the card and the scanner while people wait behind | U5 | social |
| P7 | The previous reader's loan list still on screen | U6 | social |
| P8 | Damaged copies recorded on paper, so the record and the shelf disagree | U7 | functional |
| P9 | An outage is discovered by readers, not by IT | U8 | functional |

The most expensive ones are not the slow ones. P1 costs minutes; P3, P4 and P8 cost trust —
a reader who was fined for a book they returned stops using the kiosk and tells others.

## 2. Gains

| # | Gain | Related job | Type |
|---|---|---|---|
| G1 | The book is in hand the same day, without planning around staff hours | U1 | functional |
| G2 | A due date I can see, and a reminder before it becomes a fine | U2 | functional |
| G3 | Proof that the loan is closed, at the moment I return it | U3 | emotional |
| G4 | No conversation about what I read | U6 | social |
| G5 | A machine that says what to do next instead of what went wrong | U4 | emotional |
| G6 | Staff freed from routine loans, available for the cases that need a human | U7 | functional |
| G7 | Loan numbers and peak hours available without rebuilding them in Excel | U7 | functional |
| G8 | A terminal that is fixed before the first reader arrives | U8 | functional |

G1 and G4 are why the kiosk exists at all: speed and privacy. G2, G3 and G5 are the gains
that keep it in use after the first visit.

## 3. What the kiosk actually addresses

| Pain / gain | Addressed today? | Where it is handled |
|---|---|---|
| P1, G1 | yes | borrow flow, M1–M6 (Task 6) |
| P2 | no | catalogue and shelf are outside the kiosk — this is step 2 of the job map |
| P3, G2 | partly | due date on screen and slip; reminders are a separate service |
| P4, G3 | partly | return confirmation exists, but the outside drop point confirms only "item received" (Task 15, J2) |
| P5, G5 | no | error states currently show a code, not a next action |
| P6 | partly | the session times out, but the timeout is short for someone with a stroller (J4) |
| P7 | yes | session reset clears the screen |
| P8 | no | damage is still a paper note at the desk (J5) |
| P9 | partly | status exists, but the last error is not visible remotely (J8) |

Four of the nine pains are outside the kiosk's control (P2, P3, P8, P9). That is the same
finding as Task 16: the kiosk is one step in a longer job, and the biggest pains sit at the
seams between the kiosk, the catalogue, the account and the desk.

## 4. What I would fix first

By cost of trust, not by effort: **P3/P4** (unexpected fines and unproven returns), then
**P5** (errors without a next step), then **P2** (shelf accuracy). The first two are
confirmation problems, and the kiosk already owns most of the confirmation path — it only
has to carry the signal past the branch door instead of stopping at the screen.

---

## Conclusion

The kiosk removes the queue and the conversation, which are its two real gains, but it leaves
the pains that live between systems: an inaccurate shelf, a reminder that arrives late, a
return that is not proven. Those are the ones worth fixing next, because they cost trust
rather than seconds.
