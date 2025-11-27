# STUDENT MANAGER

# Import required libraries
import tkinter as tk  # Tkinter for GUI components
from tkinter import ttk, messagebox, simpledialog  # Extra widgets, dialogs, and message boxes
import os  # For file handling (checking existence, reading/writing)
from PIL import Image, ImageTk  # For loading and displaying images in Tkinter

# DATA FILE SETUP
DATA_FILE = "studentMarks.txt"  # File where student records are stored

# Data utilities
def load_students(path=DATA_FILE):  # Function to load student data from file
    students = []  # Empty list to hold student dictionaries
    if not os.path.exists(path):  # If file doesn’t exist, return empty list
        return students
    with open(path, "r", encoding="utf-8") as f:  # Open file in read mode
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]  # Read lines, strip whitespace, ignore blanks
    if not lines:  # If file is empty, return empty list
        return students
    try:
        int(lines[0])  # Try to read first line as student count
        data_lines = lines[1:]  # Skip first line if it’s a number
    except:
        data_lines = lines  # Otherwise treat all lines as data

    for ln in data_lines:  # Loop through each line of student data
        parts = [p.strip() for p in ln.split(",")]  # Split by commas
        if len(parts) < 6:  # Skip malformed lines
            continue
        code = parts[0]  # Student code
        name = parts[1]  # Student name
        try:
            cw1, cw2, cw3 = int(parts[2]), int(parts[3]), int(parts[4])  # Coursework marks
            exam = int(parts[5])  # Exam mark
        except:
            continue  # Skip if marks aren’t integers
        students.append({  # Add student dictionary to list
            "code": code,
            "name": name,
            "cw": [cw1, cw2, cw3],
            "exam": exam
        })
    return students  # Return list of students


def save_students(students, path=DATA_FILE):  # Function to save student list to file
    with open(path, "w", encoding="utf-8") as f:  # Open file in write mode
        f.write(str(len(students)) + "\n")  # First line = number of students
        for s in students:  # Loop through each student
            line = f"{s['code']},{s['name']},{s['cw'][0]},{s['cw'][1]},{s['cw'][2]},{s['exam']}\n"  # Format as CSV
            f.write(line)  # Write line to file


def coursework_total(s):  # Function to calculate coursework total
    return sum(s["cw"])  # Sum of three coursework marks (out of 60)


def overall_percentage(s):  # Function to calculate overall percentage
    total = coursework_total(s) + s["exam"]  # Coursework + exam marks
    return round((total / 160.0) * 100, 2)  # Convert to percentage (max 160 marks)


def grade_from_percent(p):  # Function to assign grade based on percentage
    if p >= 70: return "A"  # 70% or above = A
    if p >= 60: return "B"  # 60–69% = B
    if p >= 50: return "C"  # 50–59% = C
    if p >= 40: return "D"  # 40–49% = D
    return "F"  # Below 40% = Fail


def format_student_output(s):  # Function to format student info for display
    cw_total = coursework_total(s)  # Coursework total
    exam = s["exam"]  # Exam mark
    percent = overall_percentage(s)  # Overall percentage
    g = grade_from_percent(percent)  # Grade
    lines = [  # Build output lines
        f"Student Name: {s['name']}",
        f"Student Number: {s['code']}",
        f"Total coursework mark (out of 60): {cw_total}",
        f"Exam mark (out of 100): {exam}",
        f"Overall percentage (out of 160): {percent}%",
        f"Grade: {g}"
    ]
    return "\n".join(lines)  # Return formatted string


# GUI
class StudentManagerApp:  # Main application class for managing students
    def __init__(self, root):  # Constructor, runs when app starts
        self.root = root  # Store reference to Tkinter root window
        root.title("Student Manager")  # Set window title
        root.geometry("1000x600")  # Set window size (width x height)

        self.students = load_students()  # Load student data from file
        self._ensure_unique_codes()  # Ensure no duplicate student codes

        # SIDEBAR
        self.sidebar = tk.Frame(root, width=220, bg="#2c3e50")  # Create sidebar frame
        self.sidebar.pack(side="left", fill="y")  # Place sidebar on left, fill vertically

        # LOGO
        try:
            img = Image.open("images/bsu.png")  # Try to open logo image
            img = img.resize((140, 140))  # Resize image to fit sidebar
            self.logo_img = ImageTk.PhotoImage(img)  # Convert to Tkinter image
            logo_label = tk.Label(self.sidebar, image=self.logo_img, bg="#2c3e50")  # Label to hold logo
            logo_label.pack(pady=20)  # Place logo with padding
        except:
            print("Could not load logo image (images/bsu.png).")  # Print error if image missing

        # MAIN PANEL
        self.main = tk.Frame(root, bg="#ecf0f1")  # Create main panel (light background)
        self.main.pack(side="right", fill="both", expand=True)  # Place on right, expand to fill

        # SIDEBAR BUTTONS
        btn_options = [  # List of sidebar buttons with labels and linked functions
            ("View All Records", self.view_all_records),
            ("View Individual", self.view_individual_prompt),
            ("Highest Scorer", self.show_highest),
            ("Lowest Scorer", self.show_lowest),
            ("Sort Records", self.sort_prompt),
            ("Add Student", self.add_student_form),
            ("Delete Student", self.delete_student_prompt),
            ("Update Student", self.update_student_prompt)
        ]
        for i, (label, cmd) in enumerate(btn_options):  # Loop through button list
            b = tk.Button(self.sidebar, text=label, fg="white", bg="#34495e",  # Create button
                          relief="flat", command=cmd, anchor="w")  # Assign function to button
            b.pack(fill="x", padx=10, pady=6)  # Place button in sidebar

        # TITLE
        self.title_label = tk.Label(self.main, text="Student Manager",  # Title label
                                    font=("Segoe UI", 18, "bold"), bg="#ecf0f1")
        self.title_label.pack(pady=10)  # Place at top of main panel

        # SEARCH CONTROLS
        ctrl_frame = tk.Frame(self.main, bg="#ecf0f1")  # Frame for search controls
        ctrl_frame.pack(fill="x", padx=12)  # Place at top, fill horizontally
        tk.Label(ctrl_frame, text="Search (code or name):", bg="#ecf0f1").pack(side="left")  # Label
        self.search_entry = tk.Entry(ctrl_frame)  # Entry box
        self.search_entry.pack(side="left", padx=6)
        tk.Button(ctrl_frame, text="Find", command=self.view_individual_from_search).pack(side="left", padx=6)  # Find button
        tk.Button(ctrl_frame, text="Refresh", command=self.refresh_data).pack(side="left", padx=6)  # Refresh button

                # TEXT OUTPUT AREA
        text_frame = tk.Frame(self.main)  # Frame for text output
        text_frame.pack(fill="both", expand=True, padx=12, pady=12)

        self.text_widget = tk.Text(text_frame, wrap="word", state="normal", font=("Consolas", 11))  # Text widget
        self.text_widget.pack(side="left", fill="both", expand=True)

        self.text_widget.tag_configure("heading", font=("Segoe UI", 12, "bold"))  # Style for headings

        self.scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)  # Scrollbar for text widget
        self.scrollbar.pack(side="right", fill="y")
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)  # Link scrollbar to text widget

        # STATUS BAR
        self.status = tk.Label(self.main, text="", anchor="w", bg="#ecf0f1")  # Status bar at bottom
        self.status.pack(fill="x", padx=12, pady=(0, 10))

        # Show welcome message initially
        self.display_welcome()

    # Helper functions
    def _ensure_unique_codes(self):  # Ensure student codes are unique
        used = set()
        changed = False
        for s in self.students:
            if s['code'] in used:  # Duplicate found
                base = int(s['code']) if s['code'].isdigit() else 1000
                newcode = str(base)
                while newcode in used:  # Increment until unique
                    base += 1
                    newcode = str(base)
                s['code'] = newcode
                changed = True
            used.add(s['code'])
        if changed:
            save_students(self.students)  # Save updated codes

    def refresh_data(self):  # Reload data from file
        self.students = load_students()
        self._ensure_unique_codes()
        self.show_message("Data reloaded from file.")

    def display_welcome(self):  # Show welcome text
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", "Welcome to Student Manager\n\n", "heading")
        self.text_widget.insert("end", "Use the menu on the left to view and manage student records.\n")
        self._display_summary_brief()
        self.text_widget.config(state="disabled")

    def _display_summary_brief(self):  # Show class summary
        n = len(self.students)
        avg = self._class_average()
        self.text_widget.insert("end", f"\nClass size: {n}\nAverage percentage: {avg}%\n")

    def _class_average(self):  # Calculate average percentage
        if not self.students:
            return 0.0
        avg = sum(overall_percentage(s) for s in self.students) / len(self.students)
        return round(avg, 2)

    # Menu actions
    def view_all_records(self):  # Display all student records
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", "ALL STUDENT RECORDS\n\n", "heading")
        for s in self.students:
            self.text_widget.insert("end", format_student_output(s) + "\n" + "-" * 50 + "\n")
        n = len(self.students)
        avg = self._class_average()
        self.text_widget.insert("end", f"\nClass size: {n}\nAverage percentage: {avg}%\n", "heading")
        self.text_widget.config(state="disabled")
        self.status.config(text=f"Displayed all records ({n} students)")

    def view_individual_prompt(self):  # Prompt for student search
        key = simpledialog.askstring("Find student", "Enter student code or name:")
        if key:
            self._view_individual(key.strip())

    def view_individual_from_search(self):  # Search via entry box
        key = self.search_entry.get().strip()
        if not key:
            messagebox.showinfo("Find", "Enter student code or name in search box.")
            return
        self._view_individual(key)

    def _view_individual(self, key):  # Display one student
        found = None
        for s in self.students:
            if s['code'] == key or s['name'].lower() == key.lower() or key.lower() in s['name'].lower():
                found = s
                break
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        if not found:
            self.text_widget.insert("end", f"No student found for '{key}'.\n")
            self.status.config(text="No student found")
        else:
            self.text_widget.insert("end", "STUDENT RECORD\n\n", "heading")
            self.text_widget.insert("end", format_student_output(found) + "\n")
            self.status.config(text=f"Displayed student {found['code']} - {found['name']}")
        self.text_widget.config(state="disabled")

    def show_highest(self):  # Show highest scorer
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        best = max(self.students, key=lambda s: overall_percentage(s))
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", "STUDENT WITH HIGHEST OVERALL PERCENTAGE\n\n", "heading")
        self.text_widget.insert("end", format_student_output(best) + "\n")
        self.text_widget.config(state="disabled")
        self.status.config(text=f"Highest: {best['code']} - {best['name']} ({overall_percentage(best)}%)")

    def show_lowest(self):  # Show lowest scorer
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        worst = min(self.students, key=lambda s: overall_percentage(s))
        self.text_widget.config(state="normal")
        self.text_widget.delete("1.0", "end")
        self.text_widget.insert("end", "STUDENT WITH LOWEST OVERALL PERCENTAGE\n\n", "heading")
        self.text_widget.insert("end", format_student_output(worst) + "\n")
        self.text_widget.config(state="disabled")
        self.status.config(text=f"Lowest: {worst['code']} - {worst['name']} ({overall_percentage(worst)}%)")

    def sort_prompt(self):  # Sort records
        if not self.students:
            messagebox.showinfo("No data", "No students loaded.")
            return
        choice = messagebox.askquestion("Sort", "Sort ascending by overall percentage?\nNo = descending")
        asc = (choice == "yes")
        self.students.sort(key=lambda s: overall_percentage(s), reverse=not asc)
        self.view_all_records()
        self.status.config(text=f"Sorted ({'Ascending' if asc else 'Descending'})")

    def add_student_form(self):  # Open add student dialog
        AddDialog(self.root, self)

    def delete_student_prompt(self):  # Delete student
        key = simpledialog.askstring("Delete", "Enter student code or name:")
        if not key:
            return
        target = None
        for s in self.students:
            if s['code'] == key or s['name'].lower() == key.lower():
                target = s
                break
        if not target:
            messagebox.showinfo("Delete", f"No student found for '{key}'")
            return
        confirm = messagebox.askyesno("Confirm", f"Delete {target['code']} - {target['name']}?")
        if confirm:
            self.students.remove(target)
            save_students(self.students)
            self.view_all_records()
            self.status.config(text=f"Deleted {target['name']}")

    def update_student_prompt(self):  # Update student
        key = simpledialog.askstring("Update", "Enter student code or name:")
        if not key:
            return
        found = None
        for s in self.students:
            if s['code'] == key or s['name'].lower() == key.lower():
                found = s
                break
        if not found:
            messagebox.showinfo("Update", f"No student found for '{key}'")
            return
        UpdateDialog(self.root, self, found)

    def show_message(self, txt):  # Show info popup
        messagebox.showinfo("Info", txt)

# Add Dialog
class AddDialog:  # Dialog window for adding a new student
    def __init__(self, root, app):
        self.app = app  # Reference to main app
        self.top = tk.Toplevel(root)  # Create popup window
        self.top.title("Add Student")  # Window title
        self.top.geometry("420x380")  # Window size
        self.top.transient(root)  # Keep on top of main window
        self.top.grab_set()  # Make dialog modal (block other actions)

        frm = tk.Frame(self.top)  # Frame inside dialog
        frm.pack(padx=12, pady=12, fill="both", expand=True)

        # Input fields
        tk.Label(frm, text="Student Code (1000-9999):").pack(anchor="w")
        self.code_ent = tk.Entry(frm); self.code_ent.pack(fill="x")

        tk.Label(frm, text="Student Name:").pack(anchor="w")
        self.name_ent = tk.Entry(frm); self.name_ent.pack(fill="x")

        tk.Label(frm, text="Coursework 1 (0-20):").pack(anchor="w")
        self.cw1 = tk.Entry(frm); self.cw1.pack(fill="x")

        tk.Label(frm, text="Coursework 2 (0-20):").pack(anchor="w")
        self.cw2 = tk.Entry(frm); self.cw2.pack(fill="x")

        tk.Label(frm, text="Coursework 3 (0-20):").pack(anchor="w")
        self.cw3 = tk.Entry(frm); self.cw3.pack(fill="x")

        tk.Label(frm, text="Exam mark (0-100):").pack(anchor="w")
        self.exam = tk.Entry(frm); self.exam.pack(fill="x")

        # Buttons
        tk.Button(frm, text="Add", command=self.on_add).pack(pady=10)
        tk.Button(frm, text="Cancel", command=self.top.destroy).pack()

    def on_add(self):  # Function called when Add button pressed
        code = self.code_ent.get().strip()
        name = self.name_ent.get().strip()

        try:
            cw1 = int(self.cw1.get())
            cw2 = int(self.cw2.get())
            cw3 = int(self.cw3.get())
            exam = int(self.exam.get())
        except:
            messagebox.showerror("Input error", "Marks must be integers")
            return

        if not code.isdigit() or not (1000 <= int(code) <= 9999):
            messagebox.showerror("Input error", "Code must be 1000–9999")
            return

        if any(not (0 <= m <= 20) for m in (cw1, cw2, cw3)) or not (0 <= exam <= 100):
            messagebox.showerror("Input error", "Marks out of range")
            return

        for s in self.app.students:
            if s['code'] == code:
                messagebox.showerror("Input error", "Code already exists")
                return

        new = {"code": code, "name": name, "cw": [cw1, cw2, cw3], "exam": exam}
        self.app.students.append(new)
        save_students(self.app.students)
        self.app.view_all_records()
        self.app.status.config(text=f"Added {name}")
        self.top.destroy()

# Update Dialog
class UpdateDialog:  # Dialog window for updating student info
    def __init__(self, root, app, student):
        self.app = app
        self.student = student

        self.top = tk.Toplevel(root)  # Popup window
        self.top.title(f"Update {student['code']} - {student['name']}")  # Title with student info
        self.top.geometry("420x420")  # Window size
        self.top.transient(root)
        self.top.grab_set()

        frm = tk.Frame(self.top)
        frm.pack(padx=12, pady=12, fill="both", expand=True)

        # Input fields pre-filled with current values
        tk.Label(frm, text="Student Code:").pack(anchor="w")
        self.code_ent = tk.Entry(frm); self.code_ent.pack(fill="x")
        self.code_ent.insert(0, student['code'])

        tk.Label(frm, text="Student Name:").pack(anchor="w")
        self.name_ent = tk.Entry(frm); self.name_ent.pack(fill="x")
        self.name_ent.insert(0, student['name'])

        tk.Label(frm, text="Coursework 1 (0-20):").pack(anchor="w")
        self.cw1 = tk.Entry(frm); self.cw1.pack(fill="x")
        self.cw1.insert(0, str(student['cw'][0]))

        tk.Label(frm, text="Coursework 2 (0-20):").pack(anchor="w")
        self.cw2 = tk.Entry(frm); self.cw2.pack(fill="x")
        self.cw2.insert(0, str(student['cw'][1]))

        tk.Label(frm, text="Coursework 3 (0-20):").pack(anchor="w")
        self.cw3 = tk.Entry(frm); self.cw3.pack(fill="x")
        self.cw3.insert(0, str(student['cw'][2]))

        tk.Label(frm, text="Exam mark (0-100):").pack(anchor="w")
        self.exam = tk.Entry(frm); self.exam.pack(fill="x")
        self.exam.insert(0, str(student['exam']))

        # Buttons
        tk.Button(frm, text="Save", command=self.on_save).pack(pady=10)
        tk.Button(frm, text="Cancel", command=self.top.destroy).pack()

    def on_save(self):  # Function called when Save button pressed
        code = self.code_ent.get().strip()
        name = self.name_ent.get().strip()

        try:
            cw1 = int(self.cw1.get())
            cw2 = int(self.cw2.get())
            cw3 = int(self.cw3.get())
            exam = int(self.exam.get())
        except:
            messagebox.showerror("Input error", "Marks must be integers")
            return

        if not code.isdigit() or not (1000 <= int(code) <= 9999):
            messagebox.showerror("Input error", "Code must be 1000–9999")
            return

        if any(not (0 <= m <= 20) for m in (cw1, cw2, cw3)) or not (0 <= exam <= 100):
            messagebox.showerror("Input error", "Marks out of range")
            return

        for s in self.app.students:
            if s is not self.student and s['code'] == code:
                messagebox.showerror("Input error", "Another student has this code")
                return

        # Update student info
        self.student['code'] = code
        self.student['name'] = name
        self.student['cw'] = [cw1, cw2, cw3]
        self.student['exam'] = exam

        save_students(self.app.students)
        self.app.view_all_records()
        self.app.status.config(text=f"Updated {name}")
        self.top.destroy()

# Start App
if __name__ == "__main__":  # Run program if file executed directly
    root = tk.Tk()  # Create main Tkinter window
    app = StudentManagerApp(root)  # Create app instance
    root.mainloop()  # Start Tkinter event loop
