import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime
import base64

st.set_page_config(page_title="NCHS Trivia Night Raffle - After Prom 2024", page_icon="🎟️", layout="wide", menu_items={
    'Get Help': None,
    'Report a bug': None,
    'About': None
})

def validate_email(email):
    # Regular expression pattern for basic email validation
    pattern = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    return re.match(pattern, email)

def validate_field(value):
    if len(value) == 0:
        return False
    else:
        return True

# Function to send email
def send_email(to_email, data, cc_email="nchsjr.board@gmail.com"):
    # SMTP server configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'nchsjr.board@gmail.com'  # Replace with your email address
    smtp_password = st.secrets["MAIL_APP_PWD"]  # Replace with your email password

    # Email content
    message = MIMEMultipart()
    message['From'] = smtp_user
    message['To'] = to_email
    message['Cc'] = cc_email
    message['Subject'] = 'NCHS After Prom 2024 Trivia Night Raffle Registration'

    body = f"Here is the registration data submitted:\n{data}"
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(message)
    server.quit()

# Function to save data to Google Sheets
def save_to_sheet(data, sheet_url):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    # Use Streamlit secrets to load credentials
    creds_dict = {
        'type': st.secrets['gcp_service_account']['type'],
        'project_id': st.secrets['gcp_service_account']['project_id'],
        'private_key_id': st.secrets['gcp_service_account']['private_key_id'],
        'private_key': st.secrets['gcp_service_account']['private_key'],
        'client_email': st.secrets['gcp_service_account']['client_email'],
        'client_id': st.secrets['gcp_service_account']['client_id'],
        'auth_uri': st.secrets['gcp_service_account']['auth_uri'],
        'token_uri': st.secrets['gcp_service_account']['token_uri'],
        'auth_provider_x509_cert_url': st.secrets['gcp_service_account']['auth_provider_x509_cert_url'],
        'client_x509_cert_url': st.secrets['gcp_service_account']['client_x509_cert_url'],
        'universe_domain': st.secrets['gcp_service_account']['universe_domain']
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1

    # Append data to the sheet
    sheet.append_row(data)


st.image("https://lh3.googleusercontent.com/d/1dY782sUfxKrRjjg3pcXLoOdOQ1mbXTTN")
with st.container():
    st.markdown("### Exciting News!")
    st.markdown("Dive into the fun of [NCHS Trivia Night](https://bit.ly/nchstrivia) with our online raffle – your chance to score awesome prizes before the big event safely and securely from the comforts of your couch.")
    st.markdown("Prizes so cool, you'll need a study break just to admire them! Boost your chances of winning awesome prizes, since the odds of winning is huge! Remember, every ticket helps support Afterprom 2024, so it's a win-win!")

st.markdown("### Choose # of tickets and split into buckets")
option = st.radio("How many tickets?", ["5 tickets for $10", "12 tickets for $20", "26 tickets for $40"])
if option == "5 tickets for $10":
    max_tickets = 5
if option == "12 tickets for $20":
    max_tickets = 12
if option == "26 tickets for $40":
    max_tickets = 26

col1, col2, col3 = st.columns(3)

with col1:
    st.header("Basket #1:")
    with st.container(border=True):
        st.subheader(":green[Perfect PROM Night]")
        st.markdown("""
        <ul style="list-style-position: inside; padding-left: 0px;">
        <li> <b>Prom date not included &#128540; </b> </li>
        <li> Biaggi’s $40 Gift Card</li>
        <li>Men’s Warehouse  -Tux /Suit Rental- $259</li>
        </ul>
        """, unsafe_allow_html=True)
        st.markdown("""Total value: **:blue[$299]**""")
        n1 = st.number_input("Number of tickets for Basket #1", min_value=0, max_value=max_tickets, value=0)
        st.image("https://lh3.googleusercontent.com/d/1bM7dQvdTXAdXq86WPMZkCkO82F8gKM8N")
   
   
with col2:
    st.header("Basket #2") 
    with st.container(border=True):
        st.subheader(":red[Go REDBIRDS]")
        st.markdown("""
        <ul style="list-style-position: inside; padding-left: 0px;">
        <li> ISU Men’s Football 4 Tickets </b> </li>
        <li> ISU Men’s Basketball 4 Tickets</li>
        <li> ISU Swag </li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("""Total value: **:blue[$160]**""")
        n2 = st.number_input("Number of tickets for Basket #2", min_value=0, max_value=max_tickets-n1, value=0)
        st.image("https://lh3.googleusercontent.com/d/1u5knlofIt5JRiJJrA8YvNITSc5YQ_oF_")
   
with col3:
    st.header("Basket #3")
    with st.container(border=True):
        st.subheader(":blue[SPORTING SPREE!]")
        st.markdown("""
        <ul style="list-style-position: inside; padding-left: 0px;">
        <li> Unit 5 Season Pass, up to 6 people - Total $100 </b> </li>
        <li> BTT Cardio Tennis Clinic -2 passes</li>
        <li> BTT Daytime Court Rental -2 passes</li>
        <li> BTT Daytime Pickleball Court Rental -2 passes </li>
        </ul>
        """, unsafe_allow_html=True)

        st.markdown("""Total value: **:blue[$288]**""")  
        n3 = st.number_input("Number of tickets for Basket #3", min_value=0, max_value=max_tickets-(n1+n2), value=0)
        st.image("https://lh3.googleusercontent.com/d/1qxMPTw2okKVuVfAFocfOw8w09wtoO8x8")
   


st.subheader("Complete your Purchase")
if n1 + n2 + n3 == max_tickets:
    st.success("Proceed with the purchase!")

else:
    if n1 + n2 + n3 > max_tickets:
        st.error("Number of tickets exceeds limit for selected option")
    else:
        st.info("Split the tickets into three buckets")

def split_correctly(n1, n2, n3):
    if n1 + n2 + n3 == max_tickets:
        return True
    else:
        return False

col1, col2 = st.columns(2)

formSubmitted = False

with st.form(key='ticket_form', clear_on_submit=False):        
    name = st.text_input("Name:")
    email = st.text_input("Email:")
    phone = st.text_input("Phone #:")

    submitted = st.form_submit_button("Submit", disabled=not split_correctly(n1, n2, n3))

    if submitted:
        with st.spinner("Processing..."):
            tickets = n1 + n2 + n3
            if tickets > max_tickets:
                st.error("Number of tickets exceeds limit for selected option")
            else:
                st.header("Payment Options")

                # Payment options
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("#### Venmo")
                    st.markdown("Click [here](https://venmo.com/u/SUDHAKAR-Parsi) or send it to @SUDHAKAR-Parsi")
                    st.image("https://lh3.googleusercontent.com/d/1ornZZwm3irv_gWhQ7WVH6XcVJA5tYMmp", use_column_width=None)
                with col2:
                    st.markdown("#### Zelle")
                    st.markdown("Send your payments to: (404) 800-3312 (Sudhakar Parsi)")
                    st.image("https://lh3.googleusercontent.com/d/1cID276Mt7h0UZ_n7NUoJiOWnbLuiQXcy", use_column_width=None)
                with col3:
                    st.markdown("#### Paypal")
                    st.markdown("Send your payments to:  sudhakar.parsi@gmail.com (Sudhakar Parsi) ")
                    st.image("https://lh3.googleusercontent.com/d/1gRnNFLrR8GrmLtbr23d8QQU11HqMHrjE", use_column_width=None)
                
                            
                if validate_email(email) and validate_field(name) and validate_field(phone):
                    data = f"""
                    Name: {name}
                    EMail: {email}
                    Phone: {phone}
                    Ticket Option: {max_tickets}
                    Bucket-1: {n1}
                    Bucket-2: {n2}
                    Bucket-3: {n3}
                    """
                    data += "\n\nUse any payment methods below, if you have not paid yet. \n\n"
                    data += "Please add your name or email address in the comments section of the payment. \n\n"
                    data += "Using Venmo, pay to  : @SUDHAKAR-Parsi \n\n"
                    data += "Using Zelle, pay to  : sudhakar.parsi@gmail.com (Sudhakar Parsi) \n\n"
                    data += "Using Paypal, pay to  : sudhakar.parsi@gmail.com (Sudhakar Parsi) \n\n"

                    data += "For any questions, please contact nchsjr.board@gmail.com \n"
                    
                    # Send the email
                    send_email(email, data)

                    #Save the sheet to Google Sheets
                    now = datetime.now()
                    date_time = now.strftime("%Y-%m-%d %H:%M:%S")

                    registration_data = [name, email, phone, max_tickets, n1, n2, n3, date_time]
                    save_to_sheet(registration_data, 'https://docs.google.com/spreadsheets/d/1qedeYFAF6TtyWq2GDpyOOGvrkOXo3GqklUIZG3DRdUk/edit?usp=sharing')
                    st.success("Raffle ticket purchase successful! If you have not already paid for the tickets, please proceed with following payment options!")



st.markdown(f"""<div style="text-align: center;">
<img src="https://lh3.googleusercontent.com/d/1u_vpxUp3EtysOCCtGx9tGjkPPbkgMnI2" alt="Image"  style="margin-top: 30px;" >
</div>""", unsafe_allow_html=True)
