import streamlit as st
import uuid
import base64
import time
from cryptography.fernet import Fernet

# Function to display the animated title
def animated_title(text, colors, delay=0.1):
    placeholder = st.empty()
    styled_text = ""
    
    for i, char in enumerate(text):
        color = colors[i % len(colors)]
        styled_text += f"<span style='color:{color};'>{char}</span>"
        placeholder.markdown(f"<h1 style='text-align:center;'>{styled_text}</h1>", unsafe_allow_html=True)


def generate_key():
    return Fernet.generate_key()


def encrypt_message(message, key):
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    return encrypted_message


def decrypt_message(encrypted_message, key):
    fernet = Fernet(key)
    try:
        decrypted_message = fernet.decrypt(encrypted_message).decode()
        return decrypted_message
    except Exception:
        return "Invalid key or message not found."

# Main function to handle page layout and navigation
def main():
    st.set_page_config(page_title="CampusConnect", layout="wide")
    
   
    title_text = "CampusConnect"
    colors = ["#FF5733", "#33FF57", "#3357FF", "#F333FF", "#33FFF6"]
    animated_title(title_text, colors)
    
    st.write("Connect with friends from your university or department!")

    # Sidebar for navigation
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
    
    # Homepage slideshow
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

# Homepage slideshow function with reduced image size
def display_homepage():
    images = ["sample.jpg", "sampleImg1.jpg", "sampleImg2.jpg"]  # Replace with actual image file paths
    placeholder = st.empty()
    
    while True:
        for img in images:
            placeholder.image(img, width=1000)  # Adjust width to control size
            time.sleep(3)

# Log In page
def login():
    st.subheader("Log In")
    username = st.text_input("Enter your username")
    password = st.text_input("Enter your password", type="password")
    
    if st.button("Log In", key="login_button"):
        st.success(f"Welcome, {username}!")
        st.session_state.current_page = "Find Friend"

# Sign Up page
def signup():
    st.subheader("Sign Up")
    
    name = st.text_input("Full Name")
    university = st.text_input("University/ College/ School")
    dept_name = st.text_input("Department")
    session = st.text_input("Session (e.g., 2024-2028)")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    if st.button("Create Account", key="signup_button"):
        st.success(f"Welcome {name}! You’ve successfully signed up.")

# Find Friends page
def find_friends():
    st.subheader("Find Friends")
    
    personality = st.selectbox("Choose personality", ["Friendly", "Outgoing", "Introverted", "Adventurous"])
    university = st.text_input("University")
    department = st.text_input("Department")
    session = st.text_input("Session")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    
    if st.button("Search for Friends", key="search_friends_button"):
        st.write(f"Showing friends who are {personality}, from {university}, {department}, session {session}.")

# Message system with encryption
def message_system():
    st.subheader("Messages System")
    action = st.radio("Choose an action", ["Send Message", "View Message"], key="message_action")
    
    if action == "Send Message":
        message = st.text_area("Enter your message")
        key = st.text_input("Enter a secret key for encryption")
        
        if st.button("Send Message", key="send_message_button"):
            if key and message:
                encrypted_message = encrypt_message(message, key.encode())
                st.session_state.saved_message = encrypted_message
                st.success("Message encrypted and saved.")
            else:
                st.error("Both message and encryption key are required.")
    
    elif action == "View Message":
        key = st.text_input("Enter the secret key to view the message")
        
        if st.button("View Message", key="view_message_button"):
            if 'saved_message' in st.session_state:
                decrypted_message = decrypt_message(st.session_state.saved_message, key.encode())
                if decrypted_message != "Invalid key or message not found.":
                    st.write(f"Decrypted Message: {decrypted_message}")
                else:
                    st.error(decrypted_message)
            else:
                st.error("No saved message found.")

if __name__ == "__main__":
    main()
