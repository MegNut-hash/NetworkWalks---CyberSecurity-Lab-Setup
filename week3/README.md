# Week 3 – Password Cracking

Two modules this week, both cracking the same locked PDF (`My Locked PDF1.pdf`)
two different ways.

- [Module 1 – JTR / Johnny](module-1-jtr/notes.md)
- [Module 2 – Networkwalks tools](module-2-networkwalks-tools/notes.md)

## Summary
Both modules recovered the same password using a dictionary attack against
a hash extracted from the PDF. Module 1 uses real industry tooling (John
the Ripper). Module 2 uses Networkwalks' own browser-based hash
calculator and cracker with a 100-word built-in list — same idea, guided
through their site instead of local tools.

## Takeaways
- `$pdf$...` is the hash format `pdf2john` extracts from a
  password-protected PDF
- A dictionary attack only works if the actual password is in your
  wordlist — neither of these passwords ("password1", "good-luck")
  would survive five minutes against a real attacker
- Next step I want to do on my own: crack a password using hashcat and
  rockyou.txt instead of a small built-in list, to get a feel for a
  more realistic attack surface