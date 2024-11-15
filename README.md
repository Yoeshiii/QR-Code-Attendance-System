# QR Code Attendance System

A simple QR Code Attendance System built using Python and Tkinter for both student and teacher interfaces. Students can mark their attendance by scanning a generated QR code linked to a Google Form, while teachers can manage attendance records, mark students as absent, and export attendance data to an Excel file.

## Features

- **Student Interface**: 
  - Students can enter their ID and name to mark attendance.
  - QR code is generated for students to scan and submit their attendance via a Google Form.
  - ![image](https://github.com/user-attachments/assets/0a4f8892-ef76-4196-9a1d-8f9f364dfa54)

- **Teacher Interface**:

![image](https://github.com/user-attachments/assets/b9c74320-4c0e-43f9-afb7-866cd67e9857)







  - Teachers can manually mark attendance for students or mark them as absent.
  -   ![image](https://github.com/user-attachments/assets/1d1b7c9c-39e4-497b-863d-4f1652c8c917)
  - Teachers can view attendance records and export them to Excel.
  - ![image](https://github.com/user-attachments/assets/e6581496-dc64-46f8-965e-8c923b083938)
  - Access to the teacher interface is password-protected for security.

## Installation

### 1. Clone or download the repository

You can either clone the repository or download the ZIP file of the project.

To clone the repository using Git, run the following command:

```bash
git clone https://github.com/Yoeshiii/QR-Code-Attendance-System.git

## Install required dependencies
Ensure that you have Python installed on your system.
Navigate to the project folder and install the required libraries using pip:
pip install -r requirements.txt

##Run the application
After installing the dependencies, you can run the application by executing the main.py file:
python main.py

##Files
main.py: The main Python application file that handles the QR code generation, student and teacher interfaces, and attendance recording.
student_attendance.xlsx: The Excel file that stores attendance records marked by teacher manually.
student_qr_code.png: The QR code image generated dynamically when the system is run.
Record_from_Qr_cord.xlsx: Ths Excel files stores the student records sumitted through Qr cord.


So when you run the cord this userinterface will pop out whand when you selsct generate QR cord it will display the cord which a students can scan and mark their attandance.

How It Works

Student Interface
The student enters their Student ID and Name when prompted.
The student’s attendance is recorded with a timestamp and saved to an Excel file.
The student scans the QR code, which links to a Google Form, to submit their attendance.
Teacher Interface

The teacher logs in using a password.
The teacher can manually mark attendance for students or mark them as absent.
The teacher can view all attendance records in a text box.
The teacher can export attendance data to an Excel file for record-keeping.
Teacher Login
The teacher accesses the teacher panel by entering the correct password (teacher123) in the login prompt which can be changed asper the teacher wish.

Dependencies

tkinter: For creating the graphical user interface (GUI).
pandas: For handling data manipulation and saving attendance to Excel.
qrcode: For generating QR codes.
openpyxl: For saving and reading Excel files.

To install these dependencies, use the following command:
pip install pandas qrcode openpyxl

Usage

Generate QR Code: Click the "Generate QR Code" button in the main interface to create a new QR code for attendance.
Student Interface: Click the "Student Interface" button to allow students to enter their ID and name to mark attendance.
Teacher Login: Click the "Teacher Login" button to access the teacher interface, where the teacher can mark attendance, view attendance records, and export the data.
