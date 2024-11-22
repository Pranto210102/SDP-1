import streamlit as st
import requests
import bcrypt
import time


# Google Apps Script Web App URL
GOOGLE_SHEET_WEBHOOK = "https://script.google.com/macros/s/AKfycbwmX5hOPz5jvqZDJINBJMVo8GTAj7gZ1rwrJvbGB4sJh7PJSRC3_XzBPs8sVciKfMzZ/exec"


# Utility functions for password hashing
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed.encode())


# Functions to interact with Google Sheets
def sign_up_user(name, university, department, session, gender, username, password):
    hashed_password = hash_password(password)  # Hash the password before sending
    payload = {
        "action": "sign_up",
        "name": name,
        "university": university,
        "department": department,
        "session": session,
        "gender": gender,
        "username": username,
        "password": hashed_password,
    }
    response = requests.post(GOOGLE_SHEET_WEBHOOK, json=payload)
    return response.text

def log_in_user(username, password):
    payload = {
        "action": "log_in",
        "username": username,
    }
    response = requests.post(GOOGLE_SHEET_WEBHOOK, json=payload)
    if response.status_code == 200:
        stored_hashed_password = response.text
        if verify_password(password, stored_hashed_password):
            return "Login successful"
    return "Invalid credentials"


# Animated title
def animated_title(text, colors, delay=0.2):
    placeholder = st.empty()
    styled_text = ""
    
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        styled_text += f"<span style='color:{color};'>{char}</span>"
        placeholder.markdown(f"<h1 style='text-align:center;'>{styled_text}</h1>", unsafe_allow_html=True)


# Homepage slideshow
def display_homepage():
    images = [
        "https://cdn.pixabay.com/photo/2022/07/24/11/35/women-7341444_1280.jpg",
        "https://cdn.pixabay.com/photo/2016/02/05/16/19/offices-1181385_1280.jpg",
        "https://cdn.pixabay.com/photo/2024/03/12/07/54/students-8628244_1280.jpg",
        "https://images.pexels.com/photos/5676744/pexels-photo-5676744.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1"
    ]
    placeholder = st.empty()
    while True:
        for img in images:
            placeholder.image(img, width=1000)
            time.sleep(3)


# Pages
def login():
    st.subheader("Log In")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    
    if st.button("Log In", key="login_button"):
        result = log_in_user(username, password)
        if result == "Login successful":
            st.success(f"Welcome, {username}!")
            st.session_state.current_page = "Find Friend"
        else:
            st.error("Invalid credentials. Please try again.")


def signup():
    st.subheader("Sign Up")
    name = st.text_input("Full Name")
    university = st.text_input("University/ College/ School")
    dept_name = st.text_input("Department")
    session = st.text_input("Session (e.g., 2024-2028)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    username = st.text_input("Choose a Username")
    password = st.text_input("Choose a Password", type="password")
    
    if st.button("Create Account", key="signup_button"):
        result = sign_up_user(name, university, dept_name, session, gender, username, password)
        if result == "Sign-up successful":
            st.success(f"Welcome {name}! You’ve successfully signed up.")
            st.session_state.current_page = "Log In"
        else:
            st.error("Sign-up failed. Please try again.")


def find_friends():
    st.subheader("Find Friends")
    personality = st.selectbox("Choose personality", ["Friendly", "Outgoing", "Introverted", "Adventurous"])
    university = st.text_input("University")
    department = st.text_input("Department")
    session = st.text_input("Session")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    if st.button("Search for Friends", key="search_friends_button"):
        st.write(f"Showing friends who are {personality}, from {university}, {department}, session {session}.")


def message_system():
    st.subheader("Messages System")
    action = st.radio("Choose an action", ["Send Message", "View Message"], key="message_action")
    
    if action == "Send Message":
        message = st.text_area("Enter your message")
        key = st.text_input("Enter a secret key for encryption")
        if st.button("Send Message", key="send_message_button"):
            if key and message:
                st.success("Message sent successfully!")
            else:
                st.error("Both message and encryption key are required.")
    elif action == "View Message":
        key = st.text_input("Enter the secret key to view the message")
        if st.button("View Message", key="view_message_button"):
            st.error("Feature not implemented.")


def main():
    st.set_page_config(page_title="CampusConnect", layout="wide")

    title_text = "CampusConnect"
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#33FFF6"]
    animated_title(title_text, colors)

    st.write("Connect with friends from your university or department!")

    # Sidebar navigation
    with st.sidebar:
        st.write("## Navigation")
        if st.button("Log In", key="sidebar_login"):
            st.session_state.current_page = "Log In"
        if st.button("Sign Up", key="sidebar_signup"):
            st.session_state.current_page = "Sign Up"
        if st.button("Find Friend", key="sidebar_find_friend"):
            st.session_state.current_page = "Find Friend"
        if st.button("Messages", key="sidebar_messages"):
            st.session_state.current_page = "Messages"

    if "current_page" not in st.session_state or st.session_state.current_page == "Home":
        display_homepage()
    elif st.session_state.current_page == "Log In":
        login()
    elif st.session_state.current_page == "Sign Up":
        signup()
    elif st.session_state.current_page == "Find Friend":
        find_friends()
    elif st.session_state.current_page == "Messages":
        message_system()


if __name__ == "__main__":
    main()
