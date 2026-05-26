import os
import subprocess

def open_excel():
    file_path = "students.xlsx"

    # Check if file exists
    if not os.path.exists(file_path):
        print("No Excel file found!")
        return

    try:
        # Windows (your case)
        os.startfile(file_path)
    except AttributeError:
        # Fallback (Linux / Mac)
        subprocess.call(["open", file_path])