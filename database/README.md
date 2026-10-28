# Student Management System Database

A beginner-friendly relational database project developed using MySQL to manage student information, courses, and student enrollments.

## Project Overview

This project demonstrates database design, SQL queries, table relationships, and data management using MySQL.

## Objectives

- Store and manage student information.
- Maintain course details.
- Record student enrollments.
- Establish relationships using primary and foreign keys.
- Practice SQL queries, joins, aggregate functions, and constraints.

## Database Schema

**Database name:** `student_management`

### Tables

**1. Students**
- `student_id` — Primary Key
- `first_name`
- `last_name`
- `email` — Unique
- `date_of_birth`

**2. Courses**
- `course_id` — Primary Key
- `course_name`
- `course_code` — Unique
- `credits`

**3. Enrollments**
- `enrollment_id` — Primary Key
- `student_id` — Foreign Key
- `course_id` — Foreign Key
- `enrollment_date`

### Relationships

- One student can enroll in multiple courses.
- One course can have multiple students.
- The Enrollments table connects Students and Courses.
- Each student can enroll in the same course only once.

## Technologies Used

- MySQL
- MySQL Workbench
- SQL
- Visual Studio Code
- Git and GitHub

## Project Files

| File | Description |
|---|---|
| `schema.sql` | Creates the database tables |
| `sample_data.sql` | Inserts sample student, course, and enrollment records |
| `queries.sql` | Contains SQL practice and reporting queries |
| `ERD.md` | Documents the Entity Relationship Diagram |
| `../docs/` | Contains database diagram files |

## How to Run the Project

1. Install MySQL Server and MySQL Workbench.
2. Open MySQL Workbench and connect to your local server.
3. Open `schema.sql` and execute the script.
4. Open `sample_data.sql` and execute it to insert sample records.
5. Open `queries.sql` and execute the queries to explore the database.

**Note:** Run the scripts in the order shown above. If the database already contains the sample records, avoid running the sample data script repeatedly because duplicate records may be inserted.

## Project Status

Core database schema, sample data, SQL queries, and ERD documentation have been created. Further improvements may be added as part of the learning process.

## Author

Shenes Fernando

GitHub: [@ShenesFernando](https://github.com/ShenesFernando)
