import unittest
from unittest.mock import MagicMock, patch
from epicevents.models import StaffUser
from epicevents.controllers.staff_user import (
    is_staff_exists,
    get_all_staff_users,
    create_staff_users,
)


class StaffUserTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_query = MagicMock()
        self.mock_session.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_query
        self.client = StaffUser(
            staff_id=1,
            first_name="Test",
            last_name="Test",
            email="test@test.com",
            password="password",
            department_id=1,
        )

    def test_is_staffuser_exists(self, mock_get_session):
        with patch("epicevents.controllers.staff_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = is_staff_exists(self.client.staff_id)
            self.assertIsNotNone(result)

    def test_is_staffuser_exists_no_client(self):
        with patch("epicevents.controllers.staff_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            self.mock_query.first.return_value = None
            result = is_staff_exists(2)
            self.assertIsNone(result)

    def test_get_all_staff_users(self):
        with patch("epicevents.controllers.staff_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = get_all_staff_users()
            self.assertIsNotNone(result)

    def test_create_staffuser(self):
        with patch("epicevents.controllers.staff_user.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            user_created = create_staff_users(
                "Test FN", "Test LN", "email@email.fr", "password", "support"
            )
            self.assertEqual(user_created.department_id, 3)
            self.assertTrue(user_created.password.startswith("$argon2id$"))
            self.assertIsNotNone(user_created)
