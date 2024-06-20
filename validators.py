import click
import re
from epicevents.models import EpicUser, StaffUser
from utils import get_session


def validate_email(email: str):
    """
    Validates if the given email address is valid.
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise click.BadParameter("The email is not valid")
    return email


def validate_client_id(client_id: int):
    """
    Verifies if the client exists in the database.
    """
    _, session = get_session()
    client = EpicUser.get_epic_user_by_id(session, user_id=client_id)
    if not client:
        raise click.BadParameter("The client_id is not valid")
    return client_id


def validate_total_amount(total_amount: float):
    """
    Verifies if the total amount is a positive number.
    """
    if int(total_amount) < 0:
        raise click.BadParameter("Total amount cannot be negative.")
    return total_amount


def validate_amount_due(amount_due: float, total_amount: float):
    """
    Verifies if the amount due is a positive number.
    """
    if float(amount_due) > float(total_amount) or int(amount_due) < 0:
        raise click.BadParameter("Amount due cannot be greater than total amount.")
    return amount_due


def validate_commercial_id(staff_id: int):
    """
    Verifies if the staff exists in the database and is in commercial department.
    """
    _, session = get_session()
    staff: StaffUser = StaffUser.get_user_by_id(session, staff_id=staff_id)
    if not staff:
        raise click.BadParameter("The staff id is not valid")
    if staff.department_id != 2:
        raise click.BadParameter("The staff is not in commercial department")
    return staff_id
