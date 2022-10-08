from datetime import datetime
from decimal import Decimal
from budget_service import BudgetService
from budget_interface import Budget, BudgetsInterface
import unittest


class BudgetTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.budget_service = BudgetService()

    def test_should_be_zero_with_illegal_date_range(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
            ]
        )

        start_date = datetime(2033, 10, 28)
        end_date = datetime(2021, 3, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(0))

    def test_should_be_zero_with_no_overlap_data(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202211", 300),
            ]
        )

        start_date = datetime(2000, 10, 28)
        end_date = datetime(2001, 3, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(0))

    def test_should_get_budget_within_same_month(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
            ]
        )

        start_date = datetime(2022, 10, 3)
        end_date = datetime(2022, 10, 5)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(300))

    def test_should_get_budget_across_two_months(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
            ]
        )

        start_date = datetime(2022, 10, 28)
        end_date = datetime(2022, 11, 6)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(400 + 60))

    def test_should_get_budget_across_three_months(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 30),
            ]
        )

        start_date = datetime(2022, 10, 30)
        end_date = datetime(2023, 3, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(200 + 300 + 30))


if __name__ == "__main__":
    unittest.main()
