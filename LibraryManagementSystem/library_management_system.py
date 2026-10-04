import json
import os
from datetime import datetime, timedelta
import shutil

DATA_FILE = "library_data.json"


class LibraryManagementSystem:
    def __init__(self):
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    return json.load(file)
            except:
                pass

        return {
            "books": [],
            "users": []
        }

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.data, file, indent=4)

    # ---------------- BOOK MANAGEMENT ---------------- #

    def add_book(self):
        book_id = input("Enter Book ID: ")

        for book in self.data["books"]:
            if book["id"] == book_id:
                print("Book ID already exists.")
                return

        title = input("Enter Title: ")
        author = input("Enter Author: ")

        self.data["books"].append({
            "id": book_id,
            "title": title,
            "author": author,
            "issued": False,
            "issued_to": "",
            "issue_date": "",
            "due_date": ""
        })

        self.save_data()
        print("Book Added Successfully.")

    def add_user(self):
        user_id = input("Enter User ID: ")

        for user in self.data["users"]:
            if user["id"] == user_id:
                print("User ID already exists.")
                return

        name = input("Enter User Name: ")

        self.data["users"].append({
            "id": user_id,
            "name": name
        })

        self.save_data()
        print("User Added Successfully.")

    # ---------------- SEARCH ---------------- #

    def search_book(self):
        keyword = input("Enter Title or Author: ").lower()

        found = False

        for book in self.data["books"]:
            if (
                keyword in book["title"].lower()
                or keyword in book["author"].lower()
            ):
                print(
                    f"ID: {book['id']} | "
                    f"Title: {book['title']} | "
                    f"Author: {book['author']}"
                )
                found = True

        if not found:
            print("No book found.")

    # ---------------- ISSUE BOOK ---------------- #

    def issue_book(self):
        book_id = input("Enter Book ID: ")
        user_id = input("Enter User ID: ")

        user_exists = any(
            user["id"] == user_id
            for user in self.data["users"]
        )

        if not user_exists:
            print("User not found.")
            return

        for book in self.data["books"]:
            if book["id"] == book_id:

                if book["issued"]:
                    print("Book already issued.")
                    return

                issue_date = datetime.today()
                due_date = issue_date + timedelta(days=14)

                book["issued"] = True
                book["issued_to"] = user_id
                book["issue_date"] = issue_date.strftime("%Y-%m-%d")
                book["due_date"] = due_date.strftime("%Y-%m-%d")

                self.save_data()

                print("Book Issued Successfully.")
                print("Due Date:", book["due_date"])
                return

        print("Book not found.")

    # ---------------- RETURN BOOK ---------------- #

    def return_book(self):
        book_id = input("Enter Book ID: ")

        for book in self.data["books"]:

            if book["id"] == book_id:

                if not book["issued"]:
                    print("Book is not issued.")
                    return

                due_date = datetime.strptime(
                    book["due_date"],
                    "%Y-%m-%d"
                )

                today = datetime.today()

                fine = 0

                if today > due_date:
                    days_late = (today - due_date).days
                    fine = days_late * 5

                book["issued"] = False
                book["issued_to"] = ""
                book["issue_date"] = ""
                book["due_date"] = ""

                self.save_data()

                print("Book Returned Successfully.")
                print(f"Fine Amount: ₹{fine}")
                return

        print("Book not found.")

    # ---------------- DISPLAY BOOKS ---------------- #

    def available_books(self):
        print("\nAVAILABLE BOOKS")

        found = False

        for book in self.data["books"]:
            if not book["issued"]:
                print(
                    f"{book['id']} | "
                    f"{book['title']} | "
                    f"{book['author']}"
                )
                found = True

        if not found:
            print("No available books.")

    def issued_books(self):
        print("\nISSUED BOOKS")

        found = False

        for book in self.data["books"]:
            if book["issued"]:
                print(
                    f"{book['id']} | "
                    f"{book['title']} | "
                    f"Issued To: {book['issued_to']} | "
                    f"Due: {book['due_date']}"
                )
                found = True

        if not found:
            print("No issued books.")

    # ---------------- BACKUP ---------------- #

    def backup_data(self):
        shutil.copy(DATA_FILE, "backup_library_data.json")
        print("Backup Created Successfully.")

    def restore_data(self):
        if not os.path.exists("backup_library_data.json"):
            print("Backup file not found.")
            return

        shutil.copy(
            "backup_library_data.json",
            DATA_FILE
        )

        self.data = self.load_data()

        print("Data Restored Successfully.")

    # ---------------- MENU ---------------- #

    def menu(self):
        while True:

            print("\n========== LIBRARY MANAGEMENT SYSTEM ==========")
            print("1. Add Book")
            print("2. Add User")
            print("3. Search Book")
            print("4. Issue Book")
            print("5. Return Book")
            print("6. View Available Books")
            print("7. View Issued Books")
            print("8. Backup Data")
            print("9. Restore Data")
            print("10. Exit")

            choice = input("Enter Choice: ")

            if choice == "1":
                self.add_book()

            elif choice == "2":
                self.add_user()

            elif choice == "3":
                self.search_book()

            elif choice == "4":
                self.issue_book()

            elif choice == "5":
                self.return_book()

            elif choice == "6":
                self.available_books()

            elif choice == "7":
                self.issued_books()

            elif choice == "8":
                self.backup_data()

            elif choice == "9":
                self.restore_data()

            elif choice == "10":
                print("Thank You!")
                break

            else:
                print("Invalid Choice.")


if __name__ == "__main__":
    system = LibraryManagementSystem()
    system.menu()