from typing import Union
from ..models import EpicEvent
from utils import get_session


def get_all_events() -> Union[list[EpicEvent], None]:
    _, session = get_session()
    events = EpicEvent.get_all_events(session)
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
