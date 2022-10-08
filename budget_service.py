from datetime import datetime
from decimal import Decimal
from calendar import monthrange


class Budget:
    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount


class BudgetsInterface:
    budgets = []

    @staticmethod
    def get_all():
        return BudgetsInterface.budgets


class BudgetService:
    @staticmethod
    def get_budgets():
        return BudgetsInterface.get_all()

    @staticmethod
    def get_month_delta(start, end):
        return (end.month - start.month) + (end.year - start.year) * 12

    @staticmethod
    def calculate_budget(days, days_of_month, month_budget):
        return month_budget / days_of_month * days

    def query(self, start: datetime, end: datetime) -> Decimal:
        if start > end:
            return Decimal(0)

        month_delta = (end.month - start.month) + (end.year - start.year) * 12

        total_budget = 0
        if month_delta == 0:
            total_budget = self.get_budget_by_partial_month(start, end)
            return total_budget
        else:
            total_budget += self.get_budget_by_month_start(start)

            for i in range(1, month_delta):
                year_acc = (start.month + i - 1) // 12
                tmp_month = (start.month + i) % 12 + 1
                tmp_date = datetime(start.year + year_acc, tmp_month, 1)
                total_budget += self.get_budget_by_full_month(tmp_date)

            total_budget += self.get_budget_by_month_end(end)
            return Decimal(total_budget)

    def get_budget_by_month_start(self, start: datetime):
        month_budget = self.get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return self.calculate_budget(days, days_of_month, month_budget)

    def get_budget_by_month_end(self, end: datetime):
        month_budget = self.get_month_budget(end)
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return self.calculate_budget(days, days_of_month, month_budget)

    def get_budget_by_full_month(self, date: datetime) -> int:
        return self.get_month_budget(date)

    def get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return self.calculate_budget(days, days_of_month, month_budget)

    def get_month_budget(self, date: datetime) -> int:
        for i in self.get_budgets():
            if i.year_month == date.strftime("%Y%m"):
                return i.amount

        return 0
