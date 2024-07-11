import click


def display_permission_error() -> str:
    """
    Display permission error message.
    """
    error_message = "You do not have permission to access this action."
    click.secho(error_message, fg="red")
    return error_message


def display_contract_update_error() -> str:
    """
    Display contract update error message.
    """
    error_message = (
        "\nYour commercial id doesn't fit the contract commercial."
        "\nYou're not allowed to update this contract\n"
    )
    click.secho(error_message, fg="red")
    return error_message


def display_epic_user_not_found_error() -> str:
    """
    Display epic user not found error message.
    """
    error_message = "\nEpic user not found\n"
    click.secho(error_message, fg="red")
    return error_message


def display_staff_not_commercial_contact_error() -> str:
    """
    Display staff not commercial contact error message.
    """
    error_message = "\nYou are not the commercial contact of the contract\n"
    click.secho(error_message, fg="red")
    return error_message
