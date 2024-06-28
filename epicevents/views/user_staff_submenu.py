import sys
from pathlib import Path

# Adds the project path to the system's path. This allows
# to import modules from the project.
project_path = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_path)

import click  # noqa
from tabulate import tabulate  # noqa

from constants import DEPARTMENTS_BY_ID  # noqa
from epicevents.controllers.permissions import has_permission  # noqa
from epicevents.controllers.staff_user import (  # noqa
    create_staff_users,
    get_all_staff_users,
    is_staff_exists,
)
from epicevents.models import StaffUser  # noqa
from validators import validate_email  # noqa


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def display_all_staff_users_table(department_id: int):
    users = get_all_staff_users()
    data = []
    headers = ["Staff ID", "First Name", "Last Name", "Email", "Department ID"]
    for user in users:
        data.append(
            [
                user.staff_id,
                user.first_name,
                user.last_name,
                user.email,
                user.department_id,
            ]
        )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo(table)
    click.echo("\n")


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def display_created_staff_user(department_id: int) -> None:
    """
    Create and display information about a staff user.
    Format the first name and last name to capitalize the first letter.
    """
    email = click.prompt(
        "Enter staff email to create", type=str, value_proc=validate_email
    )
    password = click.prompt("Enter staff password to create", type=str, hide_input=True)
    first_name = click.prompt("Enter staff first name", type=str).capitalize()
    last_name = click.prompt("Enter staff last name", type=str).capitalize()
    department = click.prompt(
        "Enter staff department",
        type=click.Choice(
            ["management", "support", "commercial"], case_sensitive=False
        ),
    )

    create_staff_users(first_name, last_name, email, password, department)
    click.echo(click.style("\nUser created successfully:", fg="green", bold=True))
    click.echo(click.style(f"First Name: {first_name}", fg="blue"))
    click.echo(click.style(f"Last Name: {last_name}", fg="blue"))
    click.echo(click.style(f"Email: {email}", fg="blue"))
    click.echo(click.style(f"Department: {department}\n", fg="blue"))


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def get_user_staff_by_asking_id(action: str, department_id: int) -> StaffUser:
    click.echo(f"Please enter the staff id to {action}")
    staff_id = click.prompt("Enter the staff id", type=int)
    staff = is_staff_exists(staff_id)
    return staff


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def display_staff_user(staff: StaffUser, department_id: int):
    data = []
    headers = ["Staff ID", "First Name", "Last Name", "Email", "Department ID"]
    data.append(
        [
            staff.staff_id,
            staff.first_name,
            staff.last_name,
            staff.email,
            staff.department_id,
        ]
    )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo("Staff user informations\n")
    click.echo(table)
    click.echo("\n")


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def display_update_staff_user_menu(staff: StaffUser, department_id: int):
    """
    Displays a menu for updating staff user information.
    """
    click.echo("What field do you want to update?")
    click.echo("1. First Name")
    click.echo("2. Last Name")
    click.echo("3. Email")
    click.echo("4. Department ID")
    click.echo("5. Cancel update\n")

    to_update = click.prompt("Enter your choice", type=int)
    if to_update == 1:
        first_name = click.prompt("Enter the new first name").capitalize()
        StaffUser.update(staff.staff_id, first_name=first_name)
    elif to_update == 2:
        last_name = click.prompt("Enter the new last name").capitalize()
        StaffUser.update(staff.staff_id, last_name=last_name)
    elif to_update == 3:
        email = click.prompt("Enter the new email")
        StaffUser.update(staff.staff_id, email=email)
    elif to_update == 4:
        new_department_id = click.prompt("Enter the new department id", type=int)
        StaffUser.update(staff.staff_id, department_id=new_department_id)
    elif to_update == 5:
        click.echo("Update canceled")
        return
    else:
        click.secho("Invalid choice", fg="red")


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def display_staff_user_to_delete(staff: StaffUser, department_id: int):
    click.echo("\nStaff user to delete")
    display_staff_user(staff, department_id=department_id)
    confirm = click.prompt("Press enter to confirm deletion", type=str, default="")
    if confirm == "":
        StaffUser.delete(staff.staff_id)
        click.secho("\nStaff deleted successfully\n", fg="green")
    else:
        click.echo("Deletion canceled")


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
def staff_user_menu(department_id: int):
    while True:
        click.secho("Staff user menu\n", bold=True)
        click.echo("1. See all staff users")
        click.echo("2. Create a staff users")
        click.echo("3. Update a staff user")
        click.echo("4. Delete a staff user")
        click.echo("5. Return to main menu")
        click.echo("6. Exit\n")

        choice = click.prompt("Enter your choice user\n", type=int)

        if choice == 1:  # See all staff users
            display_all_staff_users_table(department_id=department_id)

        elif choice == 2:  # Create a staff user
            display_created_staff_user(department_id=department_id)

        # Update a staff user
        elif choice == 3:
            staff = get_user_staff_by_asking_id("update", department_id=department_id)
            if staff:
                display_staff_user(staff, department_id=department_id)
                display_update_staff_user_menu(staff, department_id=department_id)
                display_all_staff_users_table(department_id=department_id)
            else:
                click.secho("\nStaff not found", fg="red")

        # Delete a staff user
        elif choice == 4:
            staff = get_user_staff_by_asking_id("delete", department_id=department_id)
            if staff:
                display_staff_user_to_delete(staff, department_id=department_id)
            else:
                click.secho("\nStaff not found", fg="red")

        elif choice == 5:
            from epicevents.views.main_menu import main_menu

            main_menu(department_id=department_id)

        # Exit
        elif choice == 6:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")
            main_menu(department_id=department_id)
