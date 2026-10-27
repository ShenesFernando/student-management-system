
USE student_management;

-- Add sample students
INSERT INTO Students
    (first_name, last_name, email, date_of_birth)
VALUES
    ('Kamal', 'Perera', 'kamal@example.com', '2003-05-14'),
    ('Nimali', 'Silva', 'nimali@example.com', '2002-11-20'),
    ('Sahan', 'Fernando', 'sahan@example.com', '2004-02-08');

-- Add sample courses
INSERT INTO Courses
    (course_name, course_code, credits)
VALUES
    ('Database Design and Development', 'DB101', 15),
    ('Software Development', 'SD102', 15),
    ('Web Development', 'WD103', 15);

-- Add student enrollments
INSERT INTO Enrollments
    (student_id, course_id, enrollment_date)
VALUES
    (1, 1, '2026-10-01'),
    (1, 2, '2026-10-02'),
    (2, 1, '2026-10-03'),
    (3, 3, '2026-10-04');
