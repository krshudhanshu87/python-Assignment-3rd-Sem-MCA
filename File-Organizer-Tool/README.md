# File Organizer Tool

A Python command-line utility for organizing files automatically.

## Features

- Automatic File Categorization
- Duplicate File Detection
- Batch File Renaming
- Operation Logging
- Undo Last Operation
- File Hashing using MD5
- Exception Handling
- JSON-based Undo Tracking

## Project Structure

```text
File-Organizer-Tool/
│
├── file_organizer.py
├── operation_log.txt
├── undo_data.json
├── README.md
└── .gitignore
```

## Supported Categories

- Images
- Documents
- Videos
- Audio
- Archives
- Others

## Run

```bash
python file_organizer.py
```

## Example Features

### Organize Files

Before:

```text
Downloads/
├── photo.jpg
├── notes.pdf
├── movie.mp4
```

After:

```text
Downloads/
├── Images/
│   └── photo.jpg
├── Documents/
│   └── notes.pdf
└── Videos/
    └── movie.mp4
```

### Duplicate Detection

Identifies files with identical content using MD5 hashing.

### Undo Operation

Restores files to their previous locations after organizing or renaming.

## Author

Your Name