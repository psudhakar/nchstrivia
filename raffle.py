import streamlit as st

st.set_page_config(page_title="NCHS Trivia Night Raffle - After Prom 2024", page_icon="🎟️", layout="wide", menu_items={
    'Get Help': None,
    'Report a bug': None,
    'About': None
})

st.image("https://lh3.googleusercontent.com/d/1Wgypq9dt1SuxBbtjB3XcZ1-W-ztIMWse")

col1, col2, col3 = st.columns(3)

with col1:
   st.header("Basket #1")
   st.subheader("Perfect Prom Night")
   st.write("""Men's Warehouse rental & Biaggi's $40 gift cards. Great value gifts.""")
   st.write("""Total value: $298""")
   st.image("https://m.media-amazon.com/images/I/71EJua1AlML._AC_SX679_.jpg")
   
with col2:
   st.header("Basket #2") 
   st.subheader("Sports and Beyond")
   st.write("""$100 unit 5 pass, BTT 5 court rentals & BTT Cardio Tennis Classes. Wonderful gift!""")
   st.write("""Total value: $344""")
   st.image("https://m.media-amazon.com/images/I/71EJua1AlML._AC_SX679_.jpg")
   
with col3:
   st.header("Basket #3")
   st.subheader("Go Redbirds!")
   st.write("""4 Men's Football and 4 Men's Basketball tickets, ISU swag, popcorn, $100 Unit 5 game pass""")
   st.write("""Total value: $220""")  
   st.image("https://m.media-amazon.com/images/I/71EJua1AlML._AC_SX679_.jpg")
   
st.subheader("Purchase Raffle Tickets")


def split_correctly(n1, n2, n3):
    if n1 + n2 + n3 == max_tickets:
        return True
    else:
        return False

col1, col2 = st.columns(2)
n1 = 0
n2 = 0
n3 = 0

formSubmitted = False
with st.form(key='ticket_form', clear_on_submit=True):
    with col1:

            option = st.radio("Choose an option", ["5 tickets for $10", "12 tickets for $20"])
            if option == "5 tickets for $10":
                max_tickets = 5
            else:
                max_tickets = 12

            if n1 + n2 + n3 == max_tickets:
                st.success("Proceed with the purchase!")
            else:
                if n1 + n2 + n3 > max_tickets:
                    st.error("Number of tickets exceeds limit for selected option")
                else:
                    st.info("Split the tickets equally into three buckets")
                
    with col2:
        n1 = st.number_input("Number of tickets for Basket 1", min_value=0, max_value=12, value=0)
        n2 = st.number_input("Number of tickets for Basket 2", min_value=0, max_value=12, value=0) 
        n3 = st.number_input("Number of tickets for Basket 3", min_value=0, max_value=12, value=0)

    submitted = st.form_submit_button("Submit", disabled=not split_correctly(n1, n2, n3))

if submitted:  
    tickets = n1 + n2 + n3
    if tickets > max_tickets:
        st.error("Number of tickets exceeds limit for selected option")
    else:
        st.success("Raffle ticket purchase successful! If you have not already paid for the tickets, please proceed with following payment options!")
        st.header("Payment Options")

        # Payment options
        col1, col2, col3 = st.columns(3)
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
