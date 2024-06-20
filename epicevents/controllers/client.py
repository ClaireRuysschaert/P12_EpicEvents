from typing import Union

from utils import get_session

from ..models import EpicUser


def has_client_assign_to_commercial(client_id: int) -> Union[int, None]:
    _, session = get_session()
    client: EpicUser = EpicUser.get_epic_user_by_id(session, client_id)
    if client.assign_to:
        return client.assign_to
    return None


def is_client_exists(user_id: int) -> Union[int, None]:
    _, session = get_session()
    client: EpicUser = EpicUser.get_epic_user_by_id(session, user_id=user_id)
    if client:
        return client.user_id
    return None
