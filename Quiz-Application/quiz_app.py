import json
import random
import time
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

QUESTIONS_FILE = os.path.join(BASE_DIR, "questions.json")
LEADERBOARD_FILE = os.path.join(BASE_DIR, "leaderboard.json")

QUESTIONS_PER_QUIZ = 5
TIME_LIMIT = 15

CORRECT_MARKS = 4
NEGATIVE_MARKS = 1


class QuizApplication:

    def __init__(self):
        self.questions = self.load_questions()

    def load_questions(self):
        try:
            with open(QUESTIONS_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
                print(f"Loaded {len(data)} questions")
                return data
        except Exception as e:
            print("Error:", e)
            return []

    def load_leaderboard(self):
        if os.path.exists(LEADERBOARD_FILE):
            try:
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                    return json.load(file)
            except:
                return []
        return []

    def save_leaderboard(self, leaderboard):
        with open(LEADERBOARD_FILE, "w", encoding="utf-8") as file:
            json.dump(leaderboard, file, indent=4)

    def save_score(self, player_name, score):
        leaderboard = self.load_leaderboard()

        leaderboard.append({
            "name": player_name,
            "score": score
        })

        leaderboard.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        self.save_leaderboard(leaderboard)

    def select_category(self):

        categories = sorted(
            list(
                set(
                    question["category"]
                    for question in self.questions
                )
            )
        )

        if not categories:
            print("No categories available.")
            return None

        print("\n========== AVAILABLE CATEGORIES ==========")

        for i, category in enumerate(categories, start=1):
            print(f"{i}. {category}")

        while True:
            try:
                choice = int(input("\nSelect Category: "))

                if 1 <= choice <= len(categories):
                    return categories[choice - 1]

                print(
                    f"Please enter a number between 1 and {len(categories)}."
                )

            except ValueError:
                print("Please enter a valid numeric value.")

    def start_quiz(self):

        if not self.questions:
            print("No questions available.")
            return

        category = self.select_category()

        if category is None:
            return

        category_questions = [
            question
            for question in self.questions
            if question["category"] == category
        ]

        if not category_questions:
            print("No questions found in this category.")
            return

        random.shuffle(category_questions)

        selected_questions = category_questions[
            : min(
                QUESTIONS_PER_QUIZ,
                len(category_questions)
            )
        ]

        print("\n======================================")
        print("QUIZ STARTED")
        print(f"Category : {category}")
        print(f"Time Limit : {TIME_LIMIT} Seconds")
        print(f"Correct Answer : +{CORRECT_MARKS}")
        print(f"Wrong Answer : -{NEGATIVE_MARKS}")
        print("======================================")

        score = 0

        for index, question in enumerate(
            selected_questions,
            start=1
        ):

            print(f"\nQuestion {index}")
            print("-" * 40)
            print(question["question"])

            for option_number, option in enumerate(
                question["options"],
                start=1
            ):
                print(f"{option_number}. {option}")

            start_time = time.time()

            answer = input("\nEnter Option Number: ")

            elapsed_time = time.time() - start_time

            if elapsed_time > TIME_LIMIT:
                print("Time Up!")
                continue

            try:

                option_index = int(answer) - 1

                if option_index < 0 or option_index >= len(question["options"]):
                    print("Invalid Option.")
                    continue

                selected_answer = question["options"][option_index]

                if selected_answer == question["answer"]:
                    print("Correct Answer")
                    score += CORRECT_MARKS
                else:
                    print(f"Wrong Answer")
                    print(f"Correct Answer: {question['answer']}")
                    score -= NEGATIVE_MARKS

            except ValueError:
                print("Invalid Input")

        print("\n======================================")
        print("QUIZ COMPLETED")
        print(f"Final Score: {score}")
        print("======================================")

        player_name = input("Enter Your Name: ").strip()

        if player_name:
            self.save_score(player_name, score)
            print("Score saved successfully.")
        else:
            print("Name cannot be empty. Score not saved.")

    def show_leaderboard(self):

        leaderboard = self.load_leaderboard()

        if not leaderboard:
            print("\nLeaderboard is empty.")
            return

        print("\n========== LEADERBOARD ==========")

        for rank, player in enumerate(
            leaderboard[:10],
            start=1
        ):
            print(
                f"{rank}. {player['name']} - {player['score']} Marks"
            )

    def menu(self):

        while True:

            print("\n========== QUIZ APPLICATION ==========")
            print("1. Start Quiz")
            print("2. View Leaderboard")
            print("3. Exit")

            choice = input("Enter Choice: ").strip()

            if choice == "1":
                self.start_quiz()

            elif choice == "2":
                self.show_leaderboard()

            elif choice == "3":
                print("Thank You For Using Quiz Application")
                break

            else:
                print("Invalid Choice. Please Try Again.")


if __name__ == "__main__":
    app = QuizApplication()
    app.menu()