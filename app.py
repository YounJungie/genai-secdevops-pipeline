# app.py
import os
import sqlite3

# 1. CRITICAL BUG: Hardcoded Credentials
DB_PASSWORD = "FintechSuperSecretPassword2026!"

def get_user_profile():
    # 2. CRITICAL BUG: Broken Object Level Authorization (IDOR/BAC)
    # Mengambil data langsung berdasarkan parameter ID tanpa memeriksa session token / kepemilikan
    user_id = input("Masukkan User ID Anda untuk melihat profil: ")
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM profiles WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()

def generate_report_pdf():
    # 3. CRITICAL BUG: Command Injection via OS Command Execution
    report_name = input("Masukkan nama file laporan yang ingin diexport: ")
    os.system(f"mkdir -p /tmp/reports && touch /tmp/reports/{report_name}.pdf")

if __name__ == "__main__":
    print("Aplikasi FinTech Simpan Pinjam v1.0")
