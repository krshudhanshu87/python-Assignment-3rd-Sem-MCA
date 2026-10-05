# Quiz Application

A Python Command Line Quiz Application with category selection, timer, negative marking, random question generation, and leaderboard support.

## Features

- Random Question Selection
- Category-Based Quiz
- Timer-Based Questions
- Negative Marking
- Leaderboard System
- JSON File Storage
- Fully CUI Based

## Project Structure

```text
Quiz-Application/
│
├── quiz_app.py
├── questions.json
├── leaderboard.json
├── README.md
└── .gitignore
```

## Marking Scheme

| Action | Marks |
|----------|---------|
| Correct Answer | +4 |
| Wrong Answer | -1 |
| Unattempted | 0 |

## Time Limit

- 15 seconds per question

## Run Project

```bash
python quiz_app.py
```

## Files

### questions.json

Stores all quiz questions.

### leaderboard.json

Stores player scores.

## Technologies Used

- Python 3
- JSON
- Random Module
- Time Module

## Author

Shudhanshu Kumar 