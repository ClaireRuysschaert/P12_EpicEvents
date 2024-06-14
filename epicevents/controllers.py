from typing import Optional
from sqlalchemy.orm import Session
from .models import StaffUser
from functools import wraps
import click
from constants import DEPARTMENTS_BY_ID
from utils import validate_email, get_session, validate_email_callback


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


def create_staff_users(first_name: str, last_name: str, email : str, password: str, department: str) -> StaffUser:
    _, session = get_session()
    department_id = DEPARTMENTS_BY_ID[department]
    new_user = StaffUser(
        last_name=last_name, first_name=first_name, email=email, department_id=department_id, password=password
    )
    new_user.hash_password(password)
    session.add(new_user)
    session.commit()
    return new_user

def is_staff_exists(staff_id:int) -> StaffUser:
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





# def has_permission(permission):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             user: StaffUser = kwargs.get('user')
#             departments_allowed = kwargs.get('departments_allowed')
#             if user and user.department_id in departments_allowed:
#                 return func(*args, **kwargs)
#             else:
#                 raise PermissionError(f"User does not have the {permission} permission")
#         return wrapper
#     return decorator
