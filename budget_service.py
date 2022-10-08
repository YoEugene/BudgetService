from datetime import datetime, timedelta
from decimal import Decimal
from calendar import monthrange
from dateutil.relativedelta import relativedelta


class Budget:
    def __init__(self, yearMonth, amount):
        self.yearMonth = yearMonth
        self.amount = amount


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

    @staticmethod
    def get_month_delta(start, end):
        return (end.month - start.month) + (end.year - start.year) * 12
        # return relativedelta(end, start).months

    # '20220828' '20221005'
    def query(self, start: datetime, end: datetime) -> Decimal:
        if start > end:
            return 0

        month_delta = (end.month - start.month) + (end.year - start.year) * 12

        total_budget = 0
        if month_delta == 0:
            total_budget = self.get_budget_by_partial_month(start, end)
            return total_budget
        elif month_delta == 1:
            # 0828 0831
            total_budget += self.get_budget_by_month_start(start)

            # 0901 0905
            total_budget += self.get_budget_by_month_end(end)
            return total_budget

        else:
            # 20220828 20220831
            total_budget += self.get_budget_by_month_start(start)

            for i in range(1, month_delta):
                # 20220901 20220930
                year_acc = (start.month + i - 1) // 12
                tmp_month = (start.month + i) % 12 + 1
                tmp_date = datetime(start.year + year_acc, tmp_month, 1)
                # a + relativedelta(months=33)
                total_budget += self.get_budget_by_full_month(tmp_date)

            # 20230601 20231005
            total_budget += self.get_budget_by_month_end(end)
            return total_budget

    def get_budget_by_month_start(self, start: datetime):
        month_budget = self.get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (days_of_month - start.day) + 1
        return month_budget / days_of_month * days

    def get_budget_by_month_end(self, end: datetime):
        month_budget = self.get_month_budget(end)
        days_of_month = monthrange(end.year, end.month)[1]
        days = end.day
        return month_budget / days_of_month * days

    def get_budget_by_full_month(self, date: datetime) -> Decimal:
        return self.get_month_budget(date)

    def get_budget_by_partial_month(self, start: datetime, end: datetime) -> Decimal:
        month_budget = self.get_month_budget(start)
        days_of_month = monthrange(start.year, start.month)[1]
        days = (end - start).days + 1

        return month_budget / days_of_month * days

    def get_month_budget(self, date: datetime) -> int:
        for i in self.budgets:
            if i.yearMonth == date.strftime("%Y%m"):
                return i.amount

        return 0
