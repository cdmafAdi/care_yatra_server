import streamlit as st
import os

# Base folder for uploads
def app():
    BASE_UPLOAD_FOLDER = "uploads"
    os.makedirs(BASE_UPLOAD_FOLDER, exist_ok=True)

    st.title("☁️ Mini Cloud Storage with User ID")

    # --- User ID Input ---
    user_id = st.text_input("🆔 Enter your User ID")

    if user_id:
        # Create folder for this user
        user_folder = os.path.join(BASE_UPLOAD_FOLDER, user_id)
        os.makedirs(user_folder, exist_ok=True)

        # --- Upload Section ---
        st.header("📤 Upload a File")
        uploaded_file = st.file_uploader("Choose a file", type=None)

        if uploaded_file is not None:
            filepath = os.path.join(user_folder, uploaded_file.name)
            with open(filepath, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"✅ File uploaded successfully!")

        # --- Download Section ---
        st.header("📥 Download Your Files")
        files = os.listdir(user_folder)

        if files:
            for file in files:
                filepath = os.path.join(user_folder, file)
                with open(filepath, "rb") as f:
                    st.download_button(
                        label=f"⬇️ Download {file}",
                        data=f,
                        file_name=file,
                        key=f"download-{user_id}-{file}"  # unique key for each file
                    )
        else:
            st.info("No files uploaded yet.")
    else:
        st.warning("⚠️ Please enter your User ID to upload/download files.")
