#!/usr/bin/env python
# coding: utf-8
import json
class Transaction:
    def __init__(self, amount, category, description):
        self.amount = amount
        self.category = category
        self.description = description
    def to_dict(self):
        return {
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }
    @staticmethod
    def from_dict(data):
        return Transaction(data['amount'], data['category'], data['description'])
    def __str__(self):
        return f"{self.description}: {self.amount} ({self.category})"
class Budget:
    def __init__(self, monthly_limit):
        self.monthly_limit = monthly_limit
        self.transactions = []
    def add_transaction(self, transaction):
        if self.get_total_spent() + transaction.amount > self.monthly_limit:
            print("Transaction exceeds monthly budget limit.")
        else:
            self.transactions.append(transaction)
            print(f"Transaction added: {transaction}")
    def remove_transaction(self, index):
        try:
            removed = self.transactions.pop(index)
            print(f"Transaction removed: {removed}")
        except IndexError:
            print("Invalid transaction index.")
    def add_funds(self, amount):
        if amount > 0:
            self.monthly_limit += amount
            print(f"Funds added: {amount}. New budget limit: {self.monthly_limit}")
        else:
            print("Amount to add must be positive.")
    def get_total_spent(self):
        return sum(transaction.amount for transaction in self.transactions)
    def get_balance(self):
        return self.monthly_limit - self.get_total_spent()
    def get_summary(self):
        summary = {
            "total_spent": self.get_total_spent(),
            "remaining_budget": self.get_balance(),
            "transactions": self.transactions
        }
        return summary
    def save_to_file(self, filename):
        data = {
            "monthly_limit": self.monthly_limit,
            "transactions": [transaction.to_dict() for transaction in self.transactions]
        }
        with open(filename, 'w') as f:
            json.dump(data, f)
        print(f"Data saved to {filename}")
    @staticmethod
    def load_from_file(filename):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
                budget = Budget(data["monthly_limit"])
                budget.transactions = [Transaction.from_dict(t) for t in data["transactions"]]
                return budget
        except FileNotFoundError:
            print("File not found. Starting with a new budget.")
            return None
def main():
    filename = "budget_data.json"
    # Загружаем существующий бюджет из файла, если он есть
    monthly_budget = Budget.load_from_file(filename)
    # Если бюджета нет, создаем новый
    if monthly_budget is None:
        while True:
            try:
                monthly_limit = float(input("Enter your monthly budget limit: "))
                if monthly_limit <= 0:
                    raise ValueError("Budget limit must be positive.")
                monthly_budget = Budget(monthly_limit)
                break
            except ValueError as e:
                print(f"Invalid input: {e}. Please enter a valid number.")
    while True:
        action = input("Would you like to (1) add a transaction, (2) remove a transaction, (3) add funds, (4) save data, or (5) exit? (Enter 1, 2, 3, 4, or 5): ").strip()
        if action == '1':
            try:
                amount = float(input("Enter transaction amount: "))
                if amount <= 0:
                    raise ValueError("Amount must be positive.")
                category = input("Enter transaction category: ")
                description = input("Enter transaction description: ")
                transaction = Transaction(amount, category, description)
                monthly_budget.add_transaction(transaction)
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
        elif action == '2':
            if not monthly_budget.transactions:
                print("No transactions to remove.")
                continue
            print("Current transactions:")
            for idx, transaction in enumerate(monthly_budget.transactions):
                print(f"{idx}: {transaction}")
            try:
                index_to_remove = int(input("Enter the index of the transaction to remove: "))
                monthly_budget.remove_transaction(index_to_remove)
            except ValueError:
                print("Invalid input. Please enter a valid index.")
        elif action == '3':
            try:
                funds_to_add = float(input("Enter amount to add to the budget: "))
                monthly_budget.add_funds(funds_to_add)
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
        elif action == '4':
            monthly_budget.save_to_file(filename)
        elif action == '5':
            break
        else:
            print("Invalid input. Please enter 1, 2, 3, 4, or 5.")
    # Получаем сводку о бюджете перед выходом
    summary = monthly_budget.get_summary()
    print("--- Budget Summary ---")
    print(f"Total Spent: {summary['total_spent']}")
    print(f"Remaining Budget: {summary['remaining_budget']}")
    print("Transactions:")
    for transaction in summary['transactions']:
        print(transaction)
if __name__ == "__main__":
    main()
