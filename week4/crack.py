import sys
from pypdf import PdfReader


def crack_pdf(pdf_path, wordlist_path):
  print(f"[*] Loading PDF: {pdf_path}")
  reader = PdfReader(pdf_path)

  if not reader.is_encrypted:
    print("[!] The provided PDF is not password protected.")
    return

  print(f"[*] Loading wordlist: {wordlist_path}")
  try:
    with open(wordlist_path, "r", encoding="latin-1") as f:
      passwords = f.readlines()
  except FileNotFoundError:
    print(f"[!] Wordlist file not found: {wordlist_path}")
    return

  print(f"[*] Testing {len(passwords)} candidate passwords...")

  for i, pwd in enumerate(passwords):
    password = pwd.strip()

    # Attempt to decrypt the PDF with the current wordlist entry
    if reader.decrypt(password):
      print(f"\n[+] SUCCESS! Password found: '{password}'")
      return password

    # Progress indicator every 1,000 attempts
    if i > 0 and i % 1000 == 0:
      print(f"[*] Tested {i} passwords...")

  print("\n[-] Password not found in the provided wordlist.")
  return None


if __name__ == "__main__":
  if len(sys.argv) < 3:
    print("Usage: python pdf_cracker.py <pdf_file> <wordlist_file>")
    print("Example: python pdf_cracker.py report.pdf rockyou.txt")
  else:
    crack_pdf(sys.argv[1], sys.argv[2])