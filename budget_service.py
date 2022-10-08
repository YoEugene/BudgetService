from datetime import datetime, timedelta
from decimal import Decimal
from calendar import monthrange
from pandas import df


class Budget:
    def __init__(self, yearMonth, amount):
        self.yearMonth = yearMonth
        self.amount = amount


class BudgetsInterface:
    def __init__(self):
        pass

    def _get_all(self):
        budget = Budget("202210", 3100)
        return [budget]


class BudgetService:
    def __init__(self):
        budget_interface = BudgetsInterface()
        self.budgets = budget_interface._get_all()

    # '20220828' '20221005'
    def query(self, start: datetime, end: datetime) -> Decimal:
        # handel year
        # handle month
        # for

        month_diff = (end.month - start.month) + (end.year - start.year) * 12
        if month_diff == 0:
            return self.get_budget_by_partial_month(start, end)
        elif month_diff == 1:
            # 0828 0831
            self.get_budget_by_month_start(start)

            # 0901 0905
            self.get_budget_by_month_end(end)
        else:
            # 20220828 20220831
            self.get_budget_by_month_start(start)

            for i in range(1, month_diff):
                # 20220901 20220930
                year_acc = (start.month + i - 1) // 12
                tmp_month = (start.month + i) % 12
                tmp_date = datetime(start.year + year_acc, tmp_month, 1)
                self.get_budget_by_full_month(tmp_date)

            # 20230601 20231005
            self.get_budget_by_month_end(end)

    def get_budget_by_month_start(self, start: datetime):
        month_budget = self.get_month_budget(start.month)
        days_of_month = monthrange(start.year, start.month)
        days = (days_of_month - start.days) + 1
        return Decimal(month_budget / days_of_month * days)

    def get_budget_by_month_end(self, end: datetime):
        month_budget = self.get_month_budget(end.month)
        days_of_month = monthrange(end.year, end.month)
        days = end.days
        return Decimal(month_budget / days_of_month * days)

    def get_budget_by_full_month(self, date: datetime) -> Decimal:
        return self.get_month_budget(date)

    def get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.get_month_budget(start.month)
        days_of_month = monthrange(start.year, start.month)
        days = (end - start).days + 1

        return Decimal(month_budget / days_of_month * days)

    def get_month_budget(self, date: datetime) -> int:
        for i in self.budgets:
            if i.yearMonth == date.strftime("%Y%m"):
                return i.amount

        return 0
