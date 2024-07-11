import sys
from pathlib import Path

# Adds the project path to the system's path. This allows
# to import modules from the project.
project_path = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_path)


import click  # noqa

from epicevents.controllers.staff_user import authenticate_user  # noqa
from validators import validate_email  # noqa


def get_department_id_by_asking_login() -> int:
    """
    Login staff user.
    Verify the email and password, and return the department_id and staff_id.
    """
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
    staff_id = user_login.staff_id
    return department_id, staff_id


def main_menu(department_id: int = None, staff_id: int = None) -> None:
    """
    Display main menu, login and redirect to the desired submenu.
    Can redirect to the staff, contracts, events, or client submenu.
    """
    # Login
    if department_id is None:
        click.echo("\nWelcome to the dashboard!\n")
        department_id, staff_id = get_department_id_by_asking_login()
    else:
        pass

    while True:
        # Menu
        click.secho("\nMain menu\n", bold=True)
        click.secho("\nWhat do you want to do?\n", bold=True)
        click.echo("1. See the staff menu")
        click.echo("2. See the contracts menu")
        click.echo("3. See the events menu")
        click.echo("4. See the client menu")
        click.echo("5. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            from epicevents.views.user_staff_submenu import staff_user_menu

            staff_user_menu(department_id=department_id)

        elif choice == 2:
            from epicevents.views.contracts_submenu import epic_contracts_menu

            epic_contracts_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 3:
            from epicevents.views.events_submenu import epic_events_menu

            epic_events_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 4:
            from epicevents.views.client_submenu import client_menu

            client_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 5:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")


if __name__ == "__main__":
    main_menu()
