# Lead Management System

A simple command-line app to track sales leads — add them, update their status, search, filter, and see a dashboard with your conversion rate. All data is saved locally in a JSON file.

## Features

- **Add leads** — name, email, phone, source, status, and notes, with input validation
- **List all leads** — clean, easy-to-read table
- **Update status** — move a lead through `new → contacted → qualified → converted / lost`
- **Search** — find leads by name or email (case-insensitive, partial match)
- **Filter** — show only leads with a chosen status or from a chosen source
- **Dashboard** — total leads, counts by status, and conversion rate
- **Local storage** — leads are saved in `leads.json`, so nothing is lost when you quit

## Requirements

- Python 3.8 or newer (no external packages needed — standard library only)

## Installation

```bash
git clone https://github.com/<your-username>/lead-management-system.git
cd lead-management-system
```

That's it. There is nothing to install.

## Usage

Start the app:

```bash
python3 lead_manager.py
```

Pick an option from the menu:

```text
===== Lead Management System =====
1. Dashboard
2. List all leads
3. Add a lead
4. Update a lead's status
5. Search leads
6. Filter leads
0. Quit
==================================
```

### Sample session

**1. Dashboard** — see your numbers at a glance:

```text
========== Dashboard ==========
Total leads: 10
  New        : 3
  Contacted  : 2
  Qualified  : 2
  Converted  : 2
  Lost       : 1

Conversion rate: 20.0% (2 converted out of 10)
==============================
```

**2. Add a lead** — choose option `3` and answer the prompts:

```text
--- Add a new lead ---
Name: Hira Shah
Email: hira.shah@example.com
Phone (optional): +92 300 0001111
Source — common options: website, referral, social media, cold call, event
Source: referral
Status — allowed: new, contacted, qualified, converted, lost
Status [new]: new
Notes (optional): Friend of Sara, interested in the starter plan.

Lead added! Hira Shah (ID 11) is now 'new'.
```

**3. Search for a lead** — choose option `5` and type part of a name:

```text
--- Search leads ---
Search by name or email: sar

Found 1 lead(s) matching 'sar':

ID    Name        Email                   Status     Source
------------------------------------------------------------
3     Sara Malik  sara.malik@example.com  qualified  social media
```

**4. Filter by status** — choose option `6`, then `1`, then a status:

```text
--- Filter leads ---
1. Filter by status
2. Filter by source
Choose 1 or 2: 1
Allowed statuses: new, contacted, qualified, converted, lost
Status: qualified

2 lead(s) with status 'qualified':

ID    Name         Email                    Status     Source
--------------------------------------------------------------
3     Sara Malik   sara.malik@example.com   qualified  social media
6     Hassan Raza  hassan.raza@example.com  qualified  event
```

**5. Update a status** — choose option `4`, enter the lead ID, then the new status:

```text
--- Update a lead's status ---
Enter the lead ID to update: 2
Updating: Bilal Ahmed (bilal.ahmed@example.com) — current status: contacted
Allowed statuses: new, contacted, qualified, converted, lost
New status: qualified

Bilal Ahmed is now 'qualified'.
```

Quit any time with option `0` — your leads are already saved.

## How it works

- **Storage:** every lead is a dictionary stored in a list in `leads.json`. The app loads the file when it starts and writes it back every time a lead is added or a status changes, so the data always survives between runs.
- **Dashboard:** it counts the leads in each status, then computes the conversion rate as `converted / total × 100`.
- **Search:** it compares your query (lowercased) against each lead's name and email, so `sar` finds `Sara Malik` and `sara.malik@example.com`.
- **Validation:** empty names and emails are rejected, emails must contain `@` and a dot after it, and a status must be one of `new`, `contacted`, `qualified`, `converted`, `lost`. Unknown lead IDs are reported instead of crashing.

## Sample data

`leads.json` ships with 10 fictional sample leads (names like Ayesha Khan and Bilal Ahmed, `example.com` emails, sample phone numbers) so the dashboard and search work straight away. Use them to explore, then replace them with your own leads — just add leads in the app, or edit `leads.json` directly.

## Project structure

```text
lead-management-system/
├── lead_manager.py   # The whole app (menu, dashboard, search, filter, storage)
├── leads.json        # Your leads, saved as JSON (sample data included)
├── requirements.txt  # No external dependencies
├── .gitignore        # Standard Python ignores
└── README.md         # This file
```

## License

MIT — see the [LICENSE](LICENSE) file, or use the project freely with attribution.
