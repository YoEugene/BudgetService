from datetime import datetime
from decimal import Decimal
from calendar import monthrange
from typing import List
from dateutil.relativedelta import relativedelta

from budget_interface import Budget, BudgetsInterface


class BudgetService:
    def __init__(self):
        self.budgets = []

    def get_budgets_from_db(self) -> None:
        # print("\n\n=============== POKE DB ===============")
        self.budgets = self.__get_budgets()

    def query(self, start: datetime, end: datetime) -> Decimal:
        if not self.budgets:  # get data from db if not already done
            self.get_budgets_from_db()

        if start > end:  # deal with illegal input date range
            return Decimal(0)

        month_delta = self.__calculate_month_delta(start, end)
        # within same month
        if month_delta == 0:
            return self.__get_budget_within_same_month(start, end)
        # across different month
        else:
            return self.__get_budget_across_different_months(start, end, month_delta)

    def __get_budget_within_same_month(self, start, end) -> Decimal:
        return self.__get_budget_by_partial_month(start, end)

    def __get_budget_across_different_months(self, start, end, month_delta) -> Decimal:
        total_budget = 0
        total_budget += self.__get_budget_with_start_date(start)
        for i in range(1, month_delta):
            total_budget += self.__get_budget_by_full_month(
                start + relativedelta(months=i)
            )
        total_budget += self.__get_budget_with_end_date(end)
        return Decimal(total_budget)

    @staticmethod
    def __get_budgets() -> List[Budget]:
        return BudgetsInterface.get_all()

    @staticmethod
    def __calculate_budget(days: int, days_of_month: int, month_budget: int) -> float:
        return month_budget / days_of_month * days

    @staticmethod
    def __calculate_month_delta(start, end) -> int:
        return (end.year - start.year) * 12 + (end.month - start.month)

    def __get_budget_with_start_date(self, start: datetime) -> float:
        month_budget = self.__get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return self.__calculate_budget(days, days_of_month, month_budget)

    def __get_budget_with_end_date(self, end: datetime) -> float:
        month_budget = self.__get_month_budget(end)
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return self.__calculate_budget(days, days_of_month, month_budget)

    def __get_budget_by_full_month(self, date: datetime) -> int:
        return self.__get_month_budget(date)

    def __get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.__get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return Decimal(self.__calculate_budget(days, days_of_month, month_budget))

    def __get_month_budget(self, date: datetime) -> int:
        for i in self.budgets:
            if i.year_month == date.strftime("%Y%m"):
                return i.amount
        return 0
