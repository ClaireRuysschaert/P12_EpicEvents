import sys
from pathlib import Path
from typing import Union

# Adds the project path to the system's path. This allows
# to import modules from the project.
project_path = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_path)


import click  # noqa
from tabulate import tabulate  # noqa

from constants import DEPARTMENTS_BY_ID  # noqa
from epicevents.controllers.contract import is_staff_contract_commercial_contact  # noqa
from epicevents.controllers.events import (  # noqa
    create_events,
    get_all_events,
    get_all_staff_events,
    is_event_exists,
)
from epicevents.controllers.permissions import has_permission  # noqa
from epicevents.models import EpicEvent  # noqa
from epicevents.views.errors import display_staff_not_commercial_contact_error  # noqa
from utils import is_commercial_team, is_management_team, is_support_team  # noqa
from validators import (  # noqa
    validate_attendees,
    validate_contract_id,
    validate_date,
    validate_support_id,
)


@has_permission(
    departments_allowed=[DEPARTMENTS_BY_ID["management"], DEPARTMENTS_BY_ID["support"]]
)
def get_event_by_asking_id(department_id: int) -> Union[EpicEvent, None]:
    """
    Fetch an event by asking the user to input the event id and return
    the event if exists. If not found, return None.
    """
    click.echo("Please enter the event id to update")
    event_id = click.prompt("Enter the event id", type=int)
    event = is_event_exists(event_id)
    return event


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["commercial"],
        DEPARTMENTS_BY_ID["support"],
    ]
)
def display_all_events_table(
    department_id: int, staff_id: int = None, show_only_no_support: bool = False
) -> None:
    """
    Displays a table of all events, option to filter events with a support contact.

    This function retrieves all events or all events associated with a specific
    staff member, depending on whether a staff ID is provided. It then formats this
    information into a table and prints it. There is also an option to only display
    events that currently do not have a support contact assigned.
    """
    if staff_id:
        events = get_all_staff_events(staff_id=staff_id)
    else:
        events = get_all_events()
    data = []
    headers = [
        "Event ID",
        "Contract ID",
        "Commercial Contact",
        "Start Date",
        "End Date",
        "Support Contact",
        "Location",
        "Attendees",
        "Notes",
    ]
    for event in events:
        if show_only_no_support and event.support_contact is not None:
            continue  # Skip events with support contact
        data.append(
            [
                event.id,
                event.contract_id,
                event.contract.commercial_contact,
                event.start_date,
                event.end_date,
                event.support_contact,
                event.location,
                event.attendees,
                event.notes,
            ]
        )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo(table)
    click.echo("\n")


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["support"],
    ]
)
def display_event(event: EpicEvent, department_id: int) -> None:
    """
    Display informations about an event.
    """
    data = []
    headers = [
        "Event ID",
        "Contract ID",
        "Commercial Contact",
        "Start Date",
        "End Date",
        "Support Contact",
        "Location",
        "Attendees",
        "Notes",
    ]
    data.append(
        [
            event.id,
            event.contract_id,
            event.contract.commercial_contact,
            event.start_date,
            event.end_date,
            event.support_contact,
            event.location,
            event.attendees,
            event.notes,
        ]
    )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo("Contract informations\n")
    click.echo(table)
    click.echo("\n")


def display_event_menu(department_id: int) -> None:
    """
    Display the CRU event menu.
    """
    click.secho("\nEvents menu\n", bold=True)
    click.echo("1. See all events")
    click.echo("2. Create an event")
    click.echo("3. Update an event")
    click.echo("4. Return to main menu")
    click.echo("5. Exit")

    if is_management_team(department_id=department_id):
        click.echo("6. See events where there is no support assigned\n")
    elif is_support_team(department_id=department_id):
        click.echo("6. See my assigned events\n")
    else:
        click.echo("\n")


@has_permission(
    departments_allowed=[DEPARTMENTS_BY_ID["management"], DEPARTMENTS_BY_ID["support"]]
)
def display_update_event_menu(event: EpicEvent, department_id: int) -> None:
    """
    Display a menu for updating event information.
    Management team can only associate a support to an event.
    Support team can update all fields of their assigned events.
    """
    if is_management_team(department_id=department_id):
        click.echo("You can update the associated support to the event.")
        new_support_id = click.prompt(
            "Enter the new support contact id", type=int, value_proc=validate_support_id
        )
        EpicEvent.update(event.id, support_contact=new_support_id)
    else:
        click.echo("What field do you want to update?")
        click.echo("1. Start Date")
        click.echo("2. End Date")
        click.echo("3. Support Contact")
        click.echo("4. Location")
        click.echo("5. Attendees")
        click.echo("6. Notes")
        click.echo("7. Cancel update\n")
        to_update = click.prompt("Enter your choice", type=int)

        if to_update == 1:
            start_date = click.prompt(
                "Enter the new start date", type=str, value_proc=validate_date
            )
            EpicEvent.update(event.id, start_date=start_date)
        elif to_update == 2:
            end_date = click.prompt(
                "Enter the new end date", type=str, value_proc=validate_date
            )
            EpicEvent.update(event.id, end_date=end_date)
        elif to_update == 3:
            support_contact = click.prompt(
                "Enter the new support contact",
                type=int,
                value_proc=validate_support_id,
            )
            EpicEvent.update(event.id, support_contact=support_contact)
        elif to_update == 4:
            location = click.prompt("Enter the new location", type=str).capitalize()
            EpicEvent.update(event.id, location=location)
        elif to_update == 5:
            attendees = click.prompt(
                "Enter the new attendees number",
                type=int,
                value_proc=validate_attendees,
            )
            EpicEvent.update(event.id, attendees=attendees)
        elif to_update == 6:
            notes = click.prompt("Enter the new notes", type=str)
            EpicEvent.update(event.id, notes=notes)
        elif to_update == 7:
            click.echo("Update canceled")
            return
        else:
            click.secho("Invalid choice", fg="red")


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
def display_events_creation(department_id: int, staff_id: int) -> None:
    """
    Create and display information about an event.
    """
    contract_id = click.prompt(
        "\nEnter the contract id", type=int, value_proc=validate_contract_id
    )
    if is_staff_contract_commercial_contact(staff_id, contract_id):
        start_date = click.prompt(
            "Enter the event start date in YYYY-MM-DD format",
            type=str,
            value_proc=validate_date,
        )
        end_date = click.prompt(
            "Enter the event end date in YYYY-MM-DD format",
            type=str,
            value_proc=validate_date,
        )
        support_contact = click.prompt(
            "Enter the support contact", type=int, value_proc=validate_support_id
        )
        location = click.prompt("Enter the event location", type=str).capitalize()
        attendees = click.prompt(
            "Enter the event attendees number", type=int, value_proc=validate_attendees
        )
        notes = click.prompt("Enter the event notes", type=str)

        create_events(
            contract_id,
            start_date,
            end_date,
            support_contact,
            location,
            attendees,
            notes,
        )
        click.echo(click.style("\nEvent created successfully:", fg="green", bold=True))
        click.echo(click.style(f"Contract ID: {contract_id}", fg="blue"))
        click.echo(click.style(f"Start date: {start_date}", fg="blue"))
        click.echo(click.style(f"End date: {end_date}", fg="blue"))
        click.echo(click.style(f"Support contact: {support_contact}", fg="blue"))
        click.echo(click.style(f"Location: {location}", fg="blue"))
        click.echo(click.style(f"Attendees: {attendees}", fg="blue"))
        click.echo(click.style(f"Notes: {notes}\n", fg="blue"))
    else:
        display_staff_not_commercial_contact_error()


def update_event_permission_check(
    event: EpicEvent, is_support_team: bool, staff_id: int, department_id: int
) -> None:
    """
    Check permsssion to update an event. Support team can only update their
    assigned events.
    """
    if is_support_team and event.support_contact != staff_id:
        click.secho("\nYou are not the support contact of the event\n", fg="red")
        epic_events_menu(department_id=department_id, staff_id=staff_id)
    return None


def fetch_event_or_notify_failure(
    department_id: int, staff_id: int
) -> Union[EpicEvent, None]:
    """
    Fetch event by asking the user to input the event id.
    Return event only if found and the user is in commercial team.
    If not, notify the user and return None.
    """
    event = get_event_by_asking_id(department_id=department_id)
    if is_commercial_team(department_id=department_id):
        epic_events_menu(department_id=department_id, staff_id=staff_id)
        return None
    elif event:
        return event
    else:
        click.secho("\nEvent not found", fg="red")
        epic_events_menu(department_id=department_id, staff_id=staff_id)
        return None


def event_update(department_id: int, staff_id: int) -> None:
    """
    Update and display to staff an event.
    """
    event = fetch_event_or_notify_failure(
        department_id=department_id, staff_id=staff_id
    )
    update_event_permission_check(event, is_support_team, staff_id, department_id)
    display_event(event, department_id=department_id)
    display_update_event_menu(event, department_id=department_id)
    display_all_events_table(department_id=department_id)


def epic_events_menu(department_id: int, staff_id: int, token: str = None) -> None:
    """
    CRU operations for events.
    Users can not delete events.
    """
    from epicevents.views.main_menu import main_menu

    while True:
        display_event_menu(department_id=department_id)
        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            display_all_events_table(department_id=department_id)

        elif choice == 2:
            display_events_creation(department_id=department_id, staff_id=staff_id)

        elif choice == 3:
            event_update(department_id=department_id, staff_id=staff_id)

        elif choice == 4:
            main_menu(department_id=department_id, staff_id=staff_id, token=token)

        elif choice == 5:
            sys.exit(0)

        elif choice == 6:
            if is_management_team(department_id=department_id):
                display_all_events_table(
                    department_id=department_id, show_only_no_support=True
                )
            elif is_support_team(department_id=department_id):
                display_all_events_table(department_id=department_id, staff_id=staff_id)

        else:
            click.secho("Invalid choice", fg="red")
            main_menu(department_id=department_id, staff_id=staff_id, token=token)
