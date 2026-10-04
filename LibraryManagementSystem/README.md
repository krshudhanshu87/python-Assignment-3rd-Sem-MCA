# Library Management System

A command-line Library Management System developed using Python.

## Features

- Add Books
- Add Users
- Search Books by Title or Author
- Issue Books
- Return Books
- Due Date Tracking
- Automatic Fine Calculation
- View Available Books
- View Issued Books
- Backup Data
- Restore Data
- JSON File Storage

## Project Structure

```text
Library-Management-System/
│
├── library_management_system.py
├── library_data.json
├── backup_library_data.json
├── README.md
└── .gitignore
```

## How to Run

```bash
python library_management_system.py
```

## Fine Policy

- Loan Period: 14 Days
- Fine: ₹5 per day after due date

## Storage

All data is stored in:

```text
library_data.json
```

Backup File:

```text
backup_library_data.json
```

## Technologies Used

- Python 3
- JSON
- Datetime Module
- File Handling

## Author

Your Name