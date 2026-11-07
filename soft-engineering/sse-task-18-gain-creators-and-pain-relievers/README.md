# SSE Task 18 — Gain Creators and Pain Relievers

**Subject:** Soft Engineering · **Course:** 2026 HR S5 Soft Engineering

## Task

Return to the list of user jobs. Ask ChatGPT to identify the features of the application that
play the role of gain creators and the features that play the role of pain relievers.

## The application and the user jobs

The prompt uses a **financial assistant application** as the example. I analyse that product:
a personal-finance assistant that aggregates bank accounts, categorises spending, reminds
about bills, and suggests a monthly budget. The user jobs I return to are:

- **J1** See where the money went this month.
- **J2** Know how much is safe to spend before the next income.
- **J3** Pay a bill on time and not miss a due date.
- **J4** Avoid an overdraft or a late fee.
- **J5** Build a small reserve without thinking about it every day.
- **J6** Feel in control of subscriptions and recurring charges.
- **J7** Keep financial data private and secure.

Note: Tasks 16–17 used the library kiosk as the chosen system; this task follows the prompt's
explicit financial-assistant example, so the user jobs above are the financial assistant's
jobs.

## Prompt used

> Let's look at the financial assistant application.
> 1. Define the features of the application that play the role of gain creators.
> 2. Define the features of the application that are pain relievers.

## ChatGPT result (for the assignment chat)

| Feature | Gain creator for | Pain reliever for |
|---|---|---|
| Automatic aggregation of accounts and cards | J1, J2 — one picture instead of five apps | No manual copying; no "where is that account?" |
| Automatic categorisation of transactions | J1 — see spending by category | No spreadsheet; no end-of-month guesswork |
| Safe-to-spend balance | J2 — a number that answers "can I buy this?" | No mental arithmetic; no fear of overdraft |
| Bill calendar and reminders | J3 — pay on time | No missed due dates; no late fee |
| Recurring-payment and subscription detector | J6 — see what is charged regularly | No forgotten subscriptions; no surprise charges |
| Low-balance and overdraft alerts | J4 — act before the fee | No nasty surprise at the till |
| Round-ups / automatic savings | J5 — save without a separate task | No "I'll start saving next month" |
| Budget targets with progress | J2, J5 — plan and adjust | No guilt-only budgeting; no vague goals |
| Merchant and category insights | J1 — understand habits | No manual analysis |
| Privacy controls: local data, masked balances, app lock | J7 — control who sees what | No fear of someone seeing the balance |
| Export to CSV / bank-grade encryption | J7 — own the data | No lock-in; no plain-text data |

### Where the fit is strong, partial or absent

| Area | Fit | Why |
|---|---|---|
| Aggregation, categorisation, safe-to-spend, bill reminders | **Strong** | These are the app's own functions |
| Subscription detection, round-ups, budget targets | **Partial** | Depend on bank feeds and user habits |
| Financial advice, debt restructuring, investment returns | **Absent** | Outside a personal-finance assistant's scope |

## Short conclusion

The app's strongest gain creators are a single picture of the money and a "safe to spend"
number; its strongest pain relievers are bill reminders and subscription detection. It does
not remove the need for a human adviser when the problem is debt or investing.
