import unittest
from unittest import mock
from unittest.mock import patch
from epicevents.models import StaffUser, EpicUser
from epicevents.views.contracts_submenu import epic_contracts_menu
from constants import DEPARTMENTS_BY_ID


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
    @patch("epicevents.views.main_menu.display_all_contracts_table")
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
