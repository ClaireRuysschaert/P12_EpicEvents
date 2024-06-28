from typing import Union

from utils import get_session

from ..models import EpicUser


def get_all_users() -> list[EpicUser]:
    _, session = get_session()
    all_users = EpicUser.get_all_users(session)
    return all_users


def create_user(
    first_name: str,
    last_name: str,
    email: str,
    phone: str,
    company: str,
    assign_to: int,
) -> EpicUser:
    _, session = get_session()
    new_user = EpicUser(
        last_name=last_name,
        first_name=first_name,
        email=email,
        phone=phone,
        company=company,
        assign_to=assign_to,
    )
    session.add(new_user)
    session.commit()
    return new_user


def is_user_exists(user_id: int) -> Union[EpicUser, None]:
    _, session = get_session()
    user: EpicUser = EpicUser.get_epic_user_by_id(session, user_id)
    if user:
        return user
    else:
        return None
