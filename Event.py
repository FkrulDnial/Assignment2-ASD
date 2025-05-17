import streamlit as st
import mysql.connector
import datetime
import requests
import re
import csv
import os
import smtplib
from email.message import EmailMessage


# --- Configure page ---
st.set_page_config(
    page_title="Dean’s Day Registration",
    page_icon="🎓",
    layout="centered"
)

# --- Inject CSS for gradient background and styling ---
def local_css():
    st.markdown(
        """
        <style>
        /* Target the entire app background */
        .stApp {
            background: linear-gradient(135deg, #EEAECA, #94BBE9);
            background-size: 400% 400%;
            animation: gradientBG 7s ease infinite;
            color: #000000;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        @keyframes gradientBG {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }

        /* Optional overlay effect */
        .stApp::before {
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: rgba(30, 58, 138, 0.5);
            z-index: -1;
        }

        /* Form container */
        .stForm {
            background-color: rgba(255, 255, 255, 0.9) !important;
            padding: 2rem !important;
            border-radius: 12px !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1) !important;
            max-width: 600px !important;
            margin: 2rem auto !important;
            color: #000000 !important;  /* Make text inside form black for clarity */
        }

        /* General button styles */
        div.stButton > button {
            font-weight: 600 !important;
            padding: 0.6rem 1.2rem !important;
            border-radius: 8px !important;
            border: none !important;
            transition: background-color 0.3s ease !important;
            width: 100% !important;
            max-width: 300px !important;
            margin: 1rem auto !important;
            display: block !important;
        }

        /* Home screen confirm button */
        /* keep your existing blue for "Confirm Attendance" */
        .stButton > button:has-text("Confirm Attendance") {
            background-color: #2563eb !important;
            color: white !important;
        }
        .stButton > button:has-text("Confirm Attendance"):hover {
            background-color: #1e40af !important;
            cursor: pointer !important;
        }

        /* Submit button inside the form */
        form .stButton > button {
            background-color: #22c55e !important;  /* A bright green */
            color: #ffffff !important;  /* White text */
            border: 2px solid #16a34a !important; /* Slightly darker green border */
        }
        form .stButton > button:hover {
            background-color: #16a34a !important;  /* Darker green on hover */
            cursor: pointer !important;
        }
        
        
        /* Header colors */
        h1, h2, h3 {
            color: #000000 !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

# --- Function to submit to local MySQL ---
def submit_to_mysql(data):
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Fakrul0087#",
            database="event_db"
        )
        cursor = conn.cursor()
        sql = """INSERT INTO registrations 
                (full_name, email, phone, matric, faculty, year, attendance, stay, bus, diet, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        cursor.execute(sql, data)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"MySQL Error: {e}")
        return False

# --- Function to submit to Google Sheets ---
def submit_to_gsheets(data):
    url = "https://script.google.com/macros/s/AKfycbzdOzGFFZ8MvUHsbx2aP0bXyrMnaiir3yO189UqS-hVAE1hha9hLd0bnaYsA02VrAPM/exec"
    payload = {
        "full_name": data[0],
        "email": data[1],
        "phone": data[2],
        "matric": data[3],
        "faculty": data[4],
        "year": data[5],
        "attendance": data[6],
        "stay": data[7],
        "bus": data[8],
        "diet": data[9],
        "timestamp": data[10]
    }
    try:
        response = requests.post(url, json=payload)
        return response.json()
    except Exception as e:
        st.error(f"Google Sheets error: {e}")
        return None

# --- Function to submit to CSV ---
def submit_to_csv(data, filename="registrations.csv"):
    file_exists = os.path.isfile(filename)
    try:
        with open(filename, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow([
                    "Full Name", "Email", "Phone", "Matric", "Faculty", "Year",
                    "Attendance", "Stay", "Bus", "Dietary Restrictions", "Timestamp"
                ])
            writer.writerow(data)
        return True
    except Exception as e:
        st.error(f"CSV Error: {e}")
        return False

# --- Validation functions ---
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

def is_valid_phone(phone):
    return phone.isdigit() and len(phone) in [10,11,12]

# --- Home screen ---
def home_screen():
    st.title("🎓 Dean’s List Award Ceremony")

    # Updated event details
    st.markdown("### 📅 Date: 30 May 2025")
    st.markdown("### 🕘 Time: 8:00 PM – 11:00 PM")
    st.markdown("### 📍 Venue: Dewan Serbaguna, UMPSA Pekan")

    # Map link button (shown below venue)
    st.link_button("📍 Open in Google Maps", "https://g.co/kgs/xQmzcL1")

    st.markdown("---")

    st.markdown(
        "You are cordially invited to the **Dean’s Day** Ceremony in honor of academic excellence.\n\n"
        "Please click the button below to confirm your attendance."
    )

    if st.button("✅ Confirm Attendance"):
        st.session_state.page = "registration"


# --- Registration form ---
def registration_form():
    st.title("📝 Confirm Your Attendance – Dean’s Day")
    st.info("Please fill in all required fields accurately.")

    with st.form("registration_form"):
        st.subheader("👤 Personal Information")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number")
        matric = st.text_input("Matric Number")

        st.subheader("🏫 Academic Info")
        faculty = st.selectbox("Faculty", ["FTKEE", "FKOM", "FTKMA", "FTKPM"])
        year = st.selectbox("Year of Study", ["Year 1", "Year 2", "Year 3", "Year 4"])

        st.subheader("🚌 Attendance Details")
        attendance = st.radio("Will you attend?", ["Yes", "No"])
        stay = st.radio("Where do you stay?", ["KK5", "Dhuam", "Others"])

        need_bus = "N/A"
        if stay == "Dhuam":
            need_bus = st.radio("Do you need the university bus?", ["Yes", "No"])

        diet = st.text_input("Any dietary restrictions? (e.g., None, Vegetarian)")

        st.markdown("---")
        submitted = st.form_submit_button("📩 Submit")

        if submitted:
            errors = []

            if not full_name.strip():
                errors.append("Full Name is required.")
            if not email.strip():
                errors.append("Email Address is required.")
            elif not is_valid_email(email.strip()):
                errors.append("Invalid Email Address format.")
            if not phone.strip():
                errors.append("Phone Number is required.")
            elif not is_valid_phone(phone.strip()):
                errors.append("Phone Number must be 10 or 11 digits long and numeric.")
            if not matric.strip():
                errors.append("Matric Number is required.")
            if not faculty:
                errors.append("Please select a Faculty.")
            if not year:
                errors.append("Please select Year of Study.")
            if not attendance:
                errors.append("Please select your attendance option.")
            if not stay:
                errors.append("Please select where you stay.")
            if stay == "Dhuam" and not need_bus:
                errors.append("Please select if you need the university bus.")

            if errors:
                for err in errors:
                    st.error(err)
            else:
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                form_data = (
                    full_name.strip(), email.strip(), phone.strip(), matric.strip(),
                    faculty, year, attendance, stay, need_bus, diet.strip(), timestamp
                )

                mysql_success = submit_to_mysql(form_data)
                gsheets_response = submit_to_gsheets(form_data)
                csv_success = submit_to_csv(form_data)

                if mysql_success:
                    st.success("✅ Your response has been recorded in MySQL.")
                else:
                    st.error("❌ Failed to save your response in MySQL.")

                if gsheets_response and gsheets_response.get("result") == "success":
                    st.success("✅ Your response has been recorded in Google Sheets.")
                else:
                    st.error("❌ Failed to save your response in Google Sheets.")

                if csv_success:
                    st.success("✅ Your response has been saved to a CSV file.")
                else:
                    st.error("❌ Failed to save your response to CSV.")
                email_sent = send_confirmation_email(email.strip(), full_name.strip())
                if email_sent:
                    st.success("📧 A confirmation email has been sent to your inbox.")
                else:
                    st.warning("⚠️ Failed to send confirmation email.")


                st.session_state.submitted_data = {
                    "Full Name": full_name.strip(),
                    "Email": email.strip(),
                    "Phone": phone.strip(),
                    "Matric": matric.strip(),
                    "Faculty": faculty,
                    "Year": year,
                    "Attendance": attendance,
                    "Stay": stay,
                    "Bus": need_bus,
                    "Dietary Restrictions": diet.strip(),
                    "Timestamp": timestamp
                }
                st.session_state.page = "confirm"

    # Back to Home button
    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

# --- Confirmation screen ---
def confirmation_screen():
    st.balloons()  # 🎈 Add this for animation effect

    st.markdown('<div class="confirmation">', unsafe_allow_html=True)
    st.title("🎉 Thank You for Registering!")
    st.success("✅ Your attendance has been confirmed.")

    st.markdown("We look forward to seeing you at:")
    st.markdown("**📅 Date:** 30 May 2025")
    st.markdown("**🕘 Time:** 8:00 PM – 11:00 PM")
    st.markdown("**📍 Venue:** Dewan Serbaguna, UMPSA Pekan")
    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("⬅️ Back to Home"):
        st.session_state.page = "home"

        

def send_confirmation_email(to_email, full_name):
    try:
        msg = EmailMessage()
        msg['Subject'] = "Dean’s Day Attendance Confirmation"
        msg['From'] = "Smartenviroment01@gmail.com"  # Replace with your email
        msg['To'] = to_email
        msg.set_content(
            f"""Hello {full_name},

Thank you for confirming your attendance for the Dean’s Day Ceremony.

📅 Date: 30 May 2025
🕘 Time: 8:00 PM – 11:00 PM
📍 Venue: Dewan Serbaguna, UMPSA Pekan

We look forward to seeing you!

Best regards,
Event Committee"""
        )

        # --- Setup SMTP Server ---
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login("Smartenviroment01@gmail.com", "prid yeww clzn eyte")
            smtp.send_message(msg)

        return True
    except Exception as e:
        st.error(f"Email Error: {e}")
        return False

# Helper function to load the Lottie animation from a URL
def load_lottie_url(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

# --- Main logic ---
def main():
    local_css()  # Apply custom CSS

    if "page" not in st.session_state:
        st.session_state.page = "home"

    if st.session_state.page == "home":
        home_screen()
    elif st.session_state.page == "registration":
        registration_form()
    elif st.session_state.page == "confirm":
        confirmation_screen()
    else:
        st.session_state.page = "home"
        home_screen()

if __name__ == "__main__":
    main()
    
    # Add the floating WhatsApp help button here so it shows on all pages
    st.markdown("""
        <style>
        .float-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: #25D366;  /* WhatsApp green */
            color: white;
            padding: 12px 18px;
            border-radius: 50px;
            font-weight: bold;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.3);
            text-align: center;
            z-index: 9999;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            gap: 8px;
            user-select: none;
        }
        .float-btn:hover {
            background-color: #128C7E;
        }
        </style>
        <a href="https://wa.me/60184088256?text=Hello!%20I%20need%20help%20with%20the%20Dean's%20Day%20registration." target="_blank" class="float-btn" rel="noopener noreferrer">
            📞 WhatsApp Help
        </a>
    """, unsafe_allow_html=True)
    
