# Student Career & Placement Management System

A desktop application built with Python, Tkinter, and SQLite to maintain student profiles and basic career-readiness details. This is a learning and portfolio project for a BCA student.

## Features

- Add student records with name, email, skills, and qualification
- Save records in a local SQLite database
- View all saved student records in a table
- Search records by name, email, or skills
- Delete a selected student record after confirmation
- Basic required-field and email-format validation
- Prevent duplicate email addresses

## Technologies Used

- **Python 3**
- **Tkinter** — graphical user interface
- **SQLite** — local database (included with standard Python installations)
- **Visual Studio Code** — development environment

## Project Structure

```text
StudentCareerPlacementSystem/
├── main.py
├── README.md
└── placement.db   # Created automatically when the app first runs
```

## Requirements

- Python 3.9 or newer recommended
- Tkinter support (usually included with Python on Windows)
- No third-party Python packages are required

## How to Run

1. Download or clone this repository.
2. Open the project folder in Visual Studio Code.
3. Open the VS Code terminal (**Terminal → New Terminal**).
4. Run:

   ```bash
   python main.py
   ```

   On some Windows installations, use:

   ```bash
   py main.py
   ```

5. The application window will open. Add a student using the form, then search or view records in the table.

The `placement.db` database file is created automatically in the current working directory the first time the app runs.

## How to Use

1. Enter a student's full name and email address.
2. Optionally enter skills separated by commas and the student's qualification.
3. Select **Add Student** to save the record.
4. Type in the search field to filter records by name, email, or skill.
5. Select a row and choose **Delete Selected** to remove a record.
6. Use **Clear Form** to clear the entry fields, or **Show All** to remove the search filter.

## Learning Objectives

- Practice Python functions and event-driven programming
- Build a desktop GUI with Tkinter
- Perform database operations with SQLite
- Use SQL `INSERT`, `SELECT`, and `DELETE` queries
- Validate user input and handle common database errors

## Future Improvements

- Student login and role-based access
- Job and internship application tracking
- Skill-based job recommendations
- Resume and certificate management
- Placement statistics and dashboard reports

These items are planned improvements and are not included in the current version.

## Project Status

**Current version:** Basic student record management with search and delete functionality.

This project is intended for learning and demonstration. Use sample data rather than real personal student information when sharing screenshots or a public repository.
