import unittest
from unittest.mock import patch
from epicevents.views.user_staff_submenu import staff_user_menu
from constants import DEPARTMENTS_BY_ID


class TestStaffUserMenu(unittest.TestCase):
    @patch("epicevents.views.main_menu.click.prompt")
    @patch("epicevents.views.main_menu.click.echo")  # don't display anything
    @patch("epicevents.views.main_menu.click.secho")  # don't display anything
    @patch("epicevents.views.main_menu.display_all_staff_users_table")
    def test_all_users_are_displayed(
        self, mock_table, mock_secho, mock_echo, mock_prompt
    ):
        department_id = DEPARTMENTS_BY_ID["management"]
        mock_prompt.side_effect = [1, 6]
        try:
            staff_user_menu(department_id=department_id)
        except SystemExit:
            pass
        mock_table.assert_called_once_with(department_id=department_id)

    @patch("epicevents.views.main_menu.click.prompt")
    @patch("epicevents.views.main_menu.click.echo")
    @patch("epicevents.views.main_menu.click.secho")
    @patch("epicevents.views.main_menu.display_all_staff_users_table")
    @patch("epicevents.controllers.permissions.display_permission_error")
    def test_cant_access_menu_without_permission(
        self, mock_error, mock_table, mock_secho, mock_echo, mock_prompt
    ):
        department_id = DEPARTMENTS_BY_ID["commercial"]
        mock_prompt.return_value = 1
        staff_user_menu(department_id=department_id)
        mock_table.assert_not_called()
        mock_error.assert_called_once()
