"""
Lead Management System
=======================

A beginner-friendly command-line app for tracking sales leads.

Features
--------
- Add a lead (name, email, phone, source, status, notes)
- List all leads in a clean table
- Update a lead's status
- Search leads by name or email (case-insensitive, partial match)
- Filter leads by status or by source
- Dashboard: total leads, counts by status, conversion rate

Data is stored in a local JSON file (leads.json) in the same folder,
so your leads are still there the next time you run the app.

Run it with:
    python3 lead_manager.py

No external packages are needed — Python 3.8+ standard library only.
"""

import json
import os

# File that stores the leads, next to this script.
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "leads.json")

# The only statuses a lead is allowed to have.
ALLOWED_STATUSES = ["new", "contacted", "qualified", "converted", "lost"]

# Common sources a lead can come from (free text is also fine).
COMMON_SOURCES = ["website", "referral", "social media", "cold call", "event"]


# ---------------------------------------------------------------------------
# Data handling
# ---------------------------------------------------------------------------

def load_leads():
    """Load the lead list from leads.json.

    Returns an empty list if the file does not exist yet or is empty.
    """
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            print("Warning: leads.json is damaged — starting with an empty list.")
            return []
    # Make sure we always work with a list.
    return data if isinstance(data, list) else []


def save_leads(leads):
    """Save the lead list to leads.json (nicely formatted)."""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, indent=2)


def next_id(leads):
    """Return the next free lead id (one more than the highest existing id)."""
    if not leads:
        return 1
    return max(lead["id"] for lead in leads) + 1


# ---------------------------------------------------------------------------
# Display helpers
# ---------------------------------------------------------------------------

def print_lead_table(leads):
    """Print leads as a simple aligned table."""
    if not leads:
        print("\nNo leads to show.\n")
        return

    # Column widths.
    id_w = 4
    name_w = max(len(lead["name"]) for lead in leads)
    name_w = max(name_w, 4)
    email_w = max(len(lead["email"]) for lead in leads)
    email_w = max(email_w, 5)
    status_w = max(len(lead["status"]) for lead in leads)
    status_w = max(status_w, 6)
    source_w = max(len(lead["source"]) for lead in leads)
    source_w = max(source_w, 6)

    header = (
        f"{'ID':<{id_w}}  {'Name':<{name_w}}  "
        f"{'Email':<{email_w}}  {'Status':<{status_w}}  {'Source':<{source_w}}"
    )
    print("\n" + header)
    print("-" * len(header))
    for lead in leads:
        print(
            f"{lead['id']:<{id_w}}  {lead['name']:<{name_w}}  "
            f"{lead['email']:<{email_w}}  {lead['status']:<{status_w}}  "
            f"{lead['source']:<{source_w}}"
        )
    print()


def show_dashboard(leads):
    """Print the dashboard: totals, counts by status, conversion rate."""
    total = len(leads)
    print("\n========== Dashboard ==========")
    print(f"Total leads: {total}")
    if total == 0:
        print("No leads yet — add your first lead from the menu.")
        print("==============================\n")
        return

    for status in ALLOWED_STATUSES:
        count = sum(1 for lead in leads if lead["status"] == status)
        print(f"  {status.capitalize():<10} : {count}")

    converted = sum(1 for lead in leads if lead["status"] == "converted")
    conversion_rate = (converted / total) * 100
    print(f"\nConversion rate: {conversion_rate:.1f}% "
          f"({converted} converted out of {total})")
    print("==============================\n")


# ---------------------------------------------------------------------------
# Lead actions
# ---------------------------------------------------------------------------

def add_lead(leads):
    """Ask the user for lead details, validate them, and save the new lead."""
    print("\n--- Add a new lead ---")

    name = input("Name: ").strip()
    if not name:
        print("Name cannot be empty. Lead not added.\n")
        return leads

    email = input("Email: ").strip()
    if not email:
        print("Email cannot be empty. Lead not added.\n")
        return leads
    if "@" not in email or "." not in email.split("@")[-1]:
        print("That does not look like a valid email address. Lead not added.\n")
        return leads

    phone = input("Phone (optional): ").strip()
    print(f"Source — common options: {', '.join(COMMON_SOURCES)}")
    source = input("Source: ").strip() or "website"

    print(f"Status — allowed: {', '.join(ALLOWED_STATUSES)}")
    status = input("Status [new]: ").strip().lower() or "new"
    if status not in ALLOWED_STATUSES:
        print(f"'{status}' is not a valid status. Lead not added.\n")
        return leads

    notes = input("Notes (optional): ").strip()

    new_lead = {
        "id": next_id(leads),
        "name": name,
        "email": email,
        "phone": phone,
        "source": source,
        "status": status,
        "notes": notes,
    }
    leads.append(new_lead)
    save_leads(leads)
    print(f"\nLead added! {name} (ID {new_lead['id']}) is now '{status}'.\n")
    return leads


def list_leads(leads):
    """Show every lead."""
    print("\n--- All leads ---")
    print_lead_table(leads)


def find_lead_by_id(leads, lead_id):
    """Return the lead with the given id, or None if there is no such lead."""
    for lead in leads:
        if lead["id"] == lead_id:
            return lead
    return None


def update_status(leads):
    """Change the status of one lead, chosen by its id number."""
    print("\n--- Update a lead's status ---")
    print_lead_table(leads)
    if not leads:
        return leads

    raw = input("Enter the lead ID to update: ").strip()
    if not raw.isdigit():
        print("Please enter a number (the lead ID). Nothing was changed.\n")
        return leads

    lead = find_lead_by_id(leads, int(raw))
    if lead is None:
        print(f"No lead with ID {raw}. Nothing was changed.\n")
        return leads

    print(f"\nUpdating: {lead['name']} ({lead['email']}) — current status: {lead['status']}")
    print(f"Allowed statuses: {', '.join(ALLOWED_STATUSES)}")
    new_status = input("New status: ").strip().lower()
    if new_status not in ALLOWED_STATUSES:
        print(f"'{new_status}' is not a valid status. Nothing was changed.\n")
        return leads

    lead["status"] = new_status
    save_leads(leads)
    print(f"\n{lead['name']} is now '{new_status}'.\n")
    return leads


def search_leads(leads):
    """Search leads by name or email (case-insensitive, partial match)."""
    print("\n--- Search leads ---")
    query = input("Search by name or email: ").strip().lower()
    if not query:
        print("Please type something to search for.\n")
        return

    matches = [
        lead for lead in leads
        if query in lead["name"].lower() or query in lead["email"].lower()
    ]
    print(f"\nFound {len(matches)} lead(s) matching '{query}':")
    print_lead_table(matches)


def filter_leads(leads):
    """Show only the leads that match a chosen status or source."""
    print("\n--- Filter leads ---")
    print("1. Filter by status")
    print("2. Filter by source")
    choice = input("Choose 1 or 2: ").strip()

    if choice == "1":
        print(f"Allowed statuses: {', '.join(ALLOWED_STATUSES)}")
        status = input("Status: ").strip().lower()
        if status not in ALLOWED_STATUSES:
            print(f"'{status}' is not a valid status.\n")
            return
        matches = [lead for lead in leads if lead["status"] == status]
        print(f"\n{len(matches)} lead(s) with status '{status}':")
        print_lead_table(matches)

    elif choice == "2":
        source = input("Source: ").strip().lower()
        if not source:
            print("Please type a source to filter by.\n")
            return
        matches = [lead for lead in leads if lead["source"].lower() == source]
        print(f"\n{len(matches)} lead(s) from source '{source}':")
        print_lead_table(matches)

    else:
        print("Please choose 1 or 2.\n")


# ---------------------------------------------------------------------------
# Menu
# ---------------------------------------------------------------------------

def show_menu():
    """Print the main menu."""
    print("===== Lead Management System =====")
    print("1. Dashboard")
    print("2. List all leads")
    print("3. Add a lead")
    print("4. Update a lead's status")
    print("5. Search leads")
    print("6. Filter leads")
    print("0. Quit")
    print("==================================")


def main():
    """Run the menu loop until the user chooses to quit."""
    leads = load_leads()
    print(f"\nWelcome! Loaded {len(leads)} lead(s) from leads.json.")

    while True:
        show_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            show_dashboard(leads)
        elif choice == "2":
            list_leads(leads)
        elif choice == "3":
            leads = add_lead(leads)
        elif choice == "4":
            leads = update_status(leads)
        elif choice == "5":
            search_leads(leads)
        elif choice == "6":
            filter_leads(leads)
        elif choice == "0":
            print("\nGoodbye! Your leads are saved in leads.json.\n")
            break
        else:
            print("\nPlease choose a number from the menu (0–6).\n")


if __name__ == "__main__":
    main()
