# CBSE Class 12 Formula Search Tool

A beginner Python project that fetches CBSE Class 12 Physics, Chemistry, and Math formulas from a MySQL database. Search by variable name or formula name to quickly find what you need.

Made as a group project by Khadijah Waseem Pandit and Bhanu Akshaya, 12th grade.

## Features

- Search formulas by variable name or formula name
- Covers Physics, Chemistry, and Math (CBSE Class 12 syllabus)
- Simple GUI built with CustomTkinter

## Built With

- Python
- MySQL (via `mysql-connector-python`)
- CustomTkinter (GUI)
- Pillow (image handling)

## Setup

1. Clone this repository
   ```
   git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   ```

2. Install dependencies
   ```
   pip install customtkinter mysql-connector-python mysqlclient pillow python-dotenv
   ```

3. Create a `.env` file in the project root with your own MySQL credentials:
   ```
   DB_HOST=localhost
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=12th_cs_project
   ```

4. Set up the `12th_cs_project` MySQL database with the required tables (formulas, variables, etc.)

5. Run the script
   ```
   python friday_05.py
   ```

## Notes

This was one of our first projects learning Python and databases together: a work in progress, but a fun one!
