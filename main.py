import csv
import hashlib
import os
import shutil
import PyPDF2
from tkinter import Tk, filedialog


# ----------------------------
# Helper Functions
# ----------------------------
def hash_password(password: str) -> str:
    """Return a SHA256 hash of the password"""
    return hashlib.sha256(password.encode()).hexdigest()


def init_files():
    """Initialize CSV files and folders if they don't exist"""
    if not os.path.exists("patients.csv"):
        with open("patients.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ABHA ID", "password", "name", "age", "doctor_assigned", "family_contact"])

    if not os.path.exists("doctors.csv"):
        with open("doctors.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ABHA ID", "password", "name", "specialization"])

    os.makedirs("documents/patient_uploads", exist_ok=True)
    os.makedirs("documents/doctor_uploads", exist_ok=True)
    os.makedirs("users_data", exist_ok=True)


# ----------------------------
# Signup Logic
# ----------------------------
def signup(user_type: str, username: str, password: str, **kwargs) -> str:
    filename = "patients.csv" if user_type == "patient" else "doctors.csv"

    # Check if user already exists
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ABHA ID"] == username:
                return f"❌ {user_type.capitalize()} with this ABHA ID already exists."

    # Store new user
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        if user_type == "patient":
            writer.writerow([
                username, hash_password(password),
                kwargs.get("name", ""), kwargs.get("age", ""),
                kwargs.get("doctor_assigned", ""), kwargs.get("family_contact", "")
            ])
        else:  # doctor
            writer.writerow([
                username, hash_password(password),
                kwargs.get("name", ""), kwargs.get("specialization", "")
            ])

    return f"✅ {user_type.capitalize()} registered successfully."


# ----------------------------
# Login Logic
# ----------------------------
def login(user_type: str, username: str, password: str):
    filename = "patients.csv" if user_type == "patient" else "doctors.csv"
    hashed_pw = hash_password(password)

    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["ABHA ID"] == username and row["password"] == hashed_pw:
                print(f"✅ {user_type.capitalize()} login successful. Welcome {row['name']}!")
                return row
    print(f"❌ Invalid ABHA ID or password for {user_type}.")
    return None


# ----------------------------
# Patient Features
# ----------------------------
def emergency_notify(patient_data):
    """Simulate emergency notification"""
    doctor = patient_data.get("doctor_assigned", "Unknown Doctor")
    family = patient_data.get("family_contact", "Unknown Contact")
    print(f"🚨 Emergency! Notifying Doctor: {doctor} and Family: {family}")


def view_documents(patient_username):
    """View patient documents"""
    patient_dir = f"users_data/{patient_username}"
    if not os.path.exists(patient_dir):
        print("📂 No documents found for this patient.")
        return

    files = os.listdir(patient_dir)
    if not files:
        print("📂 No documents uploaded yet.")
        return

    print(f"\n📑 Documents for {patient_username}:")
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")


def upload_document(patient_username):
    """Upload a new PDF or image for the patient"""
    Tk().withdraw()
    file_path = filedialog.askopenfilename(
        title="Select a PDF or Image file",
        filetypes=[("PDF or Image Files", "*.pdf;*.jpg;*.jpeg;*.png")]
    )

    if not file_path:
        print("❌ No file selected.")
        return

    user_dir = f"users_data/{patient_username}"
    os.makedirs(user_dir, exist_ok=True)

    filename = os.path.basename(file_path)
    dest_path = os.path.join(user_dir, filename)
    shutil.copy(file_path, dest_path)
    print(f"✅ File saved as {dest_path}")

    # If PDF, show first page text
    if filename.lower().endswith(".pdf"):
        try:
            with open(dest_path, "rb") as file:
                reader = PyPDF2.PdfReader(file)
                print(f"Pages: {len(reader.pages)}")
                if reader.pages:
                    print("--- Page 1 ---")
                    print(reader.pages[0].extract_text())
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")


def patient_home(patient_data):
    """Main menu for patient after login"""
    username = patient_data["ABHA ID"]
    while True:
        print("\n🏠 Patient Home Page")
        print("1. Emergency notify doctor/family")
        print("2. View uploaded documents")
        print("3. Upload new document")
        print("4. Logout")

        choice = input("Select an option (1-4): ")

        if choice == "1":
            emergency_notify(patient_data)
        elif choice == "2":
            view_documents(username)
        elif choice == "3":
            upload_document(username)
        elif choice == "4":
            print("👋 Logged out successfully.")
            break
        else:
            print("❌ Invalid choice, try again.")


# ----------------------------
# Main Program
# ----------------------------
if __name__ == "__main__":
    init_files()

    while True:
        print("\n=== Healthcare System ===")
        print("1. Signup as Patient")
        print("2. Signup as Doctor")
        print("3. Login as Patient")
        print("4. Login as Doctor")
        print("5. Exit")

        action = input("Choose option: ")

        if action == "1":
            uname = input("ABHA ID: ")
            pw = input("Password: ")
            name = input("Name: ")
            age = input("Age: ")
            doctor = input("Assigned Doctor ABHA ID: ")
            family = input("Family Contact: ")
            print(signup("patient", uname, pw, name=name, age=age,
                         doctor_assigned=doctor, family_contact=family))

        elif action == "2":
            uname = input("ABHA ID: ")
            pw = input("Password: ")
            name = input("Name: ")
            spec = input("Specialization: ")
            print(signup("doctor", uname, pw, name=name, specialization=spec))

        elif action == "3":
            uname = input("ABHA ID: ")
            pw = input("Password: ")
            patient = login("patient", uname, pw)
            if patient:
                patient_home(patient)

        elif action == "4":
            uname = input("ABHA ID: ")
            pw = input("Password: ")
            doctor = login("doctor", uname, pw)
            if doctor:
                print("👨‍⚕️ Doctor dashboard is under development...")

        elif action == "5":
            print("Goodbye 👋")
            break
        else:
            print("❌ Invalid choice, try again.")
