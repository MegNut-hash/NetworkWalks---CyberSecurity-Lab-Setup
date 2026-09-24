# Module 1 — Password Cracking with JTR

## Tools
John the Ripper (JTR) + Johnny (GUI front end)

## Steps
1. Downloaded the encrypted PDF (`My Locked PDF1.pdf`)
2. Extracted the hash using onlinehashcrack.com's PDF hash extractor
   (pdf2john under the hood) — screenshot: `onlinehashcrack-upload-output.png`
3. Saved the hash to a text file for Johnny to read — screenshot:
   `hash-saved-cracked-txt.png`
4. Pointed Johnny at the local `john.exe` binary — screenshot:
   `johnny-settings-jtr-path.png`
5. Loaded the hash file, ran the attack

## Result
Password cracked: `password1` — screenshot: `johnny-cracked-password1.png`

Ran a second pass on a different hash, password `good-luck` — screenshot:
`johnny-cracked-good-luck.png`

## Notes
- Hash format: `$pdf$4*4*128*...` — the `4*4*128` bit encodes the PDF
  revision, algorithm version, and key length
- JTR is the actual tool used in real pentesting/security work, unlike
  the browser tool in Module 2 — worth understanding the CLI args
  properly rather than relying on Johnny's GUI long term