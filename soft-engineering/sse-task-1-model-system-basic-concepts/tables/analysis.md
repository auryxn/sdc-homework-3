# SSE Task 1 — Five Basic Concepts (reference tables)

System: **city public-library self-service book-loan kiosk**

## 1. Boundary & purpose

| Inside the boundary | Outside the boundary |
|---|---|
| RFID/card reader, kiosk app, loan service, catalogue DB, tagged book copy | reader (actor), printed content, acquisition/budget system, payment rails |

**Purpose:** let a registered reader borrow or return a book in under a minute while keeping
loan records and copy availability accurate — without a librarian.

## 2. Components (5)

| ID | Component | Responsibility |
|---|---|---|
| C1 | Card & RFID reader | identify reader + book, produce digital IDs |
| C2 | Kiosk application (UI) | guide user, show prompts/errors/receipt |
| C3 | Loan-management service | business rules: availability, eligibility, due date, overdue |
| C4 | Catalogue & loan-records DB | authoritative state of copies and loans |
| C5 | Book copy (tagged) | the managed physical object |

## 3. Process object — Loan

| State | Type | Entered by |
|---|---|---|
| `REQUESTED` | initial | `initiate_borrow()` |
| `ACTIVE` | — | `approve()` |
| `RETURNED` | — | `return_book()` |
| `CLOSED` | final | `close_loan()` |

| Operation | Transition | Side effect |
|---|---|---|
| `initiate_borrow(reader, copy)` | → REQUESTED | read identities |
| `approve()` | REQUESTED → ACTIVE | set due date, copy = ON_LOAN |
| `return_book(copy)` | ACTIVE → RETURNED | copy = AVAILABLE, compute fine |
| `renew()` / `close_loan()` | ACTIVE → ACTIVE / RETURNED → CLOSED | extend due / archive |

## 4. Solution configuration — "Metro-branch express kiosk"

| Aspect | Setting |
|---|---|
| Deployment | one floor-standing kiosk at branch entrance |
| Reader | touch + card tap, no librarian |
| Service host | on-prem loan service on branch LAN |
| Data | catalogue DB shared with librarian desk |
| Network | LAN; limited offline cache of active loans |
| Concurrency | copy locked while a loan is REQUESTED |

## 5. Stakeholder value

| Stakeholder | Value |
|---|---|
| Reader | borrow/return under 1 min, no queue, instant due date |
| Library | staff time freed, accurate real-time records, lower cost/loan |
