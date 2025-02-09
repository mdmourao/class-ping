# Class Ping (Attendance)

<img src="./static/images/logo.png" alt="Logo" style="width: 150px;" />

This project is designed to manage class attendance. 
It uses an OTP (One-Time Password) system to verify that students are present in class, ensuring that only authorized individuals can mark attendance.

## Project Overview

- **OTP Verification:** The OTP is uniform and displayed simultaneously to all students present in the class.
  
## Stack

- **Django**
- **NinjaAPI** 
- **Bootstrap** 


## How It Works

- **OTP Presentation:** The professor displays the OTP code, that changes every 10 seconds, on the projector screen. 
- **Student Confirmation:** Students mark their attendance by entering the OTP shown, which verifies their presence.
- **Double Confirmation System:** The professor can use a checkbox system to manually call out each student and confirm their attendance in the class.

## Features

- **OTP Verification:** Ensures that only authorized students can mark their attendance.
- **CSV Support:** Professors can export attendance data in CSV format for record-keeping.

