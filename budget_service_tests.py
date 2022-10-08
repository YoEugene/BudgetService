from datetime import datetime
from decimal import Decimal
from budget_service import BudgetService
from budget_interface import Budget, BudgetsInterface
import unittest


class BudgetTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.budget_service = BudgetService()

    def test_mock_date_should_not_be_empty(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
            ]
        )
        self.budget_service.get_budgets_from_db()

        self.assertEqual(len(self.budget_service.budgets) > 0, True)

    def test_should_get_full_month_budget_private(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
            ]
        )
        self.budget_service.get_budgets_from_db()

        test_date = datetime(2022, 10, 2)
        budget = self.budget_service._get_month_budget(test_date)
        self.assertEqual(budget, 3100)

    def test_should_get_budget_by_partial_month_private(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202301", 310),
            ]
        )
        self.budget_service.get_budgets_from_db()

        start_date = datetime(2022, 10, 2)
        end_date = datetime(2022, 10, 10)
        budget = self.budget_service._get_budget_by_partial_month(start_date, end_date)
        self.assertEqual(budget, 900)

    def test_should_get_budget_by_full_month_private(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 31),
                Budget("202301", 310),
                Budget("202302", 999),
            ]
        )
        self.budget_service.get_budgets_from_db()

        test_date = datetime(2022, 10, 2)
        budget = self.budget_service._get_budget_by_full_month(test_date)
        self.assertEqual(budget, 3100)

    def test_should_get_budget_by_month_start_private(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 31),
                Budget("202301", 310),
                Budget("202501", 123),
            ]
        )
        self.budget_service.get_budgets_from_db()

        test_date = datetime(2022, 10, 28)
        budget = self.budget_service._get_budget_with_start_date(test_date)
        self.assertEqual(budget, 400)

    def test_should_get_budget_by_month_end_private(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 31),
                Budget("202301", 310),
            ]
        )
        self.budget_service.get_budgets_from_db()

        test_date = datetime(2022, 10, 3)
        budget = self.budget_service._get_budget_with_end_date(test_date)
        self.assertEqual(budget, 300)

    def test_should_get_budget_within_same_month(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 31),
                Budget("202301", 310),
            ]
        )

        start_date = datetime(2022, 10, 3)
        end_date = datetime(2022, 10, 5)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(300))

    def test_should_get_budget_across_multiple_months(self):
        BudgetsInterface.inject_mock_data(
            [
                Budget("202210", 3100),
                Budget("202211", 300),
                Budget("202212", 31),
                Budget("202301", 310),
            ]
        )

        start_date = datetime(2022, 10, 28)
        end_date = datetime(2023, 3, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(1041))

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


if __name__ == "__main__":
    unittest.main()
