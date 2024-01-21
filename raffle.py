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
    st.markdown("Dive into the fun of NCHS Trivia Night with our online raffle – your chance to score awesome prizes before the big event safely and securely from the comforts of your couch.")
    st.markdown("Prizes so cool, you'll need a study break just to admire them! Boost your chances of winning awesome prizes, since the odds of winning is huge! Remember, every ticket helps support Afterprom 2024, so it's a win-win!")

st.markdown("### Choose # of tickets and split into buckets")
option = st.radio("How many tickets?", ["5 tickets for $10", "12 tickets for $20"])
if option == "5 tickets for $10":
    max_tickets = 5
else:
    max_tickets = 12

col1, col2, col3 = st.columns(3)

with col1:
   st.header("Basket #1")
   st.subheader(":orange[Perfect Prom Night]")
   st.write("""Men's Warehouse rental & Biaggi's $40 gift cards. Great gift idea for the season!!""")
   st.write("""Total value: **:blue[$298]**""")
   n1 = st.number_input("Number of tickets for Basket #1", min_value=0, max_value=max_tickets, value=0)
   st.image("https://m.media-amazon.com/images/I/71EJua1AlML._AC_SX679_.jpg")
   
   
with col2:
   st.header("Basket #2") 
   st.subheader(":orange[Sports and Beyond]")
   st.write("""$100 unit 5 pass, BTT 5 court rentals & BTT Cardio Tennis Classes.""")
   st.write("""Total value: **:blue[$344]**""")
   n2 = st.number_input("Number of tickets for Basket #2", min_value=0, max_value=max_tickets-n1, value=0)
   st.image("https://m.media-amazon.com/images/I/71EJua1AlML._AC_SX679_.jpg")
   
with col3:
   st.header("Basket #3")
   st.subheader(":orange[Go Redbirds!]")
   st.write("""4 Men's Football and 4 Men's Basketball tickets, ISU swag, popcorn, $100 Unit 5 game pass""")
   st.write("""Total value: **:blue[$220]**""")  
   n3 = st.number_input("Number of tickets for Basket #3", min_value=0, max_value=max_tickets-(n1+n2), value=0)
   st.image("https://m.media-amazon.com/images/I/71EJua1AlML._AC_SX679_.jpg")
   


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
                    st.image("https://lh3.googleusercontent.com/d/1c0iAc6b2o48oYFCb8raC0qrn0D47ag6F", use_column_width=None)
                with col2:
                    st.markdown("#### Zelle")
                    st.markdown("Send your payments to: (404) 800-3312 (Sudhakar Parsi)")
                    st.image("https://lh3.googleusercontent.com/d/1ywiw7qvUwiU7yPJPwGaykyZ7IHxbdRhn", use_column_width=None)
                with col3:
                    st.markdown("#### Paypal")
                    st.markdown("Send your payments to:  sudhakar.parsi@gmail.com (Sudhakar Parsi) ")
                    st.image("https://lh3.googleusercontent.com/d/1A8QlPnO7WJx2P_MwKBZz4TAYj5PLhlfm", use_column_width=None)
                
                            
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
                    data += "Using Zelle, pay to  : (404) 800-3312 (Sudhakar Parsi) \n\n"
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
