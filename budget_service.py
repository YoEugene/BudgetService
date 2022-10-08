from datetime import datetime
from decimal import Decimal
from calendar import monthrange
from typing import List
from dateutil.relativedelta import relativedelta

from budget_interface import Budget, BudgetsInterface


class BudgetService:
    def __init__(self):
        self.budgets = []

    def query(self, start: datetime, end: datetime) -> Decimal:
        if not self.budgets:
            self.get_budgets_from_db()

        if start > end:
            return Decimal(0)

        month_delta = self._calculate_month_delta(end, start)
        if month_delta == 0:  # same month
            return self.get_budget_within_same_month(end, start)
        else:  # different month
            return self.get_budget_across_different_months(end, month_delta, start)

    def get_budgets_from_db(self) -> None:
        # print("\n\n=============== POKE DB ===============")
        self.budgets = self._get_budgets()

    def get_budget_within_same_month(self, end, start) -> Decimal:
        return self._get_budget_by_partial_month(start, end)

    def get_budget_across_different_months(self, end, month_delta, start) -> Decimal:
        total_budget = 0
        total_budget += self._get_budget_with_start_date(start)
        for i in range(1, month_delta):
            total_budget += self._get_budget_by_full_month(
                start + relativedelta(months=i)
            )
        total_budget += self._get_budget_with_end_date(end)
        return Decimal(total_budget)

    @staticmethod
    def _get_budgets() -> List[Budget]:
        return BudgetsInterface.get_all()

    @staticmethod
    def calculate_budget(days: int, days_of_month: int, month_budget: int) -> float:
        return month_budget / days_of_month * days

    @staticmethod
    def _calculate_month_delta(end, start) -> int:
        return (end.year - start.year) * 12 + (end.month - start.month)

    def _get_budget_with_start_date(self, start: datetime) -> float:
        month_budget = self._get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return self.calculate_budget(days, days_of_month, month_budget)

    def _get_budget_with_end_date(self, end: datetime) -> float:
        month_budget = self._get_month_budget(end)
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return self.calculate_budget(days, days_of_month, month_budget)

    def _get_budget_by_full_month(self, date: datetime) -> int:
        return self._get_month_budget(date)

    def _get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self._get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return Decimal(self.calculate_budget(days, days_of_month, month_budget))

    def _get_month_budget(self, date: datetime) -> int:
        for i in self.budgets:
            if i.year_month == date.strftime("%Y%m"):
                return i.amount

        return 0
