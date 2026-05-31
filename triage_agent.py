# triage_agent.py
import subprocess
import json
import os
from google import genai

# Membaca API Key langsung dari string (Aman untuk testing lokal malam ini)
API_KEY = "GEMINI_API_KEY"

if not API_KEY:
    print("[-] ERROR: API Key Gemini tidak ditemukan!")
    exit(1)

# Inisialisasi Google GenAI Client yang baru (Standar Tahun 2026)
client = genai.Client(api_key=API_KEY)

def run_sast_scan():
    print("[*] Menjalankan Bandit SAST Engine pada repositori...")
    result = subprocess.run(['bandit', '-f', 'json', 'app.py'], capture_output=True, text=True)
    try:
        return json.loads(result.stdout)
    except Exception:
        return json.loads(result.stdout)

def ask_ai_triage(issue):
    prompt = f"""
    Kamu adalah Senior Product Security Engineer ahli di Funding Societies | Modalku Group.
    Tugas Anda adalah menganalisis hasil scan otomatis dari alat SAST berikut untuk memilah mana bug riil (True Positive) dan mana salah deteksi (False Positive).

    INFORMASI TEMUAN:
    - Nama Celah Keamanan: {issue['issue_text']}
    - Tingkat Bahaya (Severity): {issue['issue_severity']}
    - Baris Kode yang Rusak:
    {issue['code']}

    Berikan laporan triase profesional dengan format Markdown:
    ### 🚨 Temuan: {issue['issue_text']}
    - **Status Analisis:** [True Positive] ATAU [False Positive]
    - **Analisis Dampak Bisnis (FinTech Context):** Jelaskan mengapa celah ini sangat berbahaya jika dieksploitasi pada aplikasi keuangan/pendanaan digital (kaitkan dengan kerugian finansial atau kebocoran data).
    - **Rekomendasi Secure Coding (Remediasi):** Berikan potongan kode Python yang sudah diperbaiki 100% aman sesuai standar OWASP untuk menggantikan kode yang rusak di atas.
    """
    
    # Memanggil model gemini-2.5-flash menggunakan SDK baru yang direkomendasikan Google
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt,
    )
    return response.text

def main():
    sast_results = run_sast_scan()
    vulnerabilities = sast_results.get('results', [])

    print(f"[+] Scan selesai. Ditemukan {len(vulnerabilities)} potensi kerentanan.")

    with open("SECURITY_AUDIT_REPORT.md", "w") as report_file:
        report_file.write("# 🛡️ Automated GenAI Security Triaging Report\n")
        report_file.write("Laporan ini dibuat otomatis oleh AI Security Agent di dalam CI/CD Pipeline.\n\n")

        for idx, vuln in enumerate(vulnerabilities, 1):
            print(f"[*] AI sedang memproses temuan #{idx}...")
            ai_report = ask_ai_triage(vuln)
            report_file.write(ai_report)
            report_file.write("\n\n---\n\n")

    print("[+] Sukses! Laporan 'SECURITY_AUDIT_REPORT.md' telah berhasil dibuat.")

if __name__ == "__main__":
    main()
