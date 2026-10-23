# SSE Task 8 — Product Variable Decomposition

**Subject:** Soft Engineering · **Course:** 2026 HR S5 Soft Engineering

## Task

Select 3 microstages from different stages.
Make different decompositions for these microstages.

---

## 1. The three microstages

I take three microstages from the stages already analysed for the **self-service book-loan
kiosk** (Tasks 1–7), each from a different stage of the SDLC:

| # | Microstage | Stage |
|---|---|---|
| **A** | Build the system model (boundary, components, Loan as process object) | analysis (Task 1) |
| **B** | Design the borrow screen flow | design (Task 7, D3) |
| **C** | Handle a damaged copy on return | design (Task 7, D2 rules) — as it runs in operation, i.e. the runtime behaviour the operation stage has to support |

The point of the task is that the *same kind* of microstage can be pulled apart in different
ways, so I deliberately use a **different decomposition principle for each one**.

## 2. Decomposition of A — system model

**Principle: by components (structural).** What the model is made of.

| Level | Part | Content |
|---|---|---|
| A1 | Boundary & purpose | what is inside the system, and the one statement of why it exists |
| A2 | Component list | card/RFID reader, kiosk app, loan service, catalogue/loan DB |
| A3 | Process object | the Loan: states and operations |
| A4 | Solution configuration | one deployable kiosk instance |

*Alternative cut:* by stakeholder value (reader value / library value) — useful, but it
answers "why", not "what it is made of", so for a model I keep the structural one.

## 3. Decomposition of B — borrow screen flow

**Principle: by user decision points (behavioural).** Where the flow branches on something the
user sees.

| Step | Screen | Branch |
|---|---|---|
| B1 | Welcome | card tapped? → continue / timeout |
| B2 | Scan the book | tag read? → continue / "try again" |
| B3 | Member check result | active + under limit → continue / **stop with reason** |
| B4 | Copy check result | available → continue / **stop with reason** |
| B5 | Confirmation | loan created → show due date, offer receipt |

Here the structural cut does not work: the flow is not made of parts, it is made of
decisions. Two of the four branches end the flow, which is the whole reason the flow has to be
designed as a chain of checks rather than one form.

## 4. Decomposition of C — damaged return

**Principle: by state transition (temporal).** What happens to the objects over time.

| Step | Trigger | Transition |
|---|---|---|
| C1 | Return starts | Loan: `ACTIVE` → `RETURNING`; Copy: `ON LOAN` → `IN TRANSIT` |
| C2 | Damage is reported at the kiosk | Copy: `IN TRANSIT` → `FLAGGED`; no shelf state yet |
| C3 | Librarian inspects | `FLAGGED` → `DAMAGED` (repair) or back to `AVAILABLE` (false alarm) |
| C4 | Loan settlement | Loan: `RETURNING` → `CLOSED` with a note of the damage |

This microstage does not decompose into components either — the interesting fact is that the
copy leaves the normal return path *between* two states, and that only a person (C3) can
decide how it leaves.

## 5. Why three different decompositions

| Microstage | Principle | Because the microstage is about… |
|---|---|---|
| A — system model | structural | what the thing is made of |
| B — screen flow | behavioural | what the user decides |
| C — damaged return | temporal | how objects change state |

The same product, the same language, three different cuts — and choosing the cut is itself a
design decision. A structural decomposition of B would list screens and miss that the flow's
value is in the stop-points; a behavioural decomposition of C would describe what the
librarian does and miss that the copy is stuck between states until someone decides.

---

## Conclusion

Variable decomposition means: pick the axis that matches the microstage, not the axis you are
used to. Structure for the model, decisions for the interaction, states for the exception
path — each gives a table an engineer can review, and each would hide the key fact if it had
been used for the other two microstages.
