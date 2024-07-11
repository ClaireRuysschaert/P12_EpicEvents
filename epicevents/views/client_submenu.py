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
from epicevents.controllers.epic_user import (  # noqa
    create_user,
    get_all_users,
    is_client_exists,
)
from epicevents.controllers.permissions import has_permission  # noqa
from epicevents.models import EpicUser  # noqa
from validators import validate_email, validate_phone_number  # noqa


def display_all_clients_table(department_id: int) -> None:
    """
    Display a table with all clients.
    """
    users = get_all_users()
    data = []
    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Company",
        "Assign To",
    ]
    for user in users:
        data.append(
            [
                user.user_id,
                user.first_name,
                user.last_name,
                user.email,
                user.phone,
                user.company,
                user.assign_to,
            ]
        )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo(table)
    click.echo("\n")


def display_created_client(department_id: int, staff_id: int) -> None:
    """
    Create and display information about a client.
    Format the first name and last name to capitalize the first letter.
    """
    email = click.prompt(
        "Enter client email to create", type=str, value_proc=validate_email
    )
    phone = click.prompt(
        "Enter client phone number", type=str, value_proc=validate_phone_number
    )
    first_name = click.prompt("Enter client first name", type=str).capitalize()
    last_name = click.prompt("Enter client last name", type=str).capitalize()
    company = click.prompt("Enter client company", type=str)
    assign_to = staff_id
    create_user(
        first_name,
        last_name,
        email=email,
        phone=phone,
        company=company,
        assign_to=assign_to,
    )
    click.echo(click.style("\nUser created successfully:", fg="green", bold=True))
    click.echo(click.style(f"First Name: {first_name}", fg="blue"))
    click.echo(click.style(f"Last Name: {last_name}", fg="blue"))
    click.echo(click.style(f"Email: {email}", fg="blue"))
    click.echo(click.style(f"Department: {phone}", fg="blue"))
    click.echo(click.style(f"Company: {company}", fg="blue"))
    click.echo(click.style(f"Assign To: {assign_to}", fg="blue"))


def get_user_by_asking_id(department_id: int) -> Union[EpicUser, None]:
    """
    Fetch the user by asking the user ID, and return the user if found.
    Otherwise, return None.
    """
    user_id = click.prompt("Please enter the user ID to update", type=int)
    user = is_client_exists(user_id)
    return user


def display_client(user: EpicUser, department_id: int) -> None:
    """
    Display the client information in a table.
    """
    data = []
    headers = [
        "User ID",
        "First Name",
        "Last Name",
        "Email",
        "Phone",
        "Company",
        "Assign To",
    ]
    data.append(
        [
            user.user_id,
            user.first_name,
            user.last_name,
            user.email,
            user.phone,
            user.company,
            user.assign_to,
        ]
    )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo("Client informations\n")
    click.echo(table)
    click.echo("\n")


def display_update_user_menu(user: EpicUser, department_id: int) -> None:
    """
    Display a menu for updating client information.
    """
    click.echo("What field do you want to update?")
    click.echo("1. First Name")
    click.echo("2. Last Name")
    click.echo("3. Email")
    click.echo("4. Phone")
    click.echo("5. Company")
    click.echo("6. Cancel update\n")

    to_update = click.prompt("Enter your choice", type=int)
    if to_update == 1:
        first_name = click.prompt("Enter the new first name").capitalize()
        EpicUser.update(user.user_id, first_name=first_name)
    elif to_update == 2:
        last_name = click.prompt("Enter the new last name").capitalize()
        EpicUser.update(user.user_id, last_name=last_name)
    elif to_update == 3:
        email = click.prompt("Enter the new email")
        EpicUser.update(user.user_id, email=email)
    elif to_update == 4:
        phone = click.prompt("Enter the new phone number")
        EpicUser.update(user.user_id, phone=phone)
    elif to_update == 5:
        company = click.prompt("Enter the new company")
        EpicUser.update(user.user_id, company=company)
    elif to_update == 6:
        return
    else:
        click.secho("Invalid choice", fg="red")


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["commercial"]])
def client_menu(department_id: int, staff_id: int) -> None:
    """
    Display a menu for managing clients.
    """
    while True:
        click.secho("\nClient menu\n", bold=True)
        click.echo("1. See all clients")
        click.echo("2. Create a client")
        click.echo("3. Update a client")
        click.echo("4. Return to main menu")
        click.echo("5. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            display_all_clients_table(department_id)
        elif choice == 2:
            display_created_client(department_id, staff_id)
        elif choice == 3:
            user = get_user_by_asking_id(department_id=department_id)
            if user and user.assign_to == staff_id:
                display_client(user, department_id=department_id)
                display_update_user_menu(user, department_id=department_id)
                display_all_clients_table(department_id=department_id)
            else:
                if not user:
                    click.secho("\nUser not found", fg="red")
                else:
                    click.secho("\nYou are not allowed to update this user", fg="red")
        elif choice == 4:
            from epicevents.views.main_menu import main_menu

            main_menu(department_id=department_id)
        elif choice == 5:
            sys.exit(0)
