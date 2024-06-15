import click


def display_permission_error():
    """
    Display permission error message.
    """
    click.secho("/nYou do not have permission to access this action./n", fg="red")
    return None
