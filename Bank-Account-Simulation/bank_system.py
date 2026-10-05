import json
import os
import csv
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "accounts.json")

TRANSACTION_DIR = os.path.join(BASE_DIR, "transactions")

if not os.path.exists(TRANSACTION_DIR):
    os.makedirs(TRANSACTION_DIR)


class BankSystem:

    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    return json.load(file)
            except:
                return []
        return []

    def save_accounts(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.accounts, file, indent=4)

    def log_transaction(self, account_no, transaction_type, amount):

        file_path = os.path.join(
            TRANSACTION_DIR,
            f"{account_no}_transactions.csv"
        )

        file_exists = os.path.exists(file_path)

        with open(file_path, "a", newline="") as file:

            writer = csv.writer(file)

            if not file_exists:
                writer.writerow(
                    [
                        "Timestamp",
                        "Transaction Type",
                        "Amount"
                    ]
                )

            writer.writerow(
                [
                    datetime.now().strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    transaction_type,
                    amount
                ]
            )

    def create_account(self):

        account_no = f"ACC{1000 + len(self.accounts) + 1}"

        name = input("Enter Account Holder Name: ")

        print("\nAccount Types")
        print("1. Savings")
        print("2. Current")

        choice = input("Select Type: ")

        if choice == "1":
            account_type = "Savings"
        elif choice == "2":
            account_type = "Current"
        else:
            print("Invalid Account Type")
            return

        pin = input("Create 4 Digit PIN: ")

        if len(pin) != 4 or not pin.isdigit():
            print("PIN must be 4 digits.")
            return

        account = {
            "account_no": account_no,
            "name": name,
            "type": account_type,
            "pin": pin,
            "balance": 0
        }

        self.accounts.append(account)
        self.save_accounts()

        print("\nAccount Created Successfully")
        print("Account Number:", account_no)

    def login(self):

        account_no = input("Enter Account Number: ")
        pin = input("Enter PIN: ")

        for account in self.accounts:

            if (
                account["account_no"] == account_no
                and account["pin"] == pin
            ):
                return account

        print("Invalid Credentials")
        return None

    def deposit(self, account):

        try:
            amount = float(input("Enter Amount: "))

            if amount <= 0:
                print("Invalid Amount")
                return

            account["balance"] += amount

            self.save_accounts()

            self.log_transaction(
                account["account_no"],
                "Deposit",
                amount
            )

            print("Amount Deposited Successfully")

        except ValueError:
            print("Invalid Input")

    def withdraw(self, account):

        try:
            amount = float(input("Enter Amount: "))

            if amount > account["balance"]:
                print("Insufficient Balance")
                return

            account["balance"] -= amount

            self.save_accounts()

            self.log_transaction(
                account["account_no"],
                "Withdraw",
                amount
            )

            print("Withdrawal Successful")

        except ValueError:
            print("Invalid Input")

    def transfer_funds(self, sender):

        receiver_account_no = input(
            "Enter Receiver Account Number: "
        )

        receiver = None

        for account in self.accounts:
            if account["account_no"] == receiver_account_no:
                receiver = account
                break

        if receiver is None:
            print("Receiver Not Found")
            return

        try:
            amount = float(
                input("Enter Transfer Amount: ")
            )

            if amount > sender["balance"]:
                print("Insufficient Balance")
                return

            sender["balance"] -= amount
            receiver["balance"] += amount

            self.save_accounts()

            self.log_transaction(
                sender["account_no"],
                "Transfer Sent",
                amount
            )

            self.log_transaction(
                receiver["account_no"],
                "Transfer Received",
                amount
            )

            print("Transfer Successful")

        except ValueError:
            print("Invalid Amount")

    def check_balance(self, account):

        print(
            f"\nCurrent Balance: ₹{account['balance']:.2f}"
        )

    def calculate_interest(self, account):

        if account["type"] != "Savings":
            print(
                "Interest Calculation Available Only For Savings Accounts"
            )
            return

        interest_rate = 4

        interest = (
            account["balance"]
            * interest_rate
            / 100
        )

        print("\nInterest Calculation")
        print(f"Balance : ₹{account['balance']:.2f}")
        print(f"Rate    : {interest_rate}%")
        print(f"Interest: ₹{interest:.2f}")

    def view_transaction_history(self, account):

        file_path = os.path.join(
            TRANSACTION_DIR,
            f"{account['account_no']}_transactions.csv"
        )

        if not os.path.exists(file_path):
            print("No Transactions Found")
            return

        print("\n===== TRANSACTION HISTORY =====\n")

        with open(file_path, "r") as file:
            print(file.read())

    def user_menu(self, account):

        while True:

            print("\n========== BANK MENU ==========")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Transfer Funds")
            print("4. Check Balance")
            print("5. Calculate Interest")
            print("6. Transaction History")
            print("7. Logout")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.deposit(account)

            elif choice == "2":
                self.withdraw(account)

            elif choice == "3":
                self.transfer_funds(account)

            elif choice == "4":
                self.check_balance(account)

            elif choice == "5":
                self.calculate_interest(account)

            elif choice == "6":
                self.view_transaction_history(account)

            elif choice == "7":
                break

            else:
                print("Invalid Choice")

    def main_menu(self):

        while True:

            print("\n========== BANK ACCOUNT SIMULATION ==========")
            print("1. Create Account")
            print("2. Login")
            print("3. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.create_account()

            elif choice == "2":

                account = self.login()

                if account:
                    self.user_menu(account)

            elif choice == "3":
                print("Thank You")
                break

            else:
                print("Invalid Choice")


if __name__ == "__main__":
    system = BankSystem()
    system.main_menu()