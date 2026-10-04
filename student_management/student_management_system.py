import json
import os
#from getpass import getpass

DATA_FILE = "students.json"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"


class StudentManagementSystem:
    def __init__(self):
        self.students = self.load_data()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as file:
                    return json.load(file)
            except (json.JSONDecodeError, FileNotFoundError):
                return []
        return []

    def save_data(self):
        with open(DATA_FILE, "w") as file:
            json.dump(self.students, file, indent=4)

    def add_student(self):
        try:
            student_id = input("Enter Student ID: ").strip()

            if any(student["id"] == student_id for student in self.students):
                print("Student ID already exists.")
                return

            name = input("Enter Student Name: ").strip()
            marks = float(input("Enter Marks: "))

            self.students.append({
                "id": student_id,
                "name": name,
                "marks": marks
            })

            self.save_data()
            print("Student added successfully.")

        except ValueError:
            print("Invalid marks. Please enter a valid number.")

    def view_students(self):
        if not self.students:
            print("No student records found.")
            return

        print("\n--- Student Records ---")
        for student in self.students:
            print(
                f"ID: {student['id']} | "
                f"Name: {student['name']} | "
                f"Marks: {student['marks']}"
            )

    def search_student(self):
        keyword = input("Enter Student ID or Name: ").strip().lower()

        found = False

        for student in self.students:
            if (
                student["id"].lower() == keyword
                or student["name"].lower() == keyword
            ):
                print(
                    f"ID: {student['id']} | "
                    f"Name: {student['name']} | "
                    f"Marks: {student['marks']}"
                )
                found = True

        if not found:
            print("Student not found.")

    def update_student(self):
        student_id = input("Enter Student ID to update: ").strip()

        for student in self.students:
            if student["id"] == student_id:
                new_name = input("Enter New Name: ").strip()

                try:
                    new_marks = float(input("Enter New Marks: "))

                    student["name"] = new_name
                    student["marks"] = new_marks

                    self.save_data()
                    print("Student updated successfully.")
                    return

                except ValueError:
                    print("Invalid marks.")
                    return

        print("Student not found.")

    def delete_student(self):
        student_id = input("Enter Student ID to delete: ").strip()

        for student in self.students:
            if student["id"] == student_id:
                self.students.remove(student)
                self.save_data()
                print("Student deleted successfully.")
                return

        print("Student not found.")

    def sort_students(self):
        print("\n1. Sort by Name")
        print("2. Sort by Marks")

        choice = input("Choose option: ").strip()

        if choice == "1":
            sorted_students = sorted(
                self.students,
                key=lambda student: student["name"].lower()
            )

        elif choice == "2":
            sorted_students = sorted(
                self.students,
                key=lambda student: student["marks"],
                reverse=True
            )

        else:
            print("Invalid choice.")
            return

        print("\n--- Sorted Records ---")
        for student in sorted_students:
            print(
                f"ID: {student['id']} | "
                f"Name: {student['name']} | "
                f"Marks: {student['marks']}"
            )

    def generate_reports(self):
        if not self.students:
            print("No student data available.")
            return

        topper = max(self.students, key=lambda student: student["marks"])
        average_marks = sum(
            student["marks"] for student in self.students
        ) / len(self.students)

        print("\n--- Reports ---")
        print(
            f"Topper: {topper['name']} "
            f"(ID: {topper['id']}) - {topper['marks']} Marks"
        )
        print(f"Average Marks: {average_marks:.2f}")

    def menu(self):
        while True:
            print("\n========== STUDENT MANAGEMENT SYSTEM ==========")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Sort Students")
            print("7. Generate Reports")
            print("8. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.add_student()

            elif choice == "2":
                self.view_students()

            elif choice == "3":
                self.search_student()

            elif choice == "4":
                self.update_student()

            elif choice == "5":
                self.delete_student()

            elif choice == "6":
                self.sort_students()

            elif choice == "7":
                self.generate_reports()

            elif choice == "8":
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please try again.")


def admin_login():
    print("========== ADMIN LOGIN ==========")

    username = input("Username: ").strip()
    #password = getpass("Password: ")
    password = input("Password: ")
    

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        print("Login successful.")
        return True

    print("Invalid username or password.")
    return False


def main():
    if admin_login():
        system = StudentManagementSystem()
        system.menu()


if __name__ == "__main__":
    main()