from datetime import datetime
from decimal import Decimal
from budget_service import Budget, BudgetService, BudgetsInterface
import unittest


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.budgets = BudgetsInterface.get_all()
        self.budget_service = BudgetService()

    def test_should_be_mock_date(self):
        self.assertEqual(len(self.budgets) > 0, True)  # add assertion here

    def test_should_get_full_month_budget_private(self):
        test_date = datetime(2022, 10, 2)
        budget = self.budget_service.get_month_budget(test_date)
        self.assertEqual(budget, 3100)

    def test_should_get_partial_month_budget(self):
        start_date = datetime(2022, 10, 2)
        end_date = datetime(2022, 10, 10)
        budget = self.budget_service.get_budget_by_partial_month(start_date, end_date)
        self.assertEqual(budget, 900)

    def test_should_get_partial_month_budget(self):
        start_date = datetime(2022, 10, 2)
        end_date = datetime(2022, 10, 10)
        budget = self.budget_service.get_budget_by_partial_month(start_date, end_date)
        self.assertEqual(budget, 900)

    def test_should_get_full_month_budget(self):
        test_date = datetime(2022, 10, 2)
        budget = self.budget_service.get_budget_by_full_month(test_date)
        self.assertEqual(budget, 3100)

    def test_should_get_budget_by_month_start(self):
        test_date = datetime(2022, 10, 28)
        budget = self.budget_service.get_budget_by_month_start(test_date)
        self.assertEqual(budget, 400)

    def test_should_get_budget_by_month_end(self):
        test_date = datetime(2022, 10, 3)
        budget = self.budget_service.get_budget_by_month_end(test_date)
        self.assertEqual(budget, 300)

    def test_should_get_month_delta(self):
        test_date_start = datetime(2022, 10, 28)
        test_date_end = datetime(2023, 3, 3)
        month_delta = self.budget_service.get_month_delta(
            test_date_start, test_date_end
        )
        self.assertEqual(month_delta, 5)

    def test_should_be_single_month(self):
        start_date = datetime(2022, 10, 3)
        end_date = datetime(2022, 10, 5)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(300))

    def test_should_be_two_months(self):
        start_date = datetime(2022, 10, 28)
        end_date = datetime(2022, 11, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(430))

    def test_should_be_multiple_months(self):
        start_date = datetime(2021, 10, 28)
        end_date = datetime(2023, 3, 3)
        budget = self.budget_service.query(start_date, end_date)
        self.assertEqual(budget, Decimal(3431))


if __name__ == "__main__":
    unittest.main()
