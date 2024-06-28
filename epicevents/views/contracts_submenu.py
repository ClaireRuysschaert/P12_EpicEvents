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
from epicevents.controllers.client import (  # noqa
    has_client_assign_to_commercial,
    is_client_exists,
)
from epicevents.controllers.contract import (  # noqa
    create_contract,
    get_all_contracts,
    get_contract_by_staff_id,
    get_contract_by_user_id,
    get_contract_with_due_amount,
    is_contract_exists,
)
from epicevents.controllers.permissions import has_permission  # noqa
from epicevents.models import EpicContract, EpicUser  # noqa
from epicevents.views.errors import (  # noqa
    display_contract_update_error,
    display_epic_user_not_found_error,
)
from utils import is_commercial_team  # noqa
from validators import (  # noqa
    validate_amount_due,
    validate_client_id,
    validate_commercial_id,
    validate_total_amount,
)


def get_client_id_by_asking_id() -> Union[int, None]:
    if DEPARTMENTS_BY_ID["commercial"]:
        click.echo("Please enter the client id")
        user_id = click.prompt("Enter the client id", type=int)
        if is_client_exists(user_id):
            return user_id
        display_epic_user_not_found_error()
        return None
    return None


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
def display_all_contracts_table(
    department_id: int,
):
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


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
def display_contracts_by_filters_table(
    department_id: int,
    staff_id: int = None,
    user_id: int = None,
    filter_name: str = None,
):

    if staff_id:
        contracts = get_contract_by_staff_id(staff_id=staff_id)
    elif user_id:
        contracts = get_contract_by_user_id(user_id=user_id)
    elif filter_name == "amount due":
        contracts = get_contract_with_due_amount()
    elif filter_name == "to sign":
        contracts = get_all_contracts()
        contracts = [contract for contract in contracts if contract.status == "To sign"]
    else:
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


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["commercial"]])
def epic_contracts_filtered_menu(department_id: int, staff_id: int):
    """
    Display contracts based on filters.
    """
    from epicevents.views.main_menu import main_menu

    while True:
        click.secho("\nWhich contract do you want to display ?\n", bold=True)
        click.echo("1. See my assigned contracts")
        click.echo("2. See all contracts of a client")
        click.echo("3. See contracts by amound due or signing status")
        click.echo("4. Return to main menu")
        click.echo("5. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            display_contracts_by_filters_table(
                department_id=department_id, staff_id=staff_id
            )

        elif choice == 2:
            user_id = get_client_id_by_asking_id()
            if user_id:
                display_contracts_by_filters_table(
                    department_id=department_id, user_id=user_id
                )
            else:
                main_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 3:
            click.secho(
                "Filter contracts based on outstanding amount or signing status",
                bold=True,
            )
            filter_name = click.prompt(
                "Enter the contract filter you want to display",
                type=click.Choice(["amount due", "to sign"], case_sensitive=False),
            )
            display_contracts_by_filters_table(
                department_id=department_id, filter_name=filter_name
            )

        elif choice == 4:
            main_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 5:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")
            main_menu(department_id=department_id, staff_id=staff_id)


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
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


@has_permission(departments_allowed=[DEPARTMENTS_BY_ID["management"]])
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
    existing_commercial_id = has_client_assign_to_commercial(client_id)
    if existing_commercial_id:
        commercial_contact = existing_commercial_id
    else:
        commercial_contact = click.prompt(
            "Enter the commercial contact", type=int, value_proc=validate_commercial_id
        )
        # Save the commercial contact to the EpicUser table
        EpicUser.assign_commercial_to_epic_user(client_id, commercial_contact)

    create_contract(client_id, total_amount, amount_due, status, commercial_contact)
    click.echo(click.style("\nContract created successfully:", fg="green", bold=True))
    click.echo(click.style(f"Client ID: {client_id}", fg="blue"))
    click.echo(click.style(f"Total amount: {total_amount}", fg="blue"))
    click.echo(click.style(f"Amount due: {amount_due}", fg="blue"))
    click.echo(click.style(f"Status: {status}", fg="blue"))
    click.echo(click.style(f"Commercial contact: {commercial_contact}\n", fg="blue"))


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
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


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
def get_contract_by_asking_id(department_id: int) -> Union[EpicContract, None]:
    click.echo("Please enter the contract id to update")
    contract_id = click.prompt("Enter the contract id", type=int)
    contract = is_contract_exists(contract_id)
    return contract


@has_permission(
    departments_allowed=[
        DEPARTMENTS_BY_ID["management"],
        DEPARTMENTS_BY_ID["commercial"],
    ]
)
def epic_contracts_menu(department_id: int, staff_id: int):
    """
    CRU operations for contracts.
    Users can not delete contracts.
    """
    from epicevents.views.main_menu import main_menu

    while True:
        click.secho("\nContracts menu\n", bold=True)
        click.echo("1. See all contracts")
        click.echo("2. See specific contracts by filters")
        click.echo("3. Create a contract")
        click.echo("4. Update a contract")
        click.echo("5. Return to main menu")
        click.echo("6. Exit\n")

        choice = click.prompt("Enter your choice\n", type=int)

        if choice == 1:
            display_all_contracts_table(department_id=department_id)

        elif choice == 2:
            epic_contracts_filtered_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 3:
            display_contract_creation(department_id=department_id)

        elif choice == 4:
            contract = get_contract_by_asking_id(department_id=department_id)

            if contract:
                # Commercial can only update contracts they are assigned to
                if (
                    is_commercial_team(department_id=department_id)
                    and contract.commercial_contact != staff_id
                ):
                    display_contract_update_error()
                    main_menu(department_id=department_id)
                display_contract(contract, department_id=department_id)
                display_update_contract_menu(contract, department_id=department_id)
                display_all_contracts_table(department_id=department_id)
            else:
                click.secho("\nContract not found", fg="red")

        elif choice == 5:
            main_menu(department_id=department_id, staff_id=staff_id)

        elif choice == 6:
            sys.exit(0)

        else:
            click.secho("Invalid choice", fg="red")
            main_menu(department_id=department_id, staff_id=staff_id)
