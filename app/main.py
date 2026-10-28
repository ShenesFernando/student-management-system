
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re
from datetime import datetime, date
import os
from dotenv import load_dotenv

# ---------------- DATABASE CONNECTION ----------------

# Load environment variables from the project root .env file
load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "student_management")
    )
    


selected_student_id = None


# ---------------- CLEAR INPUT FIELDS ----------------

def clear_fields():
    global selected_student_id
    selected_student_id = None

    for entry in (
        first_name_entry,
        last_name_entry,
        email_entry,
        dob_entry
    ):
        entry.delete(0, tk.END)

    student_table.selection_remove(
        student_table.selection()
    )


# ---------------- VIEW STUDENTS ----------------

def view_students():
    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_id, first_name, last_name,
                   email, date_of_birth
            FROM Students
            ORDER BY student_id
        """)

        rows = cursor.fetchall()

        for item in student_table.get_children():
            student_table.delete(item)

        for row in rows:
            student_table.insert("", tk.END, values=row)

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ---------------- SELECT STUDENT ----------------

def select_student(event=None):
    global selected_student_id

    selected = student_table.selection()

    if not selected:
        return

    values = student_table.item(selected[0], "values")

    selected_student_id = int(values[0])

    first_name_entry.delete(0, tk.END)
    first_name_entry.insert(0, values[1])

    last_name_entry.delete(0, tk.END)
    last_name_entry.insert(0, values[2])

    email_entry.delete(0, tk.END)
    email_entry.insert(0, values[3])

    dob_entry.delete(0, tk.END)
    dob_entry.insert(0, values[4] if values[4] else "")

    form.config(text=f"Edit Student — ID: {selected_student_id}")

# ---------------- INPUT VALIDATION ----------------

def validate_student_inputs():
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    email = email_entry.get().strip()
    dob_text = dob_entry.get().strip()

    if not first_name or not last_name or not email or not dob_text:
        messagebox.showwarning(
            "Validation Error",
            "Please fill in all fields."
        )
        return False

    if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]*", first_name):
        messagebox.showwarning(
            "Validation Error",
            "Please enter a valid first name."
        )
        return False

    if not re.fullmatch(r"[A-Za-z][A-Za-z '\-]*", last_name):
        messagebox.showwarning(
            "Validation Error",
            "Please enter a valid last name."
        )
        return False

    if not re.fullmatch(
        r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}",
        email
    ):
        messagebox.showwarning(
            "Validation Error",
            "Please enter a valid email address."
        )
        return False

    try:
        dob = datetime.strptime(dob_text, "%Y-%m-%d").date()
    except ValueError:
        messagebox.showwarning(
            "Validation Error",
            "Date of Birth must use YYYY-MM-DD format."
        )
        return False

    if dob >= date.today():
        messagebox.showwarning(
            "Validation Error",
            "Date of Birth must be in the past."
        )
        return False

    return True

# ---------------- ADD STUDENT ----------------

def add_student():

    if not validate_student_inputs():
        return
    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    email = email_entry.get().strip()
    dob = dob_entry.get().strip()

    if not all([first_name, last_name, email, dob]):
        messagebox.showwarning(
            "Missing Details",
            "Please fill in all fields."
        )
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO Students
                (first_name, last_name, email, date_of_birth)
            VALUES (%s, %s, %s, %s)
        """, (first_name, last_name, email, dob))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Student added successfully!"
        )

        clear_fields()
        form.config(text="Add New Student")
        view_students()

    except mysql.connector.Error as error:
        if connection is not None:
            connection.rollback()

        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ---------------- UPDATE STUDENT ----------------

def update_student():

    if not validate_student_inputs():
        return
    if selected_student_id is None:
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table first."
        )
        return

    first_name = first_name_entry.get().strip()
    last_name = last_name_entry.get().strip()
    email = email_entry.get().strip()
    dob = dob_entry.get().strip()

    if not all([first_name, last_name, email, dob]):
        messagebox.showwarning(
            "Missing Details",
            "Please fill in all fields."
        )
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE Students
            SET first_name = %s,
                last_name = %s,
                email = %s,
                date_of_birth = %s
            WHERE student_id = %s
        """, (
            first_name,
            last_name,
            email,
            dob,
            selected_student_id
        ))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Student updated successfully!"
        )

        clear_fields()
        form.config(text="Add New Student")
        view_students()

    except mysql.connector.Error as error:
        if connection is not None:
            connection.rollback()

        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ---------------- DELETE STUDENT ----------------

def delete_student():
    if selected_student_id is None:
        messagebox.showwarning(
            "Select Student",
            "Please select a student from the table first."
        )
        return

    confirm = messagebox.askyesno(
        "Confirm Delete",
        f"Are you sure you want to delete student ID "
        f"{selected_student_id}?"
    )

    if not confirm:
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            DELETE FROM Students
            WHERE student_id = %s
        """, (selected_student_id,))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Student deleted successfully!"
        )

        clear_fields()
        form.config(text="Add New Student")
        view_students()

    except mysql.connector.Error as error:
        if connection is not None:
            connection.rollback()

        messagebox.showerror(
            "Delete Error",
            "Could not delete this student.\n\n"
            "The student may have enrollment records.\n"
            "Database message:\n" + str(error)
        )

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()


# ---------------- SEARCH STUDENTS ----------------

def search_students():
    search_text = search_entry.get().strip()

    if not search_text:
        messagebox.showwarning(
            "Search",
            "Please enter a Student ID, first name, last name, or email."
        )
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        if search_text.isdigit():
            cursor.execute("""
                SELECT student_id, first_name, last_name,
                       email, date_of_birth
                FROM Students
                WHERE student_id = %s
                   OR first_name LIKE %s
                   OR last_name LIKE %s
                   OR email LIKE %s
                ORDER BY student_id
            """, (
                int(search_text),
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%"
            ))
        else:
            cursor.execute("""
                SELECT student_id, first_name, last_name,
                       email, date_of_birth
                FROM Students
                WHERE first_name LIKE %s
                   OR last_name LIKE %s
                   OR email LIKE %s
                ORDER BY student_id
            """, (
                f"%{search_text}%",
                f"%{search_text}%",
                f"%{search_text}%"
            ))

        rows = cursor.fetchall()

        for item in student_table.get_children():
            student_table.delete(item)

        for row in rows:
            student_table.insert("", tk.END, values=row)

        clear_fields()
        form.config(text="Add New Student")

        if rows:
            messagebox.showinfo(
                "Search Results",
                f"Found {len(rows)} student(s)."
            )
        else:
            messagebox.showinfo(
                "Search Results",
                "No matching students found."
            )

    except mysql.connector.Error as error:
        messagebox.showerror("Database Error", str(error))

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

# ---------------- MAIN WINDOW ----------------

root = tk.Tk()
root.title("Student Management System")
root.geometry("1000x650")
root.minsize(850, 550)

title = tk.Label(
    root,
    text="Student Management System",
    font=("Arial", 20, "bold")
)
title.pack(pady=12)


# ---------------- STUDENT FORM ----------------

form = tk.LabelFrame(
    root,
    text="Add New Student",
    padx=12,
    pady=10
)
form.pack(fill="x", padx=15, pady=5)

tk.Label(form, text="First Name").grid(
    row=0, column=0, sticky="w"
)
first_name_entry = tk.Entry(form, width=22)
first_name_entry.grid(row=1, column=0, padx=5, pady=5)

tk.Label(form, text="Last Name").grid(
    row=0, column=1, sticky="w"
)
last_name_entry = tk.Entry(form, width=22)
last_name_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(form, text="Email").grid(
    row=0, column=2, sticky="w"
)
email_entry = tk.Entry(form, width=28)
email_entry.grid(row=1, column=2, padx=5, pady=5)

tk.Label(
    form,
    text="Date of Birth (YYYY-MM-DD)"
).grid(row=0, column=3, sticky="w")

dob_entry = tk.Entry(form, width=20)
dob_entry.grid(row=1, column=3, padx=5, pady=5)


# ---------------- ACTION BUTTONS ----------------

button_frame = tk.Frame(form)
button_frame.grid(
    row=2, column=0, columnspan=4, pady=10
)

tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    width=14
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Update Student",
    command=update_student,
    width=14
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Delete Student",
    command=delete_student,
    width=14
).pack(side="left", padx=5)

tk.Button(
    button_frame,
    text="Clear Fields",
    command=clear_fields,
    width=14
).pack(side="left", padx=5)


# ---------------- SEARCH BAR ----------------

search_frame = tk.LabelFrame(
    root,
    text="Search Students",
    padx=10,
    pady=8
)
search_frame.pack(fill="x", padx=15, pady=5)

tk.Label(
    search_frame,
    text="Student ID / Name / Email:"
).pack(side="left", padx=5)

search_entry = tk.Entry(search_frame, width=35)
search_entry.pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Search",
    command=search_students
).pack(side="left", padx=5)

tk.Button(
    search_frame,
    text="Show All",
    command=lambda: (
        search_entry.delete(0, tk.END),
        view_students()
    )
).pack(side="left", padx=5)

search_entry.bind(
    "<Return>",
    lambda event: search_students()
)


# ---------------- STUDENT TABLE ----------------

table_frame = tk.Frame(root)
table_frame.pack(
    fill="both",
    expand=True,
    padx=15,
    pady=10
)

columns = (
    "student_id",
    "first_name",
    "last_name",
    "email",
    "date_of_birth"
)

student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings",
    selectmode="browse"
)

headings = {
    "student_id": "ID",
    "first_name": "First Name",
    "last_name": "Last Name",
    "email": "Email",
    "date_of_birth": "Date of Birth"
}

for column, heading in headings.items():
    student_table.heading(column, text=heading)

student_table.column("student_id", width=50, anchor="center")
student_table.column("first_name", width=130)
student_table.column("last_name", width=130)
student_table.column("email", width=250)
student_table.column("date_of_birth", width=140)

scrollbar = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=student_table.yview
)

student_table.configure(
    yscrollcommand=scrollbar.set
)

student_table.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

student_table.bind(
    "<<TreeviewSelect>>",
    select_student
)


# ---------------- REFRESH BUTTON ----------------

tk.Button(
    root,
    text="Refresh Students",
    command=view_students,
    width=18
).pack(pady=5)


# ---------------- START APPLICATION ----------------

view_students()
root.mainloop()
