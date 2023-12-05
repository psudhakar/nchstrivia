import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


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
        'client_x509_cert_url': st.secrets['gcp_service_account']['client_x509_cert_url']
    }
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1

    # Append data to the sheet
    sheet.append_row(data)

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
    message['Subject'] = 'NCHS After Prom 2023 Trivia Night Registration'

    body = f"Here is the registration data submitted:\n\n{data}"
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(message)
    server.quit()

# Hide hamburger menu and footer
st.set_page_config(page_title="Trivia Night by NCHS After Prom Team", layout="wide", menu_items={
    'Get Help': None,
    'Report a bug': None,
    'About': None
})

st.markdown("""
    <style>
    .main {
       font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; align: center;
    }
    h1 {
        color: #ff6347;
        text-align: center;
    }
    
    h5 {
        color: white;
        text-align: center;
    }
    .font {
        font-size:16px;
        font-weight: 400;
    }
    .table-style {
        margin-left: auto; 
        margin-right: auto;
    }
    </style>
    """, unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,8,1])
with col2:
    st.markdown("# Trivia Night 2024 ")
    st.markdown("##### Organized by NCHS After Prom Parents Committee 2024")
    st.markdown("##### Sweat the Questions, Sweeten the Charity Pot: Trivia Night for a Good Cause!")

# Streamlit app layout
#st.set_page_config(page_title='Trivia Night Registration', layout='centered')
logo_url = "https://github.com/psudhakar/nchstrivia/blob/main/trivia3.JPG?raw=true"
#logo_url = "https://drive.google.com/uc?id=1SfAQ50kW6gybO-Pqcs6mFWQ2DiLY0mcH"

# Centering the logo at the top of the screen
col1, col2 = st.columns([1,2])
with col1:
    st.image(logo_url,use_column_width=True)
with col2:
    # Replicate the text and formatting from the screenshot


    st.markdown("""
        ### Looking for a fun night out for a good cause?
        Join us for an unforgettable evening of brain-bending trivia and feel-good fun at our Trivia Night Fundraiser 2024 benefiting a safer After prom. Get ready for an epic trivia throwdown masterminded by Jr. Classboard's most imaginative parents and hosted by the legendary Trivia City!
    """)

    st.markdown("""
       **Here's how you can play a part:**
        1.	Gather your cleverest crew and register your team below!
            Squad Discount: Only $100 for a table of 6, otherwise $20 per individual
        2.	Flying solo, no problem! We are Trivia matchmakers, ready to pair you with your trivia soulmates!
        3.	Fuel your brains with delicious snacks and drinks (available for purchase)!
        4.	Put your heads together to conquer tricky questions and earn bragging rights!
        5.	Most importantly, support a fantastic cause: creating a safe and memorable Afterprom experience for our NCHS students!
                
    """, unsafe_allow_html=True)

    st.markdown("""
        **Registration:**
        Reserve your table by filling the form below. Payments can be made by check, or using any payment methods below:
    """, unsafe_allow_html=True)
    venmourl = "https://venmo.com/u/Jayshri-Patel-5"
    recipient_id = 'Jayshri-Patel-5'
    cash_app_link = f'https://cash.app/$${recipient_id}'

    # Data for the table
    data = {
        "Payment Method": ["Venmo", "Zelle/Paypal", "Cash App", "Check"],
        "Instructions": [
            f"Click <a href={venmourl}> here </a>, or send it to Venmo id: Jayshri-Patel-5",
            "Send your payments to: sudhakar.parsi@gmail.com",
            f"Click <a href={cash_app_link}> here </a>  or send it to Cash id: $SudhakarParsi",
            "Make checks payable to 'NCHS After Prom' and mail to 5018 Londonderry Road, Bloomington, IL - 61705"
        ]
    }

    # Create DataFrame
    df = pd.DataFrame(data)

    # Adjust the DataFrame index to start from 1
    df.index += 1

    # Convert DataFrame to HTML, including the index
    html_table = df.to_html(escape=False, justify="center")

    # Display the table in Streamlit with clickable links and index starting from 1
    st.markdown(html_table, unsafe_allow_html=True)

    #st.markdown("To pay with Venmo, click [here](%s), or send it to Venmo id: Jayshri-Patel-5" % venmourl)
    #st.markdown("For Zelle or Paypal, send your payments to: sudhakar.parsi@gmail.com")
    #st.markdown(f'To pay with Cash App, click [here]({cash_app_link}) or send it to Cash id: $SudhakarParsi')
    #st.markdown("Make checks payable to 'NCHS After Prom' and mail to 5018 Londonderry Road, Bloomington, IL - 61705")

    # Form for registration
    with st.form(key='registration_form'):
        st.markdown("#### Team Registration - NCHS After Prom 2024 Trivia Night")
        team_contact = st.text_input("Team Contact:")
        team_name = st.text_input("Team Name:")
        team_contact_email = st.text_input("Email address for Team Contact:")
        team_contact_phone = st.text_input("Phone number for Team Contact:")
        
        # Submit button
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        # Prepare the data to be sent via email
        data = f"""
        Team Contact: {team_contact}
        Team Name: {team_name}
        Team Contact Email: {team_contact_email}
        Team Contact Phone: {team_contact_phone}
        """
        data += "Use any payment methods below. Please add your name or email address in the comments section of the payment. \n"
        data += "Using Venmo, pay to  : Jayshri-Patel-5 \n"
        data += "Using Zelle/Paypal, pay to  : sudhakar.parsi@gmail.com \n"
        data += "Using Cash, pay to  : $SudhakarParsi \n\n"
        data += "Once the payment is made, you will receive an email with Krispy Kreme gift voucher in next 24-28 hours. \n"
        data += "For any questions, please contact nchsjr.board@gmail.com or call (404)800-3312] \n"
        data += "Make checks payable to 'NCHS After Prom' and mail to 5018 Londonderry Road, Bloomington, IL - 61705"


        
        # Send the email
        send_email(team_contact_email, data)

        #Save the sheet to Google Sheets

        registration_data = [team_contact, team_name, team_contact_email, team_contact_phone]
        save_to_sheet(registration_data, 'https://docs.google.com/spreadsheets/d/1dGjZj-QNGjpn-oGTkeYKuHfw-okNSM6iYh-HLEN255A/edit?usp=sharing')


        st.success("Registration submitted successfully! You will receive a confirmation email shortly.")

    # Run this in your terminal: streamlit run your_script.py
