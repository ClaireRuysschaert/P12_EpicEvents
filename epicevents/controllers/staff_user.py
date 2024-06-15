from typing import Optional

from constants import DEPARTMENTS_BY_ID
from utils import get_session

from ..models import StaffUser


def authenticate_user(email: str, password: str) -> Optional[StaffUser]:
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


def is_staff_exists(staff_id: int) -> StaffUser:
    _, session = get_session()
    staff: StaffUser = StaffUser.get_user_by_id(session, staff_id)
    if staff:
        return staff
    else:
        return None


def get_all_staff_users() -> list[StaffUser]:
    _, session = get_session()
    all_users = StaffUser.get_all_staffusers(session)
    return all_users
