import unittest
from unittest.mock import MagicMock, patch
from epicevents.models import EpicEvent
from epicevents.controllers.events import (
    get_all_events,
    get_all_staff_events,
    create_events,
    is_event_exists,
)


class EventsTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_query = MagicMock()
        self.mock_session.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_query
        self.event = EpicEvent(
            contract_id=1,
            start_date="2023-10-10",
            end_date="2023-10-12",
            support_contact=1,
            location="Test Location",
            attendees=100,
            notes="Test Event",
        )

    def test_get_all_events(self):
        with patch("epicevents.controllers.events.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = get_all_events()
            self.assertIsNotNone(result)

    def test_get_all_staff_events(self):
        with patch("epicevents.controllers.events.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = get_all_staff_events(self.event.support_contact)
            self.assertIsNotNone(result)

    def test_create_events(self):
        with patch("epicevents.controllers.events.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            event_created = create_events(
                1, "2023-10-10", "2023-10-12", 1, "Test Location", 100, "Test Event"
            )
            self.assertIsNotNone(event_created)

    def test_is_event_exists(self):
        with patch("epicevents.controllers.events.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = is_event_exists(self.event.id)
            self.assertIsNotNone(result)


if __name__ == '__main__':
    unittest.main()
