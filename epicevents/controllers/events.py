from typing import Union

from utils import get_session

from ..models import EpicEvent


def get_all_events() -> Union[list[EpicEvent], None]:
    """
    Fetch all events from the database. If no events found, return None.
    """
    _, session = get_session()
    events = EpicEvent.get_all_events(session)
    if events:
        return events
    return None


def get_all_staff_events(staff_id: int) -> Union[list[EpicEvent], None]:
    """
    Fetch all events where the staff is the support contact.
    If no events found, return None.
    """
    _, session = get_session()
    events = EpicEvent.get_all_staff_events(session, staff_id)
    if events:
        return events
    return None


def create_events(
    contract_id: int,
    start_date: str,
    end_date: str,
    support_contact: int,
    location: str,
    attendees: int,
    notes: str,
) -> EpicEvent:
    """
    Create a new event in the database.
    """
    _, session = get_session()
    new_event = EpicEvent(
        contract_id=contract_id,
        start_date=start_date,
        end_date=end_date,
        support_contact=support_contact,
        location=location,
        attendees=attendees,
        notes=notes,
    )
    session.add(new_event)
    session.commit()
    return new_event


def is_event_exists(id: int) -> Union[list[EpicEvent], None]:
    """
    Verifies if an event exists in the database by the event id.
    If not found, return None.
    """
    _, session = get_session()
    event: EpicEvent = EpicEvent.get_event_by_id(session, id)
    if event:
        return event
    return None
