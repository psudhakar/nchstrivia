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
    message['Subject'] = 'NCHS After Prom 2024 Trivia Night Registration'

    body = f"Here is the registration data submitted:\n{data}"
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_user, smtp_password)
    server.send_message(message)
    server.quit()

def validate_email(email):
    # Regular expression pattern for basic email validation
    pattern = r"^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
    return re.match(pattern, email)

def validate_field(value):
    if len(value) == 0:
        return False
    else:
        return True

# Hide hamburger menu and footer
st.set_page_config(page_title="Trivia Night by NCHS After Prom Team", layout="wide", menu_items={
    'Get Help': None,
    'Report a bug': None,
    'About': None
})


st.markdown("""
    <style>
    .block-container {
        padding-top: 0rem;
    }
    .main {
       font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; align: center;
    }
    h1 {
        color: #ff6347;
        text-align: center;
    }
    
    h5 {
        color: dark;
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
            
    @media screen and (max-width: 768px) {
            .responsive-image {
                display: none;
            }
    }
    @media screen and (min-width: 768px) {
        .responsive-image2 {
            display: none;
        }
    }
            

    </style>
    """, unsafe_allow_html=True)


#col1, col2 = st.columns([1,50])

#with col1:
#    st.markdown(f"""<div style="text-align: center;">
#    <img src="https://github.com/psudhakar/nchstrivia/blob/main/nchslogo.jpg?raw=true" alt="Image"  style="margin-top: 30px;">
#    </div>""", unsafe_allow_html=True)

#with col2:
#st.image("https://github.com/psudhakar/nchstrivia/blob/main/trivia2.JPG?raw=true", use_column_width=True)

st.write("")  # This adds a blank line


#st.markdown(f"""
#    <img src="https://drive.google.com/uc?id=13lN1bASS74xakpsClZfCNyDAwVILIz-9" alt="Image"  style="margin-top: 30px; width=100%" >
#    """, unsafe_allow_html=True)

#st.image("https://drive.google.com/uc?id=13lN1bASS74xakpsClZfCNyDAwVILIz-9",use_column_width=True)

st.markdown("# NCHS Trivia Night 2024")
st.markdown("##### Organized by NCHS After Prom Parents Committee 2024")
st.markdown("##### Sweat the Questions, Sweeten the Charity Pot: Trivia Night for a Good Cause!")

col1, col2 = st.columns(2)

with col1:
    with st.container():
        # Event details
        st.header("Join Us!")
        st.markdown("""
        - 🗓️ **Date:** Saturday, February 3rd, 2024
        - 🕗 **Time:** 6 PM to 9 PM
        - 📍 **Venue:** , Parke Regency & Conference Center. 1413, Leslie Dr, Bloomington, IL
        - 💡 Hosted by the legendary Twin City Trivia!
        """)

    st.markdown("Join us for an unforgettable evening of brain-bending trivia and feel-good fun at our Trivia Night Fundraiser 2024 benefiting a safer After prom. Get ready for an epic trivia throwdown masterminded by Jr. Classboard's most imaginative parents and hosted by the legendary Twin City Trivia")
    # Registration instructions
    st.header("Registration")
    st.markdown("""
        1.	Gather your cleverest crew and register your team below!
        2. **Squad Discount:** Only \$100 for a table of 6, otherwise $20 per individual
        2.	Flying solo, no problem! We are Trivia matchmakers, ready to pair you with your trivia soulmates!
        3.	Fuel your brains with delicious snacks and drinks (available for purchase)!
        4.	Put your heads together to conquer tricky questions and earn bragging rights!
        5.	Most importantly, support a fantastic cause: creating a safe and memorable Afterprom experience for our NCHS students!
        6.  Come dressed in a Hawaiian theme, even decorate your table to win best themed table!
        7.  Doors open at 6pm, Trivia starts at 7pm - 9pm
                
    """, unsafe_allow_html=True)

    st.markdown("""
        Reserve your table by filling the form below. Payments can be made by check, or using any payment methods below:
    """, unsafe_allow_html=True)

    # Form for registration
    with st.form(key='registration_form', clear_on_submit=True):
        st.markdown("#### Team Registration - NCHS After Prom 2024 Trivia Night")
        team_contact = st.text_input("Team Contact:")
        team_name = st.text_input("Team Name:")
        team_contact_email = st.text_input("Email address for Team Contact:")
        team_contact_phone = st.text_input("Phone number for Team Contact:")
        where_heard = st.selectbox(
            "Where did you hear about Trivia Night?",
            ("Facebook/Instagram", "Email communication", "NCHS Staff", "Others"),
            index=0  # Set the default selection to "Facebook/Instagram" (index 0)
        )

        is_nchs_educator = st.radio(
            "Are you an NCHS educator?",
            ("yes", "no"),
            index=1  # Set the default selection to "no" (index 1)
        )

        
        # Submit button
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        with st.spinner("Processing..."):
            if validate_email(team_contact_email) and validate_field(team_name) and validate_field(team_contact) and validate_field(team_contact_phone):
                # Prepare the data to be sent via email
                data = f"""
                Team Contact: {team_contact}
                Team Name: {team_name}
                Team Contact Email: {team_contact_email}
                Team Contact Phone: {team_contact_phone}
                """
                data += "\n\nUse any payment methods below, if you have not paid yet. \n\n"
                data += "Please add your name or email address in the comments section of the payment. \n\n"
                data += "Using Venmo, pay to  : @Li-Boyer \n\n"
                data += "Using Zelle, pay to  : (309) 826-5826 (Li Boyer) \n\n"
                data += "Using Paypal, pay to  : Carriezhengli@gmail.com (Li Boyer) \n\n"
                data += "Make checks payable to 'NCHS After Prom' and mail to `5018 Londonderry Road Bloomington IL - 61705 \n\n"

                data += "For any questions, please contact nchsjr.board@gmail.com \n"
                

                # Send the email
                send_email(team_contact_email, data)

                #Save the sheet to Google Sheets
                now = datetime.now()
                date_time = now.strftime("%Y-%m-%d %H:%M:%S")

                registration_data = [team_contact, team_name, team_contact_email, team_contact_phone, date_time, where_heard, is_nchs_educator]
                save_to_sheet(registration_data, 'https://docs.google.com/spreadsheets/d/1dGjZj-QNGjpn-oGTkeYKuHfw-okNSM6iYh-HLEN255A/edit?usp=sharing')
                st.success("Registration submitted successfully! \nNext steps: \nPlease submit a payment for \$100 for 6 players per table. \nIf you are playing solo, pay \$20 per person, and we will team you up with wonderful trivia soulmates!")
            else:
                st.markdown(':red[Make sure to enter Team name, Team, Contact, Phone Number and valid email address!]')


with col2:
    #st.image("https://github.com/psudhakar/nchstrivia/blob/main/trivia2.JPG?raw=true", use_column_width=None)
    st.markdown(f"""<div style="text-align: center;">
    <img src="https://lh3.googleusercontent.com/d/1u_vpxUp3EtysOCCtGx9tGjkPPbkgMnI2" alt="Flyer"  style="margin-top: 30px;" class="responsive-image" >
    </div>""", unsafe_allow_html=True)

# Streamlit app layout
#st.set_page_config(page_title='Trivia Night Registration', layout='centered')
#logo_url = "https://github.com/psudhakar/nchstrivia/blob/main/trivia3.JPG?raw=true"
#logo_url = "https://drive.google.com/uc?id=1SfAQ50kW6gybO-Pqcs6mFWQ2DiLY0mcH"


    

st.header("Payment Options")

# Payment options
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown("#### Venmo")
    st.markdown("Click [here](https://venmo.com/Li-Boyer) or send it to @Li-Boyer")
    st.image("https://lh3.googleusercontent.com/d/1c0iAc6b2o48oYFCb8raC0qrn0D47ag6F", use_column_width=None)
with col2:
    st.markdown("#### Zelle")
    st.markdown("Send your payments to: (309) 826-5826 (Li Boyer)")
    st.image("https://lh3.googleusercontent.com/d/1ywiw7qvUwiU7yPJPwGaykyZ7IHxbdRhn", use_column_width=None)
with col3:
    st.markdown("#### Paypal")
    st.markdown("Send your payments to:  Carriezhengli@gmail.com (Li Boyer) ")
    st.image("https://lh3.googleusercontent.com/d/1A8QlPnO7WJx2P_MwKBZz4TAYj5PLhlfm", use_column_width=None)
with col4:
    st.markdown("#### Pay by Check")
    st.markdown("Make checks payable to: 'NCHS After Prom' and mail to: 5018 Londonderry Road Bloomington IL - 61705")

# -----------------
# Contact Us Section
# -----------------
st.markdown("## Contact Us")
st.markdown("For any queries or feedback, feel free to reach out to us:")
st.markdown(":email: **Email:** [nchsjr.board@gmail.com](mailto:nchsjr.board@gmail.com)")
st.markdown(":blue_heart: **Facebook:** [Nchs After Prom]   (https://www.facebook.com/people/Nchs-After-Prom/100013162357686/)")
st.markdown(":camera: **Instagram:** [nchs_afterprom](https://instagram.com/nchs_afterprom)")
st.markdown(":phone: **Contact:** Li Boyer - (309) 826 5826 | Srinivas Talasu - (309) 750-1456")

st.markdown(f"""<div style="text-align: center;">
<img src="https://lh3.googleusercontent.com/d/1u_vpxUp3EtysOCCtGx9tGjkPPbkgMnI2" alt="Image"  style="margin-top: 30px;" class="responsive-image2">
</div>""", unsafe_allow_html=True)
