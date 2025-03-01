<img  height="40px" align="right" src="./static/images/logo.png"/>


# Class Ping (Attendance)

[classping.org](https://classping.org/)

[![DigitalOcean Referral Badge](https://web-platforms.sfo2.cdn.digitaloceanspaces.com/WWW/Badge%201.svg)](https://www.digitalocean.com/?refcode=c073df1ac08a&utm_campaign=Referral_Invite&utm_medium=Referral_Program&utm_source=badge)


This project is designed to manage class attendance. 
It uses an OTP (One-Time Password) system to verify that students are present in class, ensuring that only authorized individuals can mark attendance.

## Demo

Demo video on YouTube: [Video](https://youtu.be/g1B3YId71MA)

  
## Stack

- **Django**
- **NinjaAPI** 
- **Bootstrap** 

## How It Works

- **OTP Display System:** The professor projects a dynamic OTP code that automatically refreshes at regular intervals, ensuring secure attendance verification during class sessions.

<p align="center">
    <img src="./demo/class_demo.png" align="center" alt="Class Demo" width="500"/>
</p>

- **Student Confirmation:** Students mark their attendance by entering the OTP shown, which verifies their presence.

<p align="center">
    <img src="./demo/register_demo.png" align="center" alt="Register Demo" width="500"/>
</p>

- **Double Confirmation System:** The professor can use a checkbox system to manually call out each student and confirm their attendance in the class.

<p align="center">
    <img src="./demo/confirmation_demo.png" align="center" alt="Confirmation Demo" width="500"/>
</p>


## DB Schema

<p align="center">
    <img src="./myapp_models.png" align="center" alt="DB Schema"/>
</p>


## Contact

For questions, please contact:
- Email: martim.mourao@ulusofona.pt