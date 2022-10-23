import unittest
from datetime import datetime
from decimal import Decimal
from unittest.mock import patch

from budget_service import Budget, BudgetService


class BudgetServiceTestCase(unittest.TestCase):
    def setUp(self) -> None:
        get_budgets_patcher = patch(
            "budget_service.BudgetService._BudgetService__get_budgets"
        )
        self.fake_get_budgets = get_budgets_patcher.start()
        self.budget_service = BudgetService()
        self.fake_get_budgets.return_value = [Budget("202210", 3100)]

    def given_budgets(self, budgets):
        self.fake_get_budgets.return_value = budgets

    def tearDown(self) -> None:
        patch.stopall()

    def test_should_be_single_month(self):
        self.given_budgets([Budget("202210", 3100)])
        start_date = datetime(2022, 10, 3)
        end_date = datetime(2022, 10, 5)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(300))

    def test_should_be_two_months(self):
        self.given_budgets(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
            ]
        )
        start_date = datetime(2022, 10, 28)
        end_date = datetime(2022, 11, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(Decimal(400 + 30), budget)

    def test_should_be_multiple_months(self):
        self.given_budgets(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 31),
            ]
        )
        start_date = datetime(2022, 10, 28)
        end_date = datetime(2022, 12, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(Decimal(400 + 300 + 3), budget)


if __name__ == "__main__":
    unittest.main()
