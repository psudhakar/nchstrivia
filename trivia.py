import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# ... [Your existing function definitions]

# Improved page configuration
st.set_page_config(
    page_title="NCHS Trivia Night 2024",
    layout="wide",
    menu_items={
        'Get Help': 'https://www.yourhelpsite.com',
        'Report a bug': 'https://www.yourbugreportsite.com',
        'About': "# This is a great event organized by NCHS!"
    }
)

# Improved styling
st.markdown("""
    <style>
    .main {
       font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }
    h1 {
        color: #ff6347;
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

# Header section
#st.image("https://yourimagelink.com/image.jpg", width=700)
st.markdown("# Trivia Night 2024 - NCHS After Prom Event")
st.markdown("### An exciting trivia night organized by the NCHS After Prom Parents Committee")

# Registration form
with st.form(key='registration_form', clear_on_submit=True):
    st.markdown("#### Team Registration Form")
    team_contact = st.text_input("Team Contact Name", placeholder="Enter your full name")
    team_name = st.text_input("Team Name", placeholder="Your team's awesome name")
    team_contact_email = st.text_input("Email", placeholder="name@example.com")
    team_contact_phone = st.text_input("Phone Number", placeholder="123-456-7890")
    submit_button = st.form_submit_button("Submit Registration")

# Processing form submission
if submit_button:
    # [Your existing email and sheet updating logic]

    st.success("Thank you for registering! You will receive a confirmation email shortly.")

# Payment methods section
st.markdown("### Payment Methods")
# [Your existing code for payment methods]

# Footer
st.markdown("---")
st.markdown("### Contact Us")
st.markdown("For any inquiries, please email us at [nchsjr.board@gmail.com](mailto:nchsjr.board@gmail.com) or call us at (404) 800-3312.")
st.markdown("Follow us on [Facebook](https://www.facebook.com/NCHS) and [Twitter](https://www.twitter.com/NCHS) for updates!")

# Hide Streamlit branding
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True) 
