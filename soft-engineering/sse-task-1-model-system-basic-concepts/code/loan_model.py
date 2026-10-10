#!/usr/bin/env python3
"""
SSE Task 1 — runnable model of the process object (a Loan).

Demonstrates the five basic concepts:
  - boundary/purpose  -> the LoanSystem class owns the loan cycle
  - components        -> Catalogue (C4), LoanService (C3)
  - process object    -> Loan with states REQUESTED/ACTIVE/RETURNED/CLOSED
  - operations        -> initiate_borrow / approve / return_book / renew / close_loan
  - solution config   -> an in-memory catalogue shared by kiosk + desk
  - stakeholder value -> borrow time, availability accuracy

Run:  python3 code/loan_model.py
"""

from __future__ import annotations

import datetime as dt
from dataclasses import dataclass, field
from enum import Enum


class State(str, Enum):
    REQUESTED = "REQUESTED"
    ACTIVE = "ACTIVE"
    RETURNED = "RETURNED"
    CLOSED = "CLOSED"


LOAN_DAYS = 30
DAILY_FINE = 0.20  # currency units per late day


@dataclass
class Copy:
    copy_id: str
    title: str
    available: bool = True


@dataclass
class Loan:
    """The process object: lives through the borrow cycle."""
    loan_id: str
    reader_id: str
    copy: Copy
    state: State = State.REQUESTED
    due: dt.date | None = None
    fine: float = 0.0
    history: list[str] = field(default_factory=list)

    def _log(self, msg: str) -> None:
        self.history.append(f"{self.state.value}: {msg}")


class LoanService:
    """C3 — business rules."""

    def __init__(self, catalogue: dict[str, Copy], eligible_readers: set[str]):
        self.catalogue = catalogue
        self.eligible = eligible_readers
        self._seq = 0

    # operation 1
    def initiate_borrow(self, reader_id: str, copy_id: str) -> Loan:
        copy = self.catalogue[copy_id]
        self._seq += 1
        loan = Loan(loan_id=f"L{self._seq:04d}", reader_id=reader_id, copy=copy)
        loan._log(f"borrow requested for '{copy.title}'")
        return loan

    # operation 2
    def approve(self, loan: Loan, today: dt.date | None = None) -> Loan:
        if loan.state is not State.REQUESTED:
            raise ValueError("only REQUESTED loans can be approved")
        today = today or dt.date.today()
        if not loan.copy.available:
            raise ValueError(f"copy {loan.copy.copy_id} is not available")
        if loan.reader_id not in self.eligible:
            raise ValueError(f"reader {loan.reader_id} is not eligible")
        loan.copy.available = False          # copy = ON_LOAN
        loan.due = today + dt.timedelta(days=LOAN_DAYS)
        loan.state = State.ACTIVE
        loan._log(f"approved; due {loan.due.isoformat()}")
        return loan

    # operation 3
    def return_book(self, loan: Loan, today: dt.date | None = None) -> Loan:
        if loan.state is not State.ACTIVE:
            raise ValueError("only ACTIVE loans can be returned")
        today = today or dt.date.today()
        if loan.due and today > loan.due:
            loan.fine = round((today - loan.due).days * DAILY_FINE, 2)
        loan.copy.available = True           # copy = AVAILABLE
        loan.state = State.RETURNED
        loan._log(f"returned; fine={loan.fine:.2f}")
        return loan

    # operation 4a
    def renew(self, loan: Loan, days: int = LOAN_DAYS) -> Loan:
        if loan.state is not State.ACTIVE:
            raise ValueError("only ACTIVE loans can be renewed")
        loan.due = (loan.due or dt.date.today()) + dt.timedelta(days=days)
        loan._log(f"renewed; new due {loan.due.isoformat()}")
        return loan

    # operation 4b
    def close_loan(self, loan: Loan) -> Loan:
        if loan.state is not State.RETURNED:
            raise ValueError("only RETURNED loans can be closed")
        loan.state = State.CLOSED
        loan._log("closed and archived")
        return loan


def _demo() -> None:
    cat = {
        "B-042": Copy("B-042", "Thinking in Systems"),
        "B-017": Copy("B-017", "Designing Data-Intensive Applications"),
    }
    svc = LoanService(catalogue=cat, eligible_readers={"R-777"})
    today = dt.date(2026, 10, 10)

    print("=== borrow cycle ===")
    loan = svc.initiate_borrow("R-777", "B-042")
    svc.approve(loan, today)
    print(f"loan {loan.loan_id} state={loan.state.value} due={loan.due}")

    print("\n=== renewal ===")
    svc.renew(loan)
    print(f"loan {loan.loan_id} new due={loan.due}")

    print("\n=== late return (35 days after start) ===")
    late = today + dt.timedelta(days=35)
    svc.return_book(loan, late)
    print(f"loan {loan.loan_id} state={loan.state.value} fine={loan.fine:.2f}")

    print("\n=== close ===")
    svc.close_loan(loan)

    print("\n=== history ===")
    for line in loan.history:
        print(" ", line)

    print(f"\ncopy available again: {cat['B-042'].available}")


if __name__ == "__main__":
    _demo()
