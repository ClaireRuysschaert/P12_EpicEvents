import unittest
from unittest import mock
from unittest.mock import MagicMock, patch
from epicevents.models import StaffUser, EpicUser, EpicContract
from epicevents.views.contracts_submenu import epic_contracts_menu
from constants import DEPARTMENTS_BY_ID
from epicevents.controllers.contract import (
    get_all_contracts,
    create_contract,
    get_contracts_by_staff_id,
    get_contract_by_user_id,
    get_contracts_with_due_amount,
    is_contract_exists,
    is_staff_contract_commercial_contact,
)


class ContractsTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_session = MagicMock()
        self.mock_query = MagicMock()
        self.mock_session.query.return_value = self.mock_query
        self.mock_query.filter.return_value = self.mock_query
        self.contract = EpicContract(
            client_id=1,
            total_amount=500,
            amount_due=250,
            created_on="2023-10-10",
            status="Signed",
            commercial_contact=1,
        )

    def test_get_all_contracts(self):
        with patch("epicevents.controllers.contract.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = get_all_contracts()
            self.assertIsNotNone(result)

    def test_create_contract(self):
        with patch("epicevents.controllers.contract.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            user_created = create_contract(1, 200, 200, "Signed", 1)
            self.assertIsNotNone(user_created)

    def test_client_get_contract_methods(self):
        with patch("epicevents.controllers.contract.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = get_contracts_by_staff_id(self.contract.commercial_contact)
            self.assertIsNotNone(result)
            result = get_contract_by_user_id(self.contract.client_id)
            self.assertIsNotNone(result)
            result = get_contracts_with_due_amount()
            self.assertIsNotNone(result)

    def test_is_contract_exists(self):
        with patch("epicevents.controllers.contract.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = is_contract_exists(self.contract.contract_id)
            self.assertIsNotNone(result)

    def test_is_staff_contract_commercial_contact(self):
        with patch("epicevents.controllers.contract.get_session") as mock_get_session:
            mock_get_session.return_value = (None, self.mock_session)
            result = is_staff_contract_commercial_contact(
                self.contract.commercial_contact,
                self.contract.contract_id,
            )
            self.assertIsNotNone(result)

    @patch("epicevents.controllers.contract.get_session")
    @patch("epicevents.models.EpicContract.get_all_contracts")
    def test_get_all_contracts_none(self, mock_get_all_contracts, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_all_contracts.return_value = None
        result = get_all_contracts()
        self.assertIsNone(result)

    @patch("epicevents.controllers.contract.get_session")
    @patch("epicevents.models.EpicContract.get_contracts_by_staff_id")
    def test_get_contracts_by_staff_id_none(
        self, mock_get_contracts_by_staff_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_contracts_by_staff_id.return_value = None
        result = get_contracts_by_staff_id(1)
        self.assertIsNone(result)

    @patch("epicevents.controllers.contract.get_session")
    @patch("epicevents.models.EpicContract.get_contracts_by_client_id")
    def test_get_contract_by_user_id_none(
        self, mock_get_contracts_by_client_id, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_contracts_by_client_id.return_value = None
        result = get_contract_by_user_id(1)
        self.assertIsNone(result)

    @patch("epicevents.controllers.contract.get_session")
    @patch("epicevents.models.EpicContract.get_contracts_with_due_amount")
    def test_get_contracts_with_due_amount_none(
        self, mock_get_contracts_with_due_amount, mock_get_session
    ):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_contracts_with_due_amount.return_value = None
        result = get_contracts_with_due_amount()
        self.assertIsNone(result)

    @patch("epicevents.controllers.contract.get_session")
    @patch("epicevents.models.EpicContract.get_contract_by_id")
    def test_is_contract_exists_none(self, mock_get_contract_by_id, mock_get_session):
        mock_get_session.return_value = (None, self.mock_session)
        mock_get_contract_by_id.return_value = None
        result = is_contract_exists(self.contract.contract_id)
        self.assertIsNone(result)


class TestContractsMenu(unittest.TestCase):
    def setUp(self) -> None:
        self.manager = StaffUser(
            first_name="Manager",
            last_name="Manager",
            email="manager@test.com",
            password="password",
            department_id=DEPARTMENTS_BY_ID["management"],
        )
        self.commercial = StaffUser(
            first_name="Commercial",
            last_name="Commercial",
            email="commercial@test.com",
            password="password",
            department_id=DEPARTMENTS_BY_ID["commercial"],
        )
        self.support = StaffUser(
            first_name="Support",
            last_name="Support",
            email="support@test.com",
            password="password",
            department_id=DEPARTMENTS_BY_ID["support"],
        )
        self.client = EpicUser(
            first_name="Client",
            last_name="Client",
            assign_to=self.commercial.staff_id,
        )
        self.management_department_id = DEPARTMENTS_BY_ID["management"]
        self.commercial_department_id = DEPARTMENTS_BY_ID["commercial"]
        self.support_department_id = DEPARTMENTS_BY_ID["support"]

    @patch("epicevents.views.main_menu.click.prompt")
    @patch("epicevents.views.main_menu.click.echo")
    @patch("epicevents.views.main_menu.click.secho")
    @patch("epicevents.views.contracts_submenu.display_all_contracts_table")
    def test_read_contracts_by_departments(
        self, mock_table, mock_secho, mock_echo, mock_prompt
    ):
        # Support department can't see contracts
        mock_prompt.side_effect = [1, 6]
        try:
            epic_contracts_menu(
                department_id=self.support.department_id,
                staff_id=self.support.staff_id,
            )
        except SystemExit:
            pass
        mock_table.assert_not_called()

        # Manager and Commercial departments can see contracts
        mock_prompt.side_effect = [1, 6]
        try:
            epic_contracts_menu(
                department_id=self.manager.department_id, staff_id=self.manager.staff_id
            )
        except SystemExit:
            pass

        mock_prompt.side_effect = [1, 6]
        try:
            epic_contracts_menu(
                department_id=self.commercial.department_id,
                staff_id=self.commercial.staff_id,
            )
        except SystemExit:
            pass

        assert mock_table.call_count == 2
        mock_table.assert_has_calls(
            [
                mock.call(department_id=self.management_department_id),
                mock.call(department_id=self.commercial_department_id),
            ]
        )
