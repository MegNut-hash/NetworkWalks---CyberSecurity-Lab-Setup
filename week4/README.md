# Week 4 — Penetration Testing Report: Mediroza General Hospital

**Target:** https://medirozahospital.com/index.html
**Engagement:** Networkwalks Cybersecurity Internship — Milestone 4
**Classification:** Confidential
**Date:** 01 October 2026

> This engagement was conducted in a controlled environment for educational purposes. The target was authorised for security testing. These techniques must never be applied to any system without explicit written permission from the owner.

---

## 1. Executive Summary

During an authorised penetration test of medirozahospital.com, two independent, critical weaknesses were identified that together exposed highly sensitive patient, staff, and corporate data.

The patient portal login form was found to be vulnerable to SQL injection, allowing full authentication bypass using the classic payload `admin' --` in the username field with no valid password. This granted access to an authenticated area containing three password-protected patient pathology reports. All three PDF passwords were subsequently recovered through dictionary and wordlist attacks, exposing full patient names, dates of birth, referring clinicians, and lab results.

Separately, a legacy backup directory (`/old/`) was found still publicly accessible on the web server. It contained a full SQL database export (`mediroza_db_backup_2019.sql`) with 30 staff records — including South African national ID numbers and monthly salaries — and 10 shareholder records disclosing ownership percentages and share classes, including for named clinical and executive staff.

Both issues are rated **Critical**. The backup directory exposure in particular requires no authentication, no exploitation skill, and no knowledge of the SQL injection flaw to find — it is reachable by anyone who guesses or crawls the path, which makes it the more urgent of the two to remediate.

### Summary of Findings

| Finding | Risk Rating | Why |
|---|---|---|
| F1 — SQL Injection / Auth Bypass | **Critical** | Unauthenticated full access-control bypass on the patient login |
| F2 — Patient PDF Reports Exposed & Cracked | **High** | PII and health data of 3 named patients recovered; required F1 first |
| F3 — Exposed Legacy DB Backup (`/old/`) | **Critical** | National IDs, salaries, and equity data for 40 individuals; zero auth required, independent of F1 |

---

## 2. Scope and Methodology

**Target:** https://medirozahospital.com/index.html

**Authorisation:** Testing was authorised by the owners of the website for the purpose of identifying vulnerabilities, as part of a Networkwalks Cybersecurity Internship engagement.

**Approach:** Black-box testing was performed against the public-facing patient portal with no credentials supplied in advance. Input fields were manually tested for injection weaknesses, and common legacy/backup paths were manually enumerated against the web root.

**Tools used:**
- Manual browser-based testing of the patient login form
- Boolean-based SQL injection payload (`admin' --`)
- [Networkwalks Hash Calculator](https://networkwalks.com/hash-calculator/) — pdf2john-based hash extraction from PDF
- [Networkwalks Password Cracker](https://networkwalks.com/password-cracker/) — dictionary attack against extracted PDF hashes
- Custom Python script ([`crack.py`](crack.py), built on `pypdf`) for offline dictionary attacks where the built-in wordlist was insufficient
- RockYou wordlist (`rockyou.txt`)
- Manual directory enumeration (`/old/`)

**Limitations:** This engagement was limited to the externally reachable web application and publicly exposed files. No internal network, server infrastructure, or social engineering testing was performed. The SQL injection vector was confirmed functionally (successful authentication bypass) but was not further exploited to enumerate the underlying database directly — see note in Finding 1.

---

## 3. Findings and Proof of Exploitation

### Finding 1 — SQL Injection Authentication Bypass (Patient Login)

**Risk: Critical**

The patient login form does not sanitise or parameterise user input before using it in a backend SQL query. Submitting `admin' --` as the username, with any arbitrary string as the password, causes the database query's password check to be commented out, returning a valid authenticated session as if the credentials were correct.

> ⚠️ **Evidence gap:** No screenshot of this specific step was captured during testing. This finding is documented from direct recollection of the exploitation and should be re-verified and screenshotted (login form with payload entered, and the resulting authenticated session/file listing) before this report is treated as final, so the finding is independently verifiable.

This access was the pivot point that exposed the three patient PDF reports detailed in Finding 2.

---

### Finding 2 — Patient Pathology Reports Exposed and Cracked

**Risk: High**

Once authenticated via the bypass in Finding 1, three password-protected PDF pathology lab reports were accessible. Each PDF's password was recovered and the contents reviewed, confirming each report discloses the named patient's full identity, date of birth, referring doctor, specimen type, and lab results.

#### 2a — patient_report_1.pdf (Sipho Dlamini)

Hash extracted using the Networkwalks Hash Calculator:

![Hash extracted from patient_report_1.pdf](screenshots/f2a-hash-extract.png)

Password recovered via the Networkwalks Password Cracker dictionary attack:

![Password cracked: 123456](screenshots/f2a-cracked.png)

Report contents after unlocking:

![Sipho Dlamini pathology report](screenshots/f2a-content.png)

*Elevated white cell count flagged.*

#### 2b — patient_report_2.pdf (Priya Reddy)

Hash extracted:

![Hash extracted from patient_report_2.pdf](screenshots/f2b-hash-extract.png)

Password recovered:

![Password cracked: password](screenshots/f2b-cracked.png)

Report contents after unlocking:

![Priya Reddy pathology report](screenshots/f2b-content.png)

*Elevated cholesterol, LDL, and triglycerides flagged.*

#### 2c — Third encrypted PDF (Emily Thompson)

The third PDF's password was not present in the Networkwalks Password Cracker's built-in 100-word list. A self-written Python script (`crack.py`), using the `pypdf` library, was used to perform an offline dictionary attack against the RockYou wordlist instead:

![crack.py — custom PDF password cracker](screenshots/f2c-script.png)

Password recovered after approximately 72,000 attempts against `rockyou.txt`:

![Password cracked: !@#$%^&](screenshots/f2c-cracked.png)

Report contents after unlocking:

![Emily Thompson pathology report](screenshots/f2c-content.png)

*Low haemoglobin, ferritin, and vitamin D flagged.*

---

### Finding 3 — Exposed Legacy Backup Directory Discloses Full Staff & Shareholder Database

**Risk: Critical**

Appending `/old/` to the site's base URL revealed a legacy backup directory that had not been removed from production. It contained `mediroza_db_backup_2019.sql`, a full MySQL dump. **This finding is independent of Finding 1** — no SQL injection or authentication bypass was needed to reach it, only a guessed path.

The dump includes two tables of concern:

- **`staff`** — 30 records, including full name, job title, department, email, phone number, South African national ID number, monthly salary (ZAR), and date joined, for every member of staff from the Chief Pathologist and CFO down to Ward Clerk.
- **`shareholders`** — 10 records, including shareholder name, ownership percentage, shares held, and share class — disclosing that several named clinicians and executives (including the Chief Pathologist and Medical Director) hold personal equity stakes in the hospital.

![mediroza_db_backup_2019.sql showing staff and shareholder tables](screenshots/f3-db-backup.png)

This is the most severe finding in this report. It combines personally identifiable information (national ID numbers), sensitive financial data (salaries, equity), and corporate ownership information, all reachable by an unauthenticated attacker with no special tooling.

---

## 4. Risk Rating

| Finding | Risk | Justification |
|---|---|---|
| F1 — SQLi Auth Bypass | **Critical** | Unauthenticated, requires no special tooling, grants full access-control bypass on the patient portal, and is the entry point for Finding 2. |
| F2 — Patient PDF Reports | **High** | Discloses patient PII and clinical results for 3 named individuals. Rated below Critical only because it requires Finding 1 as a prerequisite; the weak PDF passwords made the second stage trivial once inside. |
| F3 — Exposed DB Backup | **Critical** | No authentication or exploitation skill required — a guessable path. Discloses national ID numbers, salaries, and equity holdings for 40 individuals, including sensitive HR and corporate ownership data. Independently discoverable by any attacker or search engine crawler. |

---

## 5. Recommendations and Remediation

### For Finding 1 (SQL Injection)
- Rewrite all database queries to use parameterised statements / prepared statements, or a vetted ORM, so user input is never concatenated directly into SQL.
- Apply a Web Application Firewall (WAF) rule set as a defense-in-depth layer against common injection payloads — this should not replace the fix above, only supplement it.
- Add server-side logging and alerting for failed login attempts containing SQL metacharacters, to detect future attempts.

### For Finding 2 (Patient PDF Reports)
- Do not rely on document-level passwords as the real access control for patient data. Enforce authorisation at the application layer, so even an authenticated session can only retrieve records belonging to that specific user.
- If PDF passwords are used at all, enforce a minimum complexity policy — the passwords recovered here (`123456`, `password`) offered no real protection.
- Review whether patient reports need to be stored as downloadable files at all, versus rendered on-demand behind proper per-record authorisation checks.

### For Finding 3 (Exposed Backup Directory)
- Remove the `/old/` directory and any other legacy or backup paths from the production web root immediately.
- Introduce a deployment checklist or automated pipeline check that prevents backup files, legacy directories, and `.sql` dumps from ever being pushed into a publicly served directory.
- Store genuine backups off-server, in a location with its own access controls (e.g. a private storage bucket with restricted IAM), never inside the web root.
- Encrypt sensitive fields such as national ID numbers at rest, and avoid producing full plaintext database exports as routine practice.
- Audit who currently has or has had access to this and any other backup files, given the exposure window is unknown.

### General
- Conduct a full internal review of all legacy/unused paths on the production server (common patterns: `/old/`, `/backup/`, `/test/`, `/.git/`, `/.env`) as a one-off sweep in addition to the pipeline fix above.
- Given the overlap between Findings 1–3, consider a follow-up engagement scoped to authenticated/internal testing once these fixes are deployed, to check for further issues not reachable from this black-box test.
