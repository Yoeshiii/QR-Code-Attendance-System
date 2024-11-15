import tkinter as tk
from tkinter import messagebox, simpledialog, font
import pandas as pd
import qrcode
import datetime
import os

#  This cord will creat file path to save and load attendance in excel
ATTENDANCE_FILE = 'student_attendance.xlsx'

# This checks if attendance file exists; if not it will, create a new one
if not os.path.exists(ATTENDANCE_FILE):
    attendance_data = pd.DataFrame(columns=['Student_ID', 'Name', 'Time', 'Status', 'Form_URL'])
    attendance_data.to_excel(ATTENDANCE_FILE, index=False)
else:
    # Loads the existing attendance data from Excel
    attendance_data = pd.read_excel(ATTENDANCE_FILE)

# This is the password for teacher access
TEACHER_PASSWORD = "teacher123"

# This is the google Form URL where students will submit their attendance after seaning the Qr cord
form_url = "https://docs.google.com/forms/d/e/1FAIpQLScDouYoc4U_kVhOhpt7uqz1fZYXVcqNqGU85hbHqWrq61ZYEQ/viewform?usp=pp_url"

# Function  that capture and save attendance
def capture_attendance(student_id, name, status="Present"):
    # To capture the current time for attendance records
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Creates a new attendance record as a DataFrame row
    new_row = pd.DataFrame({
        'Student_ID': [student_id], 
        'Name': [name], 
        'Time': [current_time], 
        'Status': [status], 
        'Form_URL': [form_url]
    })
    
    # Adds the new record to the existing attendance data
    global attendance_data
    attendance_data = pd.concat([attendance_data, new_row], ignore_index=True)
    
    # Saves updated attendance to the Excel file
    attendance_data.to_excel(ATTENDANCE_FILE, index=False)
    
    #This notify the user that attendance has been recorded
    messagebox.showinfo("Attendance", f"Attendance recorded for {name} at {current_time} as {status}")

# This is the function to generate and display the QR code
def generate_qr_code():
    # This generate a QR code using the Google Form URL
    qr_code = qrcode.make(form_url)
    
    # This cord will save the QR code image locally to the project files.
    qr_code_path = "student_qr_code.png"
    qr_code.save(qr_code_path)
    
    # Opens the QR code image for scanning
    os.startfile(qr_code_path)  # Works on Windows systems
    messagebox.showinfo("QR Code", "QR Code generated and opened for scanning.")

# Student Interface
def student_interface():
    # Prompt the student for their ID and Name
    student_id = simpledialog.askstring("Student Attendance", "Enter your Student ID:")
    name = simpledialog.askstring("Student Attendance", "Enter your Name:")
    
    # Check if both inputs are provided like name and ID
    if student_id and name:
        # Record the attendance
        capture_attendance(student_id, name)
    else:
        # Warn the user if inputs are missing
        messagebox.showwarning("Input Error", "Both Student ID and Name are required.")

# Teacher Interface
def teacher_interface():
    # Function to manually mark attendance
    def manual_attendance():
        student_id = simpledialog.askstring("Manual Attendance", "Enter Student ID:")
        name = simpledialog.askstring("Manual Attendance", "Enter Student Name:")
        
        # This check if inputs are valid
        if student_id and name:
            capture_attendance(student_id, name)
        else:
            messagebox.showwarning("Input Error", "Both Student ID and Name are required.")

    # Function to view attendance
    def view_attendance():
        global attendance_data
        attendance_data = pd.read_excel(ATTENDANCE_FILE)  # Reload attendance data
        
        # Display attendance in the text box of the GUI or userinterface
        if not attendance_data.empty:
            text_box.delete(1.0, tk.END)  # Clear previous content
            text_box.insert(tk.END, attendance_data.to_string(index=False))
        else:
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, "No attendance records available.")

    # Function to mark a student as absent
    def mark_absent():
        student_id = simpledialog.askstring("Mark Absent", "Enter Student ID to mark as absent:")
        if student_id:
            # Update attendance status if the student is found
            if student_id in attendance_data['Student_ID'].values:
                attendance_data.loc[attendance_data['Student_ID'] == student_id, 'Status'] = 'Absent'
                attendance_data.to_excel(ATTENDANCE_FILE, index=False)  # Save updates
                messagebox.showinfo("Attendance", f"Student {student_id} marked as Absent.")
            else:
                # Warn if the student ID is not found
                messagebox.showwarning("Student Not Found", f"No attendance found for Student ID: {student_id}")
        else:
            messagebox.showwarning("Input Error", "Please enter Student ID.")

    # This cord will export attendance to Excel
    def export_attendance():
        attendance_data.to_excel(ATTENDANCE_FILE, index=False)  # Save the data
        messagebox.showinfo("Export", "Attendance data exported to 'student_attendance.xlsx'")

    # Teacher Window
    teacher_window = tk.Toplevel()
    teacher_window.title("Teacher Panel")
    teacher_window.geometry("500x400")
    teacher_window.configure(bg="#e6f7ff")

    # Title font settings
    title_font = font.Font(family="Helvetica", size=14, weight="bold")
    tk.Label(teacher_window, text="Teacher Control Panel", font=title_font, bg="#e6f7ff").pack(pady=10)

    # Button Frame
    button_frame = tk.Frame(teacher_window, bg="#e6f7ff", padx=20, pady=20)
    button_frame.pack(pady=20)

    # Add buttons for teacher functionalities
    manual_button = tk.Button(button_frame, text="Mark Attendance Manually", command=manual_attendance, bg="#FF5722", fg="white", padx=10, pady=5)
    manual_button.grid(row=0, column=0, pady=10, sticky="ew")

    view_button = tk.Button(button_frame, text="View Attendance", command=view_attendance, bg="#2196F3", fg="white", padx=10, pady=5)
    view_button.grid(row=1, column=0, pady=10, sticky="ew")

    absent_button = tk.Button(button_frame, text="Mark Absent", command=mark_absent, bg="#FF5722", fg="white", padx=10, pady=5)
    absent_button.grid(row=2, column=0, pady=10, sticky="ew")

    export_button = tk.Button(button_frame, text="Export Attendance", command=export_attendance, bg="#2196F3", fg="white", padx=10, pady=5)
    export_button.grid(row=3, column=0, pady=10, sticky="ew")

    # Text Box to display attendance
    text_box = tk.Text(teacher_window, width=50, height=10, wrap=tk.WORD)
    text_box.pack(pady=10)

# Password-protected access for teacher only
def login():
    # Ask the teacher for their type and password
    user_type = simpledialog.askstring("Login", "Enter user type (teacher):").lower()
    password = simpledialog.askstring("Password", "Enter your password:", show="*")

    # Checks credentials like the password.
    if user_type == "teacher" and password == TEACHER_PASSWORD:
        teacher_interface()
    else:
        messagebox.showerror("Access Denied", "Invalid password or user type.")

# Main Interface
root = tk.Tk()
root.title("QR Code Attendance System")
root.geometry("300x300")
root.configure(bg="#f9f9f9")

# Title font for main window
title_font = font.Font(family="Helvetica", size=16, weight="bold")
tk.Label(root, text="QR Code Attendance System", font=title_font, bg="#f9f9f9").pack(pady=20)

# Add buttons for different functionalities
qr_button = tk.Button(root, text="Generate QR Code", command=generate_qr_code, bg="#ff9800", fg="white", padx=10, pady=5)
qr_button.pack(pady=10)

student_button = tk.Button(root, text="Student Interface", command=student_interface, bg="#4CAF50", fg="white", padx=10, pady=5)
student_button.pack(pady=10)

login_button = tk.Button(root, text="Teacher Login", command=login, bg="#2196F3", fg="white", padx=10, pady=5)
login_button.pack(pady=10)

root.mainloop() 
