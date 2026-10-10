import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_NAME = "placement.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def setup_database():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                skills TEXT DEFAULT '',
                qualification TEXT DEFAULT ''
            )
        """)


class PlacementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Career & Placement Management System")
        self.root.geometry("950x650")
        self.root.minsize(800, 550)
        self.root.configure(bg="#f3f6fb")

        self.name_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.skills_var = tk.StringVar()
        self.qualification_var = tk.StringVar()
        self.search_var = tk.StringVar()

        self.build_ui()
        self.load_students()

    def build_ui(self):
        header = tk.Frame(self.root, bg="#17365d", padx=22, pady=18)
        header.pack(fill="x")
        tk.Label(
            header,
            text="Student Career & Placement Management System",
            font=("Segoe UI", 18, "bold"),
            fg="white",
            bg="#17365d"
        ).pack(anchor="w")
        tk.Label(
            header,
            text="Manage student profiles and career-readiness details",
            font=("Segoe UI", 10),
            fg="#dce6f1",
            bg="#17365d"
        ).pack(anchor="w", pady=(5, 0))

        form = ttk.LabelFrame(self.root, text="Student Details", padding=14)
        form.pack(fill="x", padx=18, pady=(16, 10))

        fields = [
            ("Full name *", self.name_var),
            ("Email address *", self.email_var),
            ("Skills (comma-separated)", self.skills_var),
            ("Qualification", self.qualification_var),
        ]
        for index, (label_text, variable) in enumerate(fields):
            row, col = divmod(index, 2)
            wrapper = ttk.Frame(form)
            wrapper.grid(row=row, column=col, sticky="ew", padx=8, pady=7)
            ttk.Label(wrapper, text=label_text).pack(anchor="w", pady=(0, 4))
            ttk.Entry(wrapper, textvariable=variable).pack(fill="x")
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        actions = ttk.Frame(self.root)
        actions.pack(fill="x", padx=26, pady=(0, 12))
        ttk.Button(actions, text="Add Student", command=self.add_student).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Clear Form", command=self.clear_form).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Delete Selected", command=self.delete_selected).pack(side="left")

        search_bar = ttk.Frame(self.root)
        search_bar.pack(fill="x", padx=22, pady=(0, 8))
        ttk.Label(search_bar, text="Search name, email, or skill:").pack(side="left", padx=(0, 8))
        search_entry = ttk.Entry(search_bar, textvariable=self.search_var, width=35)
        search_entry.pack(side="left", fill="x", expand=True)
        search_entry.bind("<KeyRelease>", lambda _event: self.load_students())
        ttk.Button(search_bar, text="Show All", command=self.show_all).pack(side="left", padx=(8, 0))

        table_frame = ttk.Frame(self.root, padding=(18, 0, 18, 8))
        table_frame.pack(fill="both", expand=True)
        columns = ("id", "name", "email", "skills", "qualification")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)
        headings = {
            "id": "ID",
            "name": "Student Name",
            "email": "Email",
            "skills": "Skills",
            "qualification": "Qualification",
        }
        widths = {"id": 55, "name": 170, "email": 220, "skills": 220, "qualification": 150}
        for column in columns:
            self.tree.heading(column, text=headings[column])
            self.tree.column(column, width=widths[column], anchor="w")
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var, anchor="w", padding=(20, 7)).pack(fill="x")

    def add_student(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        skills = self.skills_var.get().strip()
        qualification = self.qualification_var.get().strip()

        if not name or not email:
            messagebox.showwarning("Missing details", "Please enter both the student's name and email.")
            return
        if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
            messagebox.showwarning("Invalid email", "Please enter a valid email address.")
            return

        try:
            with connect_db() as conn:
                conn.execute(
                    """INSERT INTO students (name, email, skills, qualification)
                       VALUES (?, ?, ?, ?)""",
                    (name, email, skills, qualification)
                )
        except sqlite3.IntegrityError:
            messagebox.showerror("Duplicate email", "A student with this email already exists.")
            return
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not save the student.\n{error}")
            return

        self.clear_form()
        self.load_students()
        self.status_var.set(f"Added student: {name}")
        messagebox.showinfo("Success", "Student record added successfully.")

    def load_students(self):
        query = self.search_var.get().strip()
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            with connect_db() as conn:
                if query:
                    pattern = f"%{query}%"
                    rows = conn.execute(
                        """SELECT id, name, email, skills, qualification
                           FROM students
                           WHERE name LIKE ? OR email LIKE ? OR skills LIKE ?
                           ORDER BY name COLLATE NOCASE""",
                        (pattern, pattern, pattern)
                    ).fetchall()
                else:
                    rows = conn.execute(
                        """SELECT id, name, email, skills, qualification
                           FROM students ORDER BY name COLLATE NOCASE"""
                    ).fetchall()
            for row in rows:
                self.tree.insert("", "end", values=row)
            self.status_var.set(f"{len(rows)} student record(s) shown")
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not load records.\n{error}")

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No selection", "Please select a student record first.")
            return

        values = self.tree.item(selected[0], "values")
        student_id, student_name = values[0], values[1]
        if not messagebox.askyesno("Confirm deletion", f"Delete the record for {student_name}?"):
            return

        try:
            with connect_db() as conn:
                conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.load_students()
            self.status_var.set(f"Deleted student: {student_name}")
        except sqlite3.Error as error:
            messagebox.showerror("Database error", f"Could not delete the record.\n{error}")

    def clear_form(self):
        self.name_var.set("")
        self.email_var.set("")
        self.skills_var.set("")
        self.qualification_var.set("")

    def show_all(self):
        self.search_var.set("")
        self.load_students()


if __name__ == "__main__":
    setup_database()
    window = tk.Tk()
    app = PlacementApp(window)
    window.mainloop()
