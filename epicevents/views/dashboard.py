import sys
from pathlib import Path

# Adds the project path to the system's path. This allows
# to import modules from the project.
project_path = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_path)


import click  # noqa
from tabulate import tabulate  # noqa

from epicevents.controllers import (authenticate_user,  # noqa
                                    create_staff_users, get_all_staff_users,
                                    is_staff_exists)
from epicevents.models import StaffUser  # noqa
from utils import validate_email, validate_email_callback  # noqa


def get_user_staff_by_asking_id(action: str) -> StaffUser:
    click.echo(f"Please enter the staff id to {action}")
    staff_id = click.prompt("Enter the staff id", type=int)
    staff = is_staff_exists(staff_id)
    return staff


def get_department_id_by_asking_login() -> int:
    click.echo("Please login")
    user_login = False
    while user_login is False:
        email = click.prompt("Enter your email", type=str, value_proc=validate_email)
        password = click.prompt("Enter your password", hide_input=True)
        user_login = authenticate_user(email, password)
        if user_login is False:
            click.echo("Invalid email or password, please try again.")
    click.echo(
        "Welcome "
        + click.style(user_login.first_name + " " + user_login.last_name, fg="blue")
        + " !"
    )
    department_id = user_login.department_id
    return department_id


def display_all_staff_users_table():
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


@click.command
@click.option(
    "--email", prompt="Enter staff email to create", callback=validate_email_callback
)
@click.option("--password", prompt="Enter staff password to create", hide_input=True)
@click.option("--first-name", prompt="Enter staff first name")
@click.option("--last-name", prompt="Enter staff last name")
@click.option(
    "--department",
    prompt="Enter staff department",
    type=click.Choice(["management", "support", "commercial"], case_sensitive=False),
)
def display_created_staff_user(
    first_name: str, last_name: str, email: str, password: str, department: str
) -> None:
    """
    Create and display information about a staff user that just.
    Format the first name and last name to capitalize the first letter.
    """
    first_name = first_name.capitalize()
    last_name = last_name.capitalize()
    create_staff_users(first_name, last_name, email, password, department)
    click.echo(click.style("\nUser created successfully:", fg="green", bold=True))
    click.echo(click.style(f"First Name: {first_name}", fg="blue"))
    click.echo(click.style(f"Last Name: {last_name}", fg="blue"))
    click.echo(click.style(f"Email: {email}", fg="blue"))
    click.echo(click.style(f"Department: {department}\n", fg="blue"))


def display_staff_user(staff: StaffUser):
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


def display_update_staff_user_menu(staff: StaffUser):
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
        department_id = click.prompt("Enter the new department id", type=int)
        StaffUser.update(staff.staff_id, department_id=department_id)
    elif to_update == 5:
        click.echo("Update canceled")
        return
    else:
        click.secho("Invalid choice", fg="red")


def display_staff_user_to_delete(staff: StaffUser):
    click.echo("\nStaff user to delete")
    display_staff_user(staff)
    confirm = click.prompt("Press enter to confirm deletion", type=str, default="")
    if confirm == "":
        StaffUser.delete(staff.staff_id)
        click.secho("\nStaff deleted successfully\n", fg="green")
    else:
        click.echo("Deletion canceled")


def staff_user_menu():
    click.echo("Welcome to the staff users menu!\n")
    click.echo("1. See all staff users")
    click.echo("2. Create a staff users")
    click.echo("3. Update a staff user")
    click.echo("4. Delete a staff user")
    click.echo("5. Return to main menu")
    click.echo("6. Exit\n")

    choice = click.prompt("Enter your choice\n", type=int)

    if choice == 1:  # See all staff users
        display_all_staff_users_table()

    elif choice == 2:  # Create a staff user
        display_created_staff_user()

    # Update a staff user
    elif choice == 3:
        staff = get_user_staff_by_asking_id("update")
        if staff:
            display_staff_user(staff)
            display_update_staff_user_menu(staff)
            display_all_staff_users_table()
        else:
            click.secho("\nStaff not found", fg="red")

    # Delete a staff user
    elif choice == 4:
        staff = get_user_staff_by_asking_id("delete")
        if staff:
            display_staff_user_to_delete(staff)
        else:
            click.secho("\nStaff not found", fg="red")

    elif choice == 5:
        main_menu()

    # Exit
    elif choice == 6:
        sys.exit(0)

    else:
        click.secho("Invalid choice", fg="red")
        main_menu()


def main_menu():
    click.echo("\nWelcome to the dashboard!\n")

    # Login
    # department_id = get_department_id_by_asking_login()
    # print(department_id)

    while True:
        # Menu
        click.secho("What do you want to do?\n", bold=True)
        click.echo("1. See the staff users menu")
        click.echo("2. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            staff_user_menu()

        elif choice == 2:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")


if __name__ == "__main__":
    main_menu()
