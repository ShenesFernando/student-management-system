
USE student_management;

SELECT
    Students.student_id,
    Students.first_name,
    Students.last_name,
    Courses.course_name,
    Courses.course_code,
    Enrollments.enrollment_date
FROM Enrollments
INNER JOIN Students
    ON Enrollments.student_id = Students.student_id
INNER JOIN Courses
    ON Enrollments.course_id = Courses.course_id
ORDER BY Students.student_id;
