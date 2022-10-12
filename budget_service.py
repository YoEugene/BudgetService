from calendar import monthrange
from datetime import datetime
from decimal import Decimal

from dateutil.relativedelta import relativedelta


class Budget:
    def __init__(self, year_month, amount):
        self.year_month = year_month
        self.amount = amount

    def get_days(self):
        return monthrange(int(self.year_month[:4]), int(self.year_month[-2:]))[1]

    def daily_amount(self):
        return self.amount / self.get_days()

    def get_last_day(self):
        first_day = datetime.strptime(self.year_month, "%Y%m").date()
        return datetime(first_day.year, first_day.month, self.get_days())

    def get_first_day(self):
        return datetime.strptime(self.year_month, "%Y%m")


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
                if budget.year_month == start.strftime("%Y%m"):
                    overlapping_days = (budget.get_last_day() - start).days + 1
                    # days = (budget.get_days() - start.day) + 1
                elif budget.year_month == end.strftime("%Y%m"):
                    overlapping_days = (end - budget.get_first_day()).days + 1
                    # days = end.day
                else:
                    overlapping_days = budget.get_days()
                    # days = budget.get_days()
                total_budget += budget.daily_amount() * overlapping_days
                current = current + relativedelta(months=+1)

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
            if i.year_month == date.strftime("%Y%m"):
                return i
                # return i.amount

        return None

    def get_budgets(self):
        pass
