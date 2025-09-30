import streamlit as st
import os

# Base folder for uploads
BASE_UPLOAD_FOLDER = "uploads"
os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

st.title("📂 View Your Stored Files by ID")

# --- User ID Input ---
user_id = st.text_input("🆔 Enter your User ID")

if user_id:
    user_folder = os.path.join(BASE_UPLOAD_FOLDER, user_id)

    if os.path.exists(user_folder):
        files = os.listdir(user_folder)

        if files:
            st.header("📑 Your Files")
            for file in files:
                filepath = os.path.join(user_folder, file)
                with open(filepath, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {file}",
                        data=f,
                        file_name=file,
                        key=f"download-{user_id}-{file}"
                    )
        else:
            st.info("No files found in your folder.")
    else:
        st.error("❌ No such User ID found. Please check and try again.")
else:
    st.warning("⚠️ Please enter your User ID to view files.")
