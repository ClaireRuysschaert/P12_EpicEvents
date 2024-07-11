import unittest
from constants import DEPARTMENTS_BY_ID
from utils import is_management_team, is_commercial_team, is_support_team

class UtilsTestCase(unittest.TestCase):
    def setUp(self):
        self.management_id = DEPARTMENTS_BY_ID["management"]
        self.commercial_id = DEPARTMENTS_BY_ID["commercial"]
        self.support_id = DEPARTMENTS_BY_ID["support"]

    def test_is_management_team(self):
        self.assertTrue(is_management_team(self.management_id))
        self.assertFalse(is_management_team(self.commercial_id))
        self.assertFalse(is_management_team(self.support_id))

    def test_is_commercial_team(self):
        self.assertTrue(is_commercial_team(self.commercial_id))
        self.assertFalse(is_commercial_team(self.management_id))
        self.assertFalse(is_commercial_team(self.support_id))

    def test_is_support_team(self):
        self.assertTrue(is_support_team(self.support_id))
        self.assertFalse(is_support_team(self.management_id))
        self.assertFalse(is_support_team(self.commercial_id))
