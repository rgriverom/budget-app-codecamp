"""Budget App"""
from typing import List


class Category:
    def __init__(self, name):
        self.category = name
        self.ledger = []

    def __str__(self):
        first_line = self.category.center(30, '*') + "\n"
        next_lines = [
            f'{led["description"][:23]:23}' + f'{led["amount"]:7.2f}' for led in self.ledger
        ]
        next_lines = "\n".join(next_lines) + "\n"
        total = "Total: %.2f" % self.get_balance()
        return first_line + next_lines + total

    def get_balance(self):
        return sum([item["amount"] for item in self.ledger])

    def check_funds(self, amount: float):
        return self.get_balance() >= amount

    def deposit(self, amount: float, description: str = "") -> None:
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount: float, description: str = "") -> bool:
        if not self.check_funds(amount):
            return False
        self.ledger.append({"amount": amount * -1, "description": description})
        return True

    def transfer(self, amount: float, budget: 'Category') -> bool:
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, f"Transfer to {budget.category}")
        budget.deposit(amount, f"Transfer from {self.category}")
        return True


def create_spend_chart(budgets: List[Category]) -> str:
    chart = "Percentage spent by category\n"
    withdraws = [
        -sum([led.get('amount') for led in bud.ledger if led.get('amount') < 0]) for bud in budgets
    ]
    percents = [int((i / sum(withdraws) * 100) // 10 * 10) for i in withdraws]
    print(percents)
    categories = [bud.category.lower().capitalize() for bud in budgets]
    for i in range(100, -10, -10):
        chart += str(i).rjust(3) + "| "
        for percent in percents:
            chart += "o  " if percent >= i else "   "
        chart += "\n"
    chart += ' ' * 4 + '-' * (2 * (len(budgets) + 1) + 2)
    max_len = len(max(categories, key=len))
    categories = [i.ljust(max_len) for i in categories]
    for i in range(max_len):
        chart += '\n     '
        for name in categories:
            chart += name[i] + '  '
    return chart
