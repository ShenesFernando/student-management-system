# Entity Relationship Diagram (ERD)

## Overview

This diagram represents the relationships between the three tables in the Student Management System database.

## Entities

### Students
- `student_id` — Primary Key
- `first_name`
- `last_name`
- `email`
- `date_of_birth`

### Courses
- `course_id` — Primary Key
- `course_name`
- `course_code`
- `credits`

### Enrollments
- `enrollment_id` — Primary Key
- `student_id` — Foreign Key referencing `Students(student_id)`
- `course_id` — Foreign Key referencing `Courses(course_id)`
- `enrollment_date`

## Relationships

- One student can have many enrollments.
- One course can have many enrollments.
- The `Enrollments` table connects students and courses through a many-to-many relationship.

## Diagram File

The graphical ER diagram is available in the `docs/` directory as `StudentManagementSystem.png`.