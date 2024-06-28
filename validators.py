from datetime import datetime
from typing import Union
import click
import re
from epicevents.models import EpicUser, StaffUser, EpicContract
from utils import get_session
from constants import DEPARTMENTS_BY_ID


def validate_email(email: str) -> Union[str, None]:
    """
    Validates if the given email address is valid.
    """
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise click.BadParameter("The email is not valid")
    return email


def validate_client_id(client_id: int) -> Union[int, None]:
    """
    Verifies if the client exists in the database.
    """
    _, session = get_session()
    client = EpicUser.get_epic_user_by_id(session, user_id=client_id)
    if not client:
        raise click.BadParameter("The client_id is not valid")
    return client_id


def validate_total_amount(total_amount: float) -> Union[float, None]:
    """
    Verifies if the total amount is a positive number.
    """
    if int(total_amount) < 0:
        raise click.BadParameter("Total amount cannot be negative.")
    return total_amount


def validate_amount_due(amount_due: float, total_amount: float) -> Union[float, None]:
    """
    Verifies if the amount due is a positive number.
    """
    if float(amount_due) > float(total_amount) or int(amount_due) < 0:
        raise click.BadParameter("Amount due cannot be greater than total amount.")
    return amount_due


def validate_commercial_id(staff_id: int) -> Union[int, None]:
    """
    Verifies if the staff exists in the database and is in commercial department.
    """
    _, session = get_session()
    staff: StaffUser = StaffUser.get_user_by_id(session, staff_id=staff_id)
    if not staff:
        raise click.BadParameter("The staff id is not valid")
    if staff.department_id != DEPARTMENTS_BY_ID["commercial"]:
        raise click.BadParameter("The staff is not in commercial department")
    return staff_id


def validate_contract_id(contract_id: int) -> Union[int, None]:
    """
    Verifies if the contract exists in the database.
    """
    _, session = get_session()
    contract = EpicContract.get_contract_by_id(session, contract_id=contract_id)
    if not contract:
        raise click.BadParameter("The contract_id is not valid")
    return contract_id


def validate_date(date: str) -> Union[datetime, None]:
    """
    Verifies if the date is in the correct format and if it's in the future.
    """
    try:
        parsed_date = datetime.strptime(date, '%Y-%m-%d')
        if parsed_date < datetime.now():
            raise click.BadParameter("The date must be in the future")
        return parsed_date
    except ValueError:
        raise click.BadParameter('Date must be in YYYY-MM-DD format')


def validate_support_id(support_contact: int) -> Union[int, None]:
    """
    Verifies if the support contact exists in the database.
    """
    _, session = get_session()
    support: StaffUser = StaffUser.get_user_by_id(session, staff_id=support_contact)
    if not support:
        raise click.BadParameter("The support contact is not valid")
    if support.department_id != DEPARTMENTS_BY_ID["support"]:
        raise click.BadParameter("The staff is not in support department")
    return support_contact


def validate_attendees(attendees: int) -> Union[int, None]:
    """
    Verifies if the number of attendees is a positive number.
    """
    if int(attendees) < 0:
        raise click.BadParameter("Number of attendees cannot be negative.")
    return attendees
