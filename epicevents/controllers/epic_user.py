from typing import Union

from utils import get_session

from ..models import EpicUser


def get_all_users() -> list[EpicUser]:
    """
    Fetch all users from the database.
    """
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
    """
    Create a new user in the database.
    """
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


def has_client_assign_to_commercial(client_id: int) -> Union[int, None]:
    """
    Fetch the client assign to commercial contact and return the id.
    If not found, return None.
    """
    _, session = get_session()
    client: EpicUser = EpicUser.get_epic_user_by_id(session, client_id)
    if client:
        return client.assign_to
    return None


def is_client_exists(user_id: int) -> Union[int, None]:
    """
    Verifies if the client exists in the database and return the id.
    If not found, return None.
    """
    _, session = get_session()
    client: EpicUser = EpicUser.get_epic_user_by_id(session, user_id=user_id)
    if client:
        return client.user_id
    return None
