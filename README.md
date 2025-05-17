**Dean’s Day Registration Web App**
A Streamlit web application to manage event attendance registration for the Dean’s Day Award Ceremony at UMPSA Pekan. The app provides a user-friendly interface for attendees to confirm their attendance, collect participant data, save it to multiple storage options, and send confirmation emails.


**Features**
**Interactive Home Screen**: Event details with a confirmation button and Google Maps link.
**Registration Form**: Collects personal, academic, and attendance information.
**Data Storage**:
- Saves registrations to a local MySQL database.
- Posts data to a Google Sheets via Google Apps Script.
- Saves data locally to a CSV file as backup.
**Input Validation**: Ensures correct email format, phone number, and required fields.
**Email Confirmation**: Sends a personalized confirmation email to attendees.
**Beautiful Styling**: Gradient background, form styling, and responsive buttons.
**Floating WhatsApp Help Button**: Easy access to support for users.

**How It Works**
1. Home Screen
- Displays event details: date, time, venue.
- Provides a link to the venue on Google Maps.
- Users confirm their attendance by clicking a button that leads to the registration form.

2. Registration Form
Users enter:
Full Name, Email, Phone Number, Matric Number
- Faculty and Year of Study
- Attendance status, where they stay, bus requirement if staying at "Dhuam"
- Dietary restrictions

Validates inputs with:
- Email format regex check.
- Phone number length and numeric check.
- Required field checks.

On submission:
- Saves data to MySQL database.
- Sends data to Google Sheets using a Google Apps Script Webhook URL.
- Appends data to a local CSV file.
- Sends a confirmation email to the attendee.

Displays success or error messages accordingly.

3. Confirmation Screen
-Shows a thank you message and event details.
-Offers a button to return to the home screen.
-Animations (balloons) enhance user experience.

4. WhatsApp Help Button
Floating button on all pages linked to a WhatsApp chat for quick support.


**Technologies Used**
**Python** with **Streamlit** for the web app interface.
**MySQL** for relational data storage.
**Google Sheets** for cloud storage via API.
**SMTP** for sending confirmation emails (using Gmail SMTP).
**CSS** embedded for custom UI styling.
**Requests** for HTTP POST to Google Sheets API.
**CSV** file handling for local backups.

