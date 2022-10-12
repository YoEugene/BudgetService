from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta


class Budget:
    def __init__(self, yearMonth, amount):
        self.yearMonth = yearMonth
        self.amount = amount

    def get_days(self):
        return monthrange(int(self.yearMonth[:4]), int(self.yearMonth[-2:]))[1]

    def daily_amount(self):
        return self.amount / self.get_days()


class BudgetsInterface:
    def __init__(self):
        pass

    @staticmethod
    def get_all():
        budget = Budget("202210", 3100)
        return [budget]


class BudgetService:
    def __init__(self):
        budget_interface = BudgetsInterface()
        self.budgets = budget_interface.get_all()

    # '20220828' '20221005'
    def query(self, start: datetime, end: datetime) -> Decimal:
        if start > end:
            return 0

        month_delta = (end.month - start.month) + (end.year - start.year) * 12

        if month_delta == 0:
            return self.get_budget_by_partial_month(start, end)

        else:
            total_budget = 0

            current = start
            while current < end.replace(day=1) + relativedelta(months=+1):
                budget = self.get_month_budget(current)
                days_of_month = budget.get_days()
                if budget.yearMonth == start.strftime("%Y%m"):
                    days = (days_of_month - start.day) + 1
                    total_budget += budget.daily_amount() * days
                elif budget.yearMonth == end.strftime("%Y%m"):
                    day = end.day
                    total_budget += budget.amount / days_of_month * day
                else:
                    total_budget += budget.amount
                current = current + relativedelta(months=+1)

            # total_budget += self.get_budget_by_month_end(end)
            return total_budget

    def get_budget_by_month_start(self, start: datetime):
        month_budget = self.get_month_budget(start).amount
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return month_budget / days_of_month * days

    def get_budget_by_month_end(self, end: datetime):
        month_budget = self.get_month_budget(end).amount
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return month_budget / days_of_month * days

    def get_budget_by_full_month(self, date: datetime) -> Decimal:
        return self.get_month_budget(date).amount

    def get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.get_month_budget(start).amount
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return month_budget / days_of_month * days

    def get_month_budget(self, date: datetime) -> Budget:
        for i in self.get_budgets():
            if i.yearMonth == date.strftime("%Y%m"):
                return i
                # return i.amount

        return None

    def get_budgets(self):
        pass
