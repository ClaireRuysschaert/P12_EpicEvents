import unittest
from unittest.mock import MagicMock, patch
from epicevents.controllers.epic_user import (
    get_all_users,
    create_user,
    has_client_assign_to_commercial,
    is_client_exists,
)
from epicevents.models import EpicUser


class EpicUserTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_query = MagicMock()
        self.mock_session.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_query
        self.client = EpicUser(
            user_id=1,
            first_name="Test",
            last_name="Test",
            email="test@test.com",
            assign_to=1,
        )

    def test_get_all_users(self):
        with patch("epicevents.controllers.epic_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = get_all_users()
            self.assertIsNotNone(result)

    def test_create_user(self):
        with patch("epicevents.controllers.epic_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            user_created = create_user(
                "Test FN", "Test LN", "email@email.fr", "123456789", "Company", 1
            )
            self.assertIsNotNone(user_created)

    def test_client_assign_to_commercial(self):
        with patch("epicevents.controllers.epic_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = has_client_assign_to_commercial(self.client.user_id)
            self.assertIsNotNone(result)

    def test_with_no_client_assign_to_commercial(self):
        with patch("epicevents.controllers.epic_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            self.mock_query.first.return_value = None
            h = has_client_assign_to_commercial(2)
            self.assertIsNone(h)

    def test_is_client_exists(self):
        with patch("epicevents.controllers.epic_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = is_client_exists(self.client.user_id)
            self.assertIsNotNone(result)

    def test_is_client_exists_no_client(self):
        with patch("epicevents.controllers.epic_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            self.mock_query.first.return_value = None
            result = is_client_exists(2)
            self.assertIsNone(result)
