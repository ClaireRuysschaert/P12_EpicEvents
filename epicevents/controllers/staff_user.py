from typing import Union

from constants import DEPARTMENTS_BY_ID
from utils import get_session

from ..models import StaffUser


def authenticate_user(email: str, password: str) -> Union[StaffUser, None]:
    """
    Authenticate the user with the given email and password.
    Verifies the hashed password stored in the database with the given password,
    checks if the password needs rehashing, and rehashes the password if needed.

    If the user is found and the password is correct, return the user.
    Otherwise, return False.
    """
    _, session = get_session()
    user: StaffUser = StaffUser.get_user_by_email(session, email)

    if user and user.verify_password(session, email, password):
        if user.check_password_needs_rehash():
            user.hash_password(password)
            session.commit()
        return user
    else:
        return False


def create_staff_users(
    first_name: str, last_name: str, email: str, password: str, department: str
) -> StaffUser:
    """
    Create a new staff user in the database.
    """
    _, session = get_session()
    department_id = DEPARTMENTS_BY_ID[department]
    new_user = StaffUser(
        last_name=last_name,
        first_name=first_name,
        email=email,
        department_id=department_id,
        password=password,
    )
    new_user.hash_password(password)
    session.add(new_user)
    session.commit()
    return new_user


def is_staff_exists(staff_id: int) -> Union[StaffUser, None]:
    """
    Verifies if the staff exists in the database by its id. If not found, return None.
    """
    _, session = get_session()
    staff: StaffUser = StaffUser.get_user_by_id(session, staff_id)
    if staff:
        return staff
    return None


def get_all_staff_users() -> list[StaffUser]:
    """
    Fetch all staff users from the database
    """
    _, session = get_session()
    all_users = StaffUser.get_all_staffusers(session)
    return all_users
