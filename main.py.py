import tkinter as tk
from tkinter import messagebox, simpledialog, font
import pandas as pd
import qrcode
import datetime
import os

# Constants
ATTENDANCE_FILE = 'student_attendance.xlsx'
TEACHER_PASSWORD = "teacher123"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScDouYoc4U_kVhOhpt7uqz1fZYXVcqNqGU85hbHqWrq61ZYEQ/viewform?usp=pp_url"

# Create or load attendance file
if not os.path.exists(ATTENDANCE_FILE):
    attendance_data = pd.DataFrame(columns=['Student_ID', 'Name', 'Time', 'Status', 'Form_URL'])
    attendance_data.to_excel(ATTENDANCE_FILE, index=False)
else:
    attendance_data = pd.read_excel(ATTENDANCE_FILE)


def capture_attendance(student_id, name, status="Present"):
    """
    Capture the attendance of a student and save it to an Excel file.
    """
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_row = pd.DataFrame({
        'Student_ID': [student_id],
        'Name': [name],
        'Time': [current_time],
        'Status': [status],
        'Form_URL': [FORM_URL]
    })
    global attendance_data
    attendance_data = pd.concat([attendance_data, new_row], ignore_index=True)
    attendance_data.to_excel(ATTENDANCE_FILE, index=False)
    messagebox.showinfo("Attendance", f"Attendance recorded for {name} at {current_time} as {status}")


def generate_qr_code():
    """
    Generate and display a QR code for the Google Form URL.
    """
    qr_code = qrcode.make(FORM_URL)
    qr_code_path = "student_qr_code.png"
    qr_code.save(qr_code_path)
    os.startfile(qr_code_path)  # Works on Windows systems
    messagebox.showinfo("QR Code", "QR Code generated and opened for scanning.")


def student_interface():
    """
    Collect student details and record attendance.
    """
    student_id = simpledialog.askstring("Student Attendance", "Enter your Student ID:")
    name = simpledialog.askstring("Student Attendance", "Enter your Name:")

    if student_id and name:
        capture_attendance(student_id, name)
    else:
        messagebox.showwarning("Input Error", "Both Student ID and Name are required.")


def teacher_interface():
    """
    The teacher interface to manage attendance records.
    """
    def manual_attendance():
        student_id = simpledialog.askstring("Manual Attendance", "Enter Student ID:")
        name = simpledialog.askstring("Manual Attendance", "Enter Student Name:")
        if student_id and name:
            capture_attendance(student_id, name)
        else:
            messagebox.showwarning("Input Error", "Both Student ID and Name are required.")

    def view_attendance():
        global attendance_data
        attendance_data = pd.read_excel(ATTENDANCE_FILE)
        if not attendance_data.empty:
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, attendance_data.to_string(index=False))
        else:
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, "No attendance records available.")

    def mark_absent():
        student_id = simpledialog.askstring("Mark Absent", "Enter Student ID to mark as absent:")
        if student_id:
            if student_id in attendance_data['Student_ID'].values:
                attendance_data.loc[attendance_data['Student_ID'] == student_id, 'Status'] = 'Absent'
                attendance_data.to_excel(ATTENDANCE_FILE, index=False)
                messagebox.showinfo("Attendance", f"Student {student_id} marked as Absent.")
            else:
                messagebox.showwarning("Student Not Found", f"No attendance found for Student ID: {student_id}")
        else:
            messagebox.showwarning("Input Error", "Please enter Student ID.")

    def export_attendance():
        attendance_data.to_excel(ATTENDANCE_FILE, index=False)
        messagebox.showinfo("Export", "Attendance data exported to 'student_attendance.xlsx'")

    teacher_window = tk.Toplevel()
    teacher_window.title("Teacher Panel")
    teacher_window.geometry("500x400")
    teacher_window.configure(bg="#e6f7ff")

    title_font = font.Font(family="Helvetica", size=14, weight="bold")
    tk.Label(teacher_window, text="Teacher Control Panel", font=title_font, bg="#e6f7ff").pack(pady=10)

    button_frame = tk.Frame(teacher_window, bg="#e6f7ff", padx=20, pady=20)
    button_frame.pack(pady=20)

    manual_button = tk.Button(button_frame, text="Mark Attendance Manually", command=manual_attendance, bg="#FF5722", fg="white", padx=10, pady=5)
    manual_button.grid(row=0, column=0, pady=10, sticky="ew")

    view_button = tk.Button(button_frame, text="View Attendance", command=view_attendance, bg="#2196F3", fg="white", padx=10, pady=5)
    view_button.grid(row=1, column=0, pady=10, sticky="ew")

    absent_button = tk.Button(button_frame, text="Mark Absent", command=mark_absent, bg="#FF5722", fg="white", padx=10, pady=5)
    absent_button.grid(row=2, column=0, pady=10, sticky="ew")

    export_button = tk.Button(button_frame, text="Export Attendance", command=export_attendance, bg="#2196F3", fg="white", padx=10, pady=5)
    export_button.grid(row=3, column=0, pady=10, sticky="ew")

    text_box = tk.Text(teacher_window, width=50, height=10, wrap=tk.WORD)
    text_box.pack(pady=10)


def login():
    """
    Handle teacher login for accessing the teacher interface.
    """
    user_type = simpledialog.askstring("Login", "Enter user type (teacher):").lower()
    password = simpledialog.askstring("Password", "Enter your password:", show="*")

    if user_type == "teacher" and password == TEACHER_PASSWORD:
        teacher_interface()
    else:
        messagebox.showerror("Access Denied", "Invalid password or user type.")


def main_interface():
    """
    Main user interface of the application.
    """
    root = tk.Tk()
    root.title("QR Code Attendance System")
    root.geometry("300x300")
    root.configure(bg="#f9f9f9")

    title_font = font.Font(family="Helvetica", size=16, weight="bold")
    tk.Label(root, text="QR Code Attendance System", font=title_font, bg="#f9f9f9").pack(pady=20)

    qr_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code, bg="#ff9800", fg="white", padx=10, pady=5)
    qr_button.pack(pady=10)

    student_button = tk.Button(root, text="Student Interface", command=student_interface, bg="#4CAF50", fg="white", padx=10, pady=5)
    student_button.pack(pady=10)

    login_button = tk.Button(root, text="Teacher Login", command=login, bg="#2196F3", fg="white", padx=10, pady=5)
    login_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main_interface()
