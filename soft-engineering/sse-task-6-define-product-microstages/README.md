# SSE Task 6 — Define Product Microstages

**Subject:** Soft Engineering · **Course:** 2026 HR S5 Soft Engineering

## Task

Select the product (multifunctional).
Define use cases (2–3 use cases in the format of JTBD).
For each use case define the user's role.
For each use case define microstages.
For each microstage define useful function.

---

## The product

I keep the **self-service book-loan kiosk** from Tasks 1–4 and 10 (city public library). It
is multifunctional: one product lets a reader borrow a book, return a book, and see what they
currently hold — three different jobs, not one.

## Use cases (JTBD)

| # | Job story | When it happens |
|---|---|---|
| **UC1** | **When** I want to read a book I have already found on the shelf, **I want to** take it home by myself, **so I can** start reading today instead of queueing at the desk. | borrow |
| **UC2** | **When** I have finished a book and the due date is near, **I want to** give it back without talking to anyone, **so I can** avoid an overdue fine and free my borrowing limit. | return |
| **UC3** | **When** I am not sure what I already have at home or when it is due, **I want to** check my current loans, **so I can** plan my reading and avoid surprise reminders. | check |

## 1. UC1 — Borrow a book

**User role:** the *borrower* — a registered reader holding a valid membership card, acting
on their own behalf.

| # | Microstage | Useful function |
|---|---|---|
| M1 | Identify the reader | read the card and resolve the person to a membership record |
| M2 | Identify the copy | read the RFID tag and bind it to one catalogue copy |
| M3 | Check eligibility | verify membership is active and the borrower is under the loan limit |
| M4 | Check availability | confirm the copy is on the shelf and not already on loan or reserved |
| M5 | Register the loan | create the loan record, set holder and due date (+21 days) |
| M6 | Confirm to the reader | print the due-date slip and show the new loan on screen |

Default path: reader taps card → scans the book → service approves → slip printed. If
checking fails at M3 or M4 the product stops before M5 and says why.

## 2. UC2 — Return a book

**User role:** the *borrower* returning the same copy (no librarian involved — that is the
whole point of the product).

| # | Microstage | Useful function |
|---|---|---|
| M1 | Identify the reader | read the card and load the reader's open loans |
| M2 | Identify the copy | read the RFID tag of the returned book |
| M3 | Match loan | find the open loan that belongs to this reader and this copy |
| M4 | Check and record condition | check the copy is not flagged damaged and record any damage before it re-enters the shelf |
| M5 | Close the loan | set the copy back to available, close the loan, compute any late fee |
| M6 | Confirm to the reader | show the closed loan and the remaining fine or limit |

## 3. UC3 — Check my loans

**User role:** the *borrower* in read-only mode — the product only displays, it changes
nothing in the loan state.

| # | Microstage | Useful function |
|---|---|---|
| M1 | Identify the reader | read the card and load the reader's record |
| M2 | Load the loan set | fetch all open loans of this reader from the loan service |
| M3 | Compute the summary | derive due dates, days left and total fines from the loan data |
| M4 | Present the result | show one list: title, due date, status, fine |
| M5 | Offer the next step | prompt to renew or to return a copy that is due |

---

## Microstages in brief

The product is a chain of **identify → validate → act → confirm**: every use case starts
with identifying the reader, then checks the state (eligibility, matching loan, or just
loading it), then does the one state change the job needs (M5 creates a loan, M5 closes a
loan, UC3 has no change at all), and ends by telling the reader what happened. The confirm
stage is not decoration — it is what makes a self-service product trustworthy without a
librarian standing next to it.

---

## Conclusion

The kiosk is a multifunctional product with three jobs — borrow, return, check — each with
its own user role (borrower acting in write or read mode) and its own set of microstages.
The microstages line up across use cases, and each has a single useful function, so a failure
can be traced to one stage (e.g. an identification failure in M1 blocks the whole job, while
a failure of M6 still leaves the loan correct in the database).
