import os
import shutil
import hashlib
import json
from datetime import datetime

LOG_FILE = "operation_log.txt"
UNDO_FILE = "undo_data.json"


class FileOrganizer:

    FILE_CATEGORIES = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
        "Documents": [".pdf", ".docx", ".txt", ".pptx", ".xlsx"],
        "Videos": [".mp4", ".mkv", ".avi", ".mov"],
        "Audio": [".mp3", ".wav"],
        "Archives": [".zip", ".rar", ".7z"]
    }

    def __init__(self):
        self.undo_data = []

    def log_operation(self, message):
        with open(LOG_FILE, "a", encoding="utf-8") as file:
            file.write(
                f"[{datetime.now()}] {message}\n"
            )

    def save_undo(self):
        with open(UNDO_FILE, "w", encoding="utf-8") as file:
            json.dump(self.undo_data, file, indent=4)

    def load_undo(self):
        if os.path.exists(UNDO_FILE):
            with open(UNDO_FILE, "r", encoding="utf-8") as file:
                return json.load(file)
        return []

    def organize_files(self):

        folder = input(
            "Enter Folder Path: "
        ).strip()

        if not os.path.exists(folder):
            print("Folder not found.")
            return

        self.undo_data = []

        for filename in os.listdir(folder):

            file_path = os.path.join(
                folder,
                filename
            )

            if os.path.isdir(file_path):
                continue

            extension = os.path.splitext(
                filename
            )[1].lower()

            category = "Others"

            for folder_name, extensions in self.FILE_CATEGORIES.items():

                if extension in extensions:
                    category = folder_name
                    break

            destination_folder = os.path.join(
                folder,
                category
            )

            os.makedirs(
                destination_folder,
                exist_ok=True
            )

            destination_file = os.path.join(
                destination_folder,
                filename
            )

            shutil.move(
                file_path,
                destination_file
            )

            self.undo_data.append(
                {
                    "source": destination_file,
                    "destination": file_path
                }
            )

            self.log_operation(
                f"Moved {filename} to {category}"
            )

        self.save_undo()

        print("Files Organized Successfully.")

    def calculate_hash(self, file_path):

        md5 = hashlib.md5()

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):
                md5.update(chunk)

        return md5.hexdigest()

    def detect_duplicates(self):

        folder = input(
            "Enter Folder Path: "
        ).strip()

        if not os.path.exists(folder):
            print("Folder not found.")
            return

        hashes = {}

        duplicates = []

        for root, _, files in os.walk(folder):

            for file in files:

                file_path = os.path.join(
                    root,
                    file
                )

                file_hash = self.calculate_hash(
                    file_path
                )

                if file_hash in hashes:

                    duplicates.append(
                        (
                            hashes[file_hash],
                            file_path
                        )
                    )

                else:
                    hashes[file_hash] = file_path

        if duplicates:

            print("\nDuplicate Files Found\n")

            for original, duplicate in duplicates:

                print("Original :", original)
                print("Duplicate:", duplicate)
                print("-" * 50)

        else:
            print("No Duplicate Files Found.")

    def batch_rename(self):

        folder = input(
            "Enter Folder Path: "
        ).strip()

        if not os.path.exists(folder):
            print("Folder not found.")
            return

        prefix = input(
            "Enter Prefix Name: "
        ).strip()

        counter = 1

        self.undo_data = []

        for filename in os.listdir(folder):

            old_path = os.path.join(
                folder,
                filename
            )

            if os.path.isdir(old_path):
                continue

            extension = os.path.splitext(
                filename
            )[1]

            new_name = f"{prefix}_{counter}{extension}"

            new_path = os.path.join(
                folder,
                new_name
            )

            os.rename(
                old_path,
                new_path
            )

            self.undo_data.append(
                {
                    "source": new_path,
                    "destination": old_path
                }
            )

            counter += 1

        self.save_undo()

        self.log_operation(
            "Batch Rename Executed"
        )

        print("Files Renamed Successfully.")

    def undo_last_operation(self):

        operations = self.load_undo()

        if not operations:
            print("Nothing To Undo.")
            return

        for operation in reversed(operations):

            if os.path.exists(
                operation["source"]
            ):
                shutil.move(
                    operation["source"],
                    operation["destination"]
                )

        self.log_operation(
            "Undo Operation Performed"
        )

        with open(
            UNDO_FILE,
            "w",
            encoding="utf-8"
        ) as file:
            json.dump([], file)

        print("Undo Successful.")

    def view_logs(self):

        if not os.path.exists(LOG_FILE):
            print("No Logs Available.")
            return

        print("\n===== OPERATION LOGS =====\n")

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            print(file.read())

    def menu(self):

        while True:

            print("\n========== FILE ORGANIZER ==========")
            print("1. Organize Files")
            print("2. Detect Duplicates")
            print("3. Batch Rename Files")
            print("4. Undo Last Operation")
            print("5. View Logs")
            print("6. Exit")

            choice = input(
                "Enter Choice: "
            )

            if choice == "1":
                self.organize_files()

            elif choice == "2":
                self.detect_duplicates()

            elif choice == "3":
                self.batch_rename()

            elif choice == "4":
                self.undo_last_operation()

            elif choice == "5":
                self.view_logs()

            elif choice == "6":
                print("Goodbye!")
                break

            else:
                print("Invalid Choice")


if __name__ == "__main__":
    app = FileOrganizer()
    app.menu()