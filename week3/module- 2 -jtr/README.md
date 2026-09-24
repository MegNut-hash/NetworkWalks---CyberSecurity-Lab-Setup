# Module 2 — Password Cracking with Networkwalks Tools

## Tools
Networkwalks Hash Calculator (networkwalks.com/hash-calculator) +
Networkwalks Password Cracker (networkwalks.com/password-cracker)

## Steps
1. Uploaded the same locked PDF to the Hash Calculator to extract the
   `$pdf$...` hash — screenshot: `nw-hash-calculator.png`
2. Pasted the hash into the Password Cracker, ran the built-in 100-word
   dictionary attack — screenshot: `nw-password-cracker-start.png`
3. Tool matched the password after 91/100 attempts — screenshot:
   `nw-password-cracker-cracked.png`

## Result
Password cracked: `password1`

## Notes
- Functionally the same idea as Module 1 (extract hash → dictionary
  match) but wrapped in Networkwalks' own site instead of local tools
- Built-in wordlist is fixed at 100 words — fine for a demo, not
  representative of a real attack, where lists like rockyou.txt run into
  the millions
- Less useful for the CV than Module 1 since it's not tooling anyone in
  the industry actually uses — good for understanding the concept,
  not for building a transferable skill