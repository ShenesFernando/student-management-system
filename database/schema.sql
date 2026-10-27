
-- Student Management System
-- Database schema - Version 1

CREATE DATABASE IF NOT EXISTS student_management;

USE student_management;

CREATE TABLE Students (
    student_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE
);

CREATE TABLE Courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    course_name VARCHAR(100) NOT NULL,
    course_code VARCHAR(20) UNIQUE NOT NULL
);

CREATE TABLE Enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date DATE NOT NULL,

    FOREIGN KEY (student_id)
        REFERENCES Students(student_id),

    FOREIGN KEY (course_id)
        REFERENCES Courses(course_id),

    UNIQUE (student_id, course_id)
);
USE student_management;

SHOW TABLES;

DESCRIBE Students;
DESCRIBE Courses;
DESCRIBE Enrollments;
USE student_management;

SHOW TABLES;
DESCRIBE Students;
DESCRIBE Courses;
DESCRIBE Enrollments;