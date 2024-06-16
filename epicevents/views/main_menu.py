import sys
from pathlib import Path

# Adds the project path to the system's path. This allows
# to import modules from the project.
project_path = str(Path(__file__).parent.parent.parent)
sys.path.insert(0, project_path)


import click  # noqa
from tabulate import tabulate  # noqa

from epicevents.controllers.contract import (create_contract,  # noqa
                                             get_all_contracts,
                                             is_contract_exists)
from epicevents.controllers.permissions import has_permission  # noqa
from epicevents.controllers.staff_user import (authenticate_user,  # noqa
                                               create_staff_users,
                                               get_all_staff_users,
                                               is_staff_exists)
from epicevents.models import EpicContract, StaffUser  # noqa
from validators import (validate_amount_due, validate_client_id,  # noqa
                        validate_commercial_id, validate_email,
                        validate_total_amount)


@has_permission(departments_allowed=[1])
def get_user_staff_by_asking_id(action: str, department_id: int) -> StaffUser:
    click.echo(f"Please enter the staff id to {action}")
    staff_id = click.prompt("Enter the staff id", type=int)
    staff = is_staff_exists(staff_id)
    return staff


def get_contract_by_asking_id(department_id: int) -> EpicContract:
    click.echo("Please enter the contract id to update")
    contract_id = click.prompt("Enter the contract id", type=int)
    contract = is_contract_exists(contract_id)
    return contract


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


@has_permission(departments_allowed=[1])
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


@has_permission(departments_allowed=[1])
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


@has_permission(departments_allowed=[1])
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


@has_permission(departments_allowed=[1])
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


@has_permission(departments_allowed=[1])
def display_staff_user_to_delete(staff: StaffUser, department_id: int):
    click.echo("\nStaff user to delete")
    display_staff_user(staff, department_id=department_id)
    confirm = click.prompt("Press enter to confirm deletion", type=str, default="")
    if confirm == "":
        StaffUser.delete(staff.staff_id)
        click.secho("\nStaff deleted successfully\n", fg="green")
    else:
        click.echo("Deletion canceled")


@has_permission(departments_allowed=[1])
def staff_user_menu(department_id: int):
    while True:
        click.secho("Staff user menu\n", bold=True)
        click.echo("1. See all staff users")
        click.echo("2. Create a staff users")
        click.echo("3. Update a staff user")
        click.echo("4. Delete a staff user")
        click.echo("5. Return to main menu")
        click.echo("6. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

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
            main_menu(department_id=department_id)

        # Exit
        elif choice == 6:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")
            main_menu()


def display_all_contracts_table(department_id: int):
    contracts = get_all_contracts()
    data = []
    headers = [
        "Contract ID",
        "Client ID",
        "Total Amount",
        "Amount Due",
        "Status",
        "Commercial Contact",
    ]
    for contract in contracts:
        data.append(
            [
                contract.contract_id,
                contract.client_id,
                contract.total_amount,
                contract.amount_due,
                contract.status,
                contract.commercial_contact,
            ]
        )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo(table)
    click.echo("\n")


def display_contract(contract: EpicContract, department_id: int):
    data = []
    headers = [
        "Contract ID",
        "Client ID",
        "Total Amount",
        "Amount Due",
        "Status",
        "Commercial Contact",
    ]
    data.append(
        [
            contract.contract_id,
            contract.client_id,
            contract.total_amount,
            contract.amount_due,
            contract.status,
            contract.commercial_contact,
        ]
    )
    table = tabulate(data, headers=headers, tablefmt="pretty")
    click.echo("\n")
    click.echo("Contract informations\n")
    click.echo(table)
    click.echo("\n")


def display_contract_creation(department_id: int):
    """
    Create and display information about a contract.
    """
    client_id = click.prompt(
        "\nEnter the client id", type=int, value_proc=validate_client_id
    )
    total_amount = click.prompt(
        "Enter the contract total amount", type=float, value_proc=validate_total_amount
    )
    amount_due = click.prompt(
        "Enter the contract amount due",
        type=float,
        default=total_amount,
        show_default=True,
        value_proc=lambda amount_due: validate_amount_due(amount_due, total_amount),
    )
    status = click.prompt(
        "Enter the contract status",
        type=click.Choice(["To sign", "Signed", "Cancelled"], case_sensitive=False),
    )
    commercial_contact = click.prompt(
        "Enter the commercial contact", type=int, value_proc=validate_commercial_id
    )

    create_contract(client_id, total_amount, amount_due, status, commercial_contact)
    click.echo(click.style("\nContract created successfully:", fg="green", bold=True))
    click.echo(click.style(f"Client ID: {client_id}", fg="blue"))
    click.echo(click.style(f"Total amount: {total_amount}", fg="blue"))
    click.echo(click.style(f"Amount due: {amount_due}", fg="blue"))
    click.echo(click.style(f"Status: {status}", fg="blue"))
    click.echo(click.style(f"Commercial contact: {commercial_contact}\n", fg="blue"))


def display_update_contract_menu(contract: EpicContract, department_id: int):
    """
    Display a menu for updating contract information.
    """
    click.echo("What field do you want to update?")
    click.echo("1. Client ID")
    click.echo("2. Total Amount")
    click.echo("3. Amount Due")
    click.echo("4. Status")
    click.echo("5. Commercial Contact")
    click.echo("6. Cancel update\n")
    to_update = click.prompt("Enter your choice", type=int)

    if to_update == 1:
        client_id = click.prompt(
            "Enter the new client id", type=int, value_proc=validate_client_id
        )
        EpicContract.update(contract.contract_id, client_id=client_id)
    elif to_update == 2:
        total_amount = click.prompt(
            "Enter the new total amount", type=float, value_proc=validate_total_amount
        )
        EpicContract.update(contract.contract_id, total_amount=total_amount)
    elif to_update == 3:
        total_amount = contract.total_amount
        amount_due = click.prompt(
            "Enter the new amount due",
            type=float,
            value_proc=lambda amount_due: validate_amount_due(amount_due, total_amount),
        )
        EpicContract.update(contract.contract_id, amount_due=amount_due)
    elif to_update == 4:
        status = click.prompt(
            "Enter the new status",
            type=click.Choice(["To sign", "Signed", "Cancelled"], case_sensitive=False),
        )
        EpicContract.update(contract.contract_id, status=status)
    elif to_update == 5:
        commercial_contact = click.prompt(
            "Enter the new commercial contact",
            type=int,
            value_proc=validate_commercial_id,
        )
        EpicContract.update(contract.contract_id, commercial_contact=commercial_contact)
    elif to_update == 6:
        click.echo("Update canceled")
        return
    else:
        click.secho("Invalid choice", fg="red")


def epic_contracts_menu(department_id: int):
    """
    CRU operations for contracts.
    Users can not delete contracts.
    """
    while True:
        click.secho("Main menu\n", bold=True)
        click.echo("1. See all contracts")
        click.echo("2. Create a contract")
        click.echo("3. Update a contract")
        click.echo("4. Return to main menu")
        click.echo("5. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            display_all_contracts_table(department_id=department_id)

        elif choice == 2:
            display_contract_creation(department_id=department_id)

        elif choice == 3:
            click.echo("Update a contract")
            contract = get_contract_by_asking_id(department_id=department_id)
            if contract:
                display_contract(contract, department_id=department_id)
                display_update_contract_menu(contract, department_id=department_id)
                display_all_contracts_table(department_id=department_id)
            else:
                click.secho("\nContract not found", fg="red")

        elif choice == 4:
            main_menu(department_id=department_id)

        elif choice == 5:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")
            main_menu()


def main_menu(department_id: int = None):

    # Login
    if department_id is None:
        click.echo("\nWelcome to the dashboard!\n")
        department_id = get_department_id_by_asking_login()
    else:
        pass

    while True:
        # Menu
        click.secho("Main menu\n", bold=True)
        click.secho("\nWhat do you want to do?\n", bold=True)
        click.echo("1. See the staff menu")
        click.echo("2. See the contracts menu")
        click.echo("3. See the events menu")
        click.echo("4. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            staff_user_menu(department_id=department_id)

        elif choice == 2:
            epic_contracts_menu(department_id=department_id)

        elif choice == 4:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")


if __name__ == "__main__":
    main_menu()
