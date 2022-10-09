from datetime import datetime, timedelta
from decimal import Decimal
from calendar import monthrange
from dateutil.relativedelta import relativedelta

from budget_interface import BudgetsInterface


class BudgetService:
    def __init__(self):
        self.budgets = []

    def query(self, start: datetime, end: datetime) -> Decimal:
        if start > end:  # illegal date range
            return Decimal(0)

        self.budgets = BudgetsInterface.get_all()
        return (
            self.__get_budget_partial_month(start, end)
            if self.__is_same_month(start, end)
            else self.__get_budget_across_months(start, end)
        )

    @staticmethod
    def __is_same_month(start, end):
        return True if (start.year == end.year and start.month == end.month) else False

    def __get_budget_across_months(self, start: datetime, end: datetime) -> Decimal:
        total_budget = Decimal(0)

        # first month
        last_day_of_month = monthrange(start.year, start.month)[1]
        partial_end = datetime(start.year, start.month, last_day_of_month)
        total_budget += self.__get_budget_partial_month(start, partial_end)

        # middle part
        month_delta = (end.year - start.year) * 12 + (end.month - start.month)
        for i in range(1, month_delta):
            step_month = start + relativedelta(months=i)
            total_budget += self.__get_budget_entire_month(step_month)

        # last month
        partial_start = datetime(end.year, end.month, 1)
        total_budget += self.__get_budget_partial_month(partial_start, end)
        return total_budget

    def __get_budget_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.__get_budget_entire_month(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return Decimal(month_budget / days_of_month * days)

    def __get_budget_entire_month(self, date: datetime) -> Decimal:
        result = [b for b in self.budgets if b.year_month == date.strftime("%Y%m")]
        return Decimal(result[0].amount) if len(result) > 0 else Decimal(0)
