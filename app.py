import streamlit as st
from cryptography.fernet import Fernet

# --- 🧑‍💻 Hardcoded user credentials ---
USERS = {
    "admin": "password123",
    "user1": "securepass"
}

# --- 🔐 Session management ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

# --- 🔑 Generate/load encryption key ---
@st.cache_resource
def load_key():
    return Fernet.generate_key()

fernet = Fernet(load_key())

# --- 👤 Login Page ---
def login():
    st.title("🔐 Secure Data Encryption System")
    st.subheader("👋 Welcome! Please log in to continue")

    username = st.text_input("🧑 Username")
    password = st.text_input("🔑 Password", type='password')

    if st.button("🔓 Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.success("✅ Login successful!")
        else:
            st.error("❌ Invalid username or password")

# --- 🔒 Encryption/Decryption Page ---
def encryption_page():
    st.title("🔐 Secure Data Encryption System")
    st.subheader("🛡️ Encrypt or Decrypt your data securely")

    st.write("📝 Enter your message below:")
    text_input = st.text_area("✉️ Your Text Here")

    action = st.radio("⚙️ What would you like to do?", ("🔒 Encrypt", "🔓 Decrypt"))

    if st.button("🚀 Submit"):
        if action == "🔒 Encrypt":
            encrypted = fernet.encrypt(text_input.encode()).decode()
            st.success("✅ Encrypted Text:")
            st.code(encrypted)
        else:
            try:
                decrypted = fernet.decrypt(text_input.encode()).decode()
                st.success("✅ Decrypted Text:")
                st.code(decrypted)
            except Exception as e:
                st.error("⚠️ Decryption failed. Please check your input.")

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

# --- 🚦 App Flow ---
if not st.session_state.logged_in:
    login()
else:
    encryption_page()
