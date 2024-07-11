from datetime import datetime, timedelta
import unittest
from unittest.mock import MagicMock, patch

import click
from epicevents.models import StaffUser, EpicUser, EpicContract
from validators import (
    validate_attendees,
    validate_email,
    validate_client_id,
    validate_phone_number,
    validate_total_amount,
    validate_amount_due,
    validate_commercial_id,
    validate_contract_id,
    validate_date,
    validate_support_id,
)

from constants import DEPARTMENTS_BY_ID


class ValidatorsTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.email = "test@test.com"
        self.wrong_emails = ("test@test", "", " ", "test.com")
        self.mock_session = MagicMock()
        self.mock_query = MagicMock()
        self.mock_session.query.return_value = self.mock_query
        self.staff = StaffUser(
            staff_id=1, first_name="Test", last_name="Test", email="test@test.com"
        )
        self.client = EpicUser(
            user_id=1, first_name="Test", last_name="Test", email="test@test.com"
        )
        self.contract = EpicContract(
            contract_id=1,
            client_id=1,
            commercial_contact=1,
            total_amount=100.0,
            amount_due=50.0,
            status="Signed",
        )

    def test_email_validator(self):
        self.assertTrue(validate_email(self.email))
        for email in self.wrong_emails:
            with self.assertRaises(click.BadParameter):
                validate_email(email)

    @patch("validators.get_session")
    @patch("epicevents.models.EpicUser.get_epic_user_by_id")
    def test_validate_client_id(self, mock_get_epic_user_by_id, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_epic_user_by_id.return_value = self.client
        self.assertEqual(validate_client_id(self.client.user_id), 1)
        mock_get_epic_user_by_id.assert_called_once_with(self.mock_session, user_id=1)

    @patch("validators.get_session")
    @patch("epicevents.models.EpicUser.get_epic_user_by_id")
    def test_validate_client_id_bad_param(
        self, mock_get_epic_user_by_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_epic_user_by_id.return_value = None
        with self.assertRaises(click.BadParameter) as context:
            validate_client_id(self.client.user_id)
        self.assertEqual(str(context.exception), "The client_id is not valid")
        mock_get_epic_user_by_id.assert_called_once_with(self.mock_session, user_id=1)

    def test_validate_total_amount(self):
        self.assertEqual(validate_total_amount(100.0), 100.0)
        self.assertEqual(validate_total_amount(0.0), 0.0)
        with self.assertRaises(click.BadParameter) as context:
            validate_total_amount(-1.0)
        self.assertEqual(str(context.exception), "Total amount cannot be negative.")

    def test_validate_amount_due(self):
        self.assertEqual(validate_amount_due(50.0, 100.0), 50.0)
        self.assertEqual(validate_amount_due(0.0, 100.0), 0.0)
        with self.assertRaises(click.BadParameter) as context:
            validate_amount_due(150.0, 100.0)
        self.assertEqual(
            str(context.exception), "Amount due cannot be greater than total amount."
        )
        with self.assertRaises(click.BadParameter) as context:
            validate_amount_due(-1.0, 100.0)
        self.assertEqual(
            str(context.exception), "Amount due cannot be greater than total amount."
        )

    @patch("validators.get_session")
    @patch("epicevents.models.StaffUser.get_user_by_id")
    def test_validate_commercial_id_valid(self, mock_get_user_by_id, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        self.staff.department_id = DEPARTMENTS_BY_ID["commercial"]
        mock_get_user_by_id.return_value = self.staff

        self.assertEqual(validate_commercial_id(1), 1)
        mock_get_user_by_id.assert_called_once_with(self.mock_session, staff_id=1)

    @patch("validators.get_session")
    @patch("epicevents.models.StaffUser.get_user_by_id")
    def test_validate_commercial_id_invalid_staff(
        self, mock_get_user_by_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_user_by_id.return_value = None

        with self.assertRaises(click.BadParameter) as context:
            validate_commercial_id(self.staff.staff_id)
        self.assertEqual(str(context.exception), "The staff id is not valid")
        mock_get_user_by_id.assert_called_once_with(self.mock_session, staff_id=1)

    @patch("validators.get_session")
    @patch("epicevents.models.StaffUser.get_user_by_id")
    def test_validate_commercial_id_not_commercial(
        self, mock_get_user_by_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        self.staff.department_id = DEPARTMENTS_BY_ID["management"]
        mock_get_user_by_id.return_value = self.staff

        with self.assertRaises(click.BadParameter) as context:
            validate_commercial_id(1)
        self.assertEqual(
            str(context.exception), "The staff is not in commercial department"
        )
        mock_get_user_by_id.assert_called_once_with(self.mock_session, staff_id=1)

    @patch("validators.get_session")
    @patch("epicevents.models.EpicContract.get_contract_by_id")
    def test_validate_contract_id_valid(
        self, mock_get_contract_by_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_contract_by_id.return_value = self.contract

        self.assertEqual(validate_contract_id(self.contract.contract_id), 1)
        mock_get_contract_by_id.assert_called_once_with(
            self.mock_session, contract_id=1
        )

    @patch("validators.get_session")
    @patch("epicevents.models.EpicContract.get_contract_by_id")
    def test_validate_contract_id_invalid(
        self, mock_get_contract_by_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_contract_by_id.return_value = None

        with self.assertRaises(click.BadParameter) as context:
            validate_contract_id(self.contract.contract_id)
        self.assertEqual(str(context.exception), "The contract_id is not valid")
        mock_get_contract_by_id.assert_called_once_with(
            self.mock_session, contract_id=1
        )

    def test_validate_date_valid_future_date(self):
        future_date = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        parsed_date = validate_date(future_date)
        self.assertEqual(parsed_date.strftime('%Y-%m-%d'), future_date)

    def test_validate_date_invalid_format(self):
        with self.assertRaises(click.BadParameter) as context:
            validate_date("2023/10/10")
        self.assertEqual(str(context.exception), 'Date must be in YYYY-MM-DD format')

    def test_validate_date_past_date(self):
        past_date = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        with self.assertRaises(click.BadParameter) as context:
            validate_date(past_date)
        self.assertEqual(str(context.exception), "The date must be in the future")
    
    @patch('validators.get_session')
    @patch('epicevents.models.StaffUser.get_user_by_id')
    def test_validate_support_id_valid(self, mock_get_user_by_id, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        self.staff.department_id = DEPARTMENTS_BY_ID["support"]
        mock_get_user_by_id.return_value = self.staff
        
        self.assertEqual(validate_support_id(self.staff.staff_id), 1)
        mock_get_user_by_id.assert_called_once_with(self.mock_session, staff_id=1)

    @patch('validators.get_session')
    @patch('epicevents.models.StaffUser.get_user_by_id')
    def test_validate_support_id_invalid_support(self, mock_get_user_by_id, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_user_by_id.return_value = None
        
        with self.assertRaises(click.BadParameter) as context:
            validate_support_id(self.staff.staff_id)
        self.assertEqual(str(context.exception), "The support contact is not valid")
        mock_get_user_by_id.assert_called_once_with(self.mock_session, staff_id=1)

    @patch('validators.get_session')
    @patch('epicevents.models.StaffUser.get_user_by_id')
    def test_validate_support_id_not_support(self, mock_get_user_by_id, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        self.staff.department_id = DEPARTMENTS_BY_ID["management"]
        mock_get_user_by_id.return_value = self.staff
        
        with self.assertRaises(click.BadParameter) as context:
            validate_support_id(self.staff.staff_id)
        self.assertEqual(str(context.exception), "The staff is not in support department")
        mock_get_user_by_id.assert_called_once_with(self.mock_session, staff_id=1)
    
    def test_validate_attendees_valid(self):
        self.assertEqual(validate_attendees(10), 10)
        self.assertEqual(validate_attendees(0), 0)
        with self.assertRaises(click.BadParameter) as context:
            validate_attendees(-1)
        context.exception, "Number of attendees cannot be negative."
    
    def test_validate_phone_number_valid(self):
        valid_phone_number = "0123456789"
        self.assertEqual(validate_phone_number(valid_phone_number), valid_phone_number)

    def test_validate_phone_number_invalid(self):
        invalid_phone_numbers = [
            "123456789",    # Missing leading 0
            "012345678",    # Too short
            "01234567890",  # Too long
            "0A23456789",   # Contains a letter
            "0012345678",   # Starts with 00
        ]
        for phone_number in invalid_phone_numbers:
            with self.assertRaises(click.BadParameter) as context:
                validate_phone_number(phone_number)
            self.assertEqual(str(context.exception), "The phone number is not a valid French number")
