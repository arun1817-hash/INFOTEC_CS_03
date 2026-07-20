# INFOTEC_CS_03
Here's the description of this task:  Task-03: Password Complexity Checker  Build a tool that assesses the strength of a password based on criteria such as length, presence of uppercase and lowercase letters, numbers, and special characters. Provide feedback to users on the password's strength.

Description:

Build a tool that assesses the strength of a password based on criteria such as length, presence of uppercase and lowercase letters, numbers, and special characters. Provide feedback to users on the password's strength.

Features — Password Complexity Checker:

Real-time password strength checking based on multiple criteria
Checks 5 core criteria:
Minimum length (e.g., 8+ characters)
Presence of uppercase letters (A–Z)
Presence of lowercase letters (a–z)
Presence of numbers (0–9)
Presence of special characters (!@#$%^&* etc.)
Scoring system — each satisfied criterion adds a point to the overall strength score
Strength classification — categorizes password as:
Weak (few criteria met)
Medium (some criteria met)
Strong (most/all criteria met)
Detailed feedback messages — tells the user exactly what's missing (e.g., "Add a special character", "Password too short", "Include an uppercase letter") instead of just showing a score
Optional advanced checks (extra credit):
Detects common/weak passwords (password123, qwerty, etc.)
Flags repeated characters (aaaa)
Flags sequential patterns (1234, abcd)
Two interface options:
Command-line version — quick and simple
GUI version (Tkinter) — live strength meter/progress bar as the user types
No external dependencies needed — can be built using only Python's built-in re module

How It Works:

Step 1: Take input — user types a password (terminal or GUI text box)
Step 2: Check against each rule using regex (re module):
Length — at least 8 characters: len(password) >= 8
Uppercase — contains A–Z: re.search(r'[A-Z]', password)
Lowercase — contains a–z: re.search(r'[a-z]', password)
Digit — contains 0–9: re.search(r'[0-9]', password)
Special character — contains symbols: re.search(r'[!@#$%^&*(),.?":{}|<>]', password)
Step 3: Score the password — each passed rule adds +1 point (max score = 5)
Step 4: Classify strength based on score:
0–2 → Weak
3–4 → Medium
5 → Strong
Step 5: Give feedback on what's missing — loops through failed checks and tells user exactly what to fix (e.g., "Add an uppercase letter", "Add a special character")
Step 6: Display result
CLI mode → prints strength label + feedback list
GUI mode → live strength meter/progress bar that updates as the user types

Code Explanation :

import re — used for pattern matching (checking for uppercase, lowercase, digits, special characters)
CRITERIA list — holds all 5 checks as tuples: (key, description, test_function)
Each test function is a small lambda that returns True/False for a password
Keeping checks in a list (instead of separate if-statements) makes it easy to add/remove rules later
COMMON_WEAK_PASSWORDS set — a list of well-known weak passwords to flag as extra feedback
check_password(password) — loops through CRITERIA and runs each test function, returns a dictionary like {"length": True, "uppercase": False, ...}
get_score(results) — counts how many values in the results dict are True (i.e., how many rules passed)
get_strength_label(score) — converts the numeric score into Weak / Medium / Strong using score thresholds (≤40% = Weak, ≤80% = Medium, else Strong)
get_feedback(password, results) — builds a list of messages:
For every failed criterion, adds a "Missing: ..." message
Also checks for common weak passwords and repeated characters (re.search(r'(.)\1{2,}', password) catches things like "aaa")
If nothing failed, shows a "Great password!" message
analyze_password(password) — the main function that ties everything together and returns one combined report (results, score, label, feedback)
run_cli() — infinite loop that asks for a password, calls analyze_password(), and prints the strength + feedback with right/wrong markers
run_gui() → PasswordCheckerApp class
password_var.trace_add(...) — automatically calls update_ui() every time the user types a character (live feedback, no submit button needed)
update_ui() — re-runs analyze_password(), updates the progress bar (ttk.Progressbar) and color-coded strength label, and rebuilds the feedback message list
toggle_visibility() — lets the user show/hide the password text via a checkbox
Entry point — python password_complexity_checker.py --cli runs CLI mode; running with no arguments opens the GUI

Technology Used:

Python 3 — the core programming language used to build the entire tool
re (Regular Expressions) — Python's built-in module used to check for:
Uppercase letters ([A-Z])
Lowercase letters ([a-z])
Digits ([0-9])
Special characters ([!@#$%^&*...])
Repeated character patterns ((.)\1{2,})
Tkinter — Python's built-in GUI toolkit, used for:
The password entry box
ttk.Progressbar — the live strength meter
Color-coded strength label (red/orange/green)
"Show password" checkbox
Live feedback list that updates as you type (via StringVar().trace_add())
sys — used to detect command-line arguments and decide whether to launch CLI mode or GUI mode

How to Run :

No installation needed — uses only Python's built-in libraries (re, tkinter, sys)
Note (Linux only): if Tkinter isn't installed, run:
  sudo apt-get install python3-tk
Run in GUI mode (default, no arguments):
  python password_complexity_checker.py
Type password into the box
Strength meter + feedback update live as you type
"Show password" checkbox reveals the text
Run in CLI mode (terminal-based):
  python password_complexity_checker.py --cli
Type a password, press Enter
Strength label + feedback printed instantly
Loops for repeated checks; Ctrl+C to exit
Requirements: Python 3.6+ (Tkinter and re are pre-installed with standard Python)


Example Usage

Example 1 — Weak password

Enter password: abc

Strength: Weak  (1/5 checks passed)
   Missing: At least 8 characters
   Missing: Contains an uppercase letter
   Missing: Contains a number
   Missing: Contains a special character (!@#$%^&* etc.

Example 2 — Medium password

Enter password: password123

Strength: Medium  (3/5 checks passed)
   Missing: Contains an uppercase letter
   Missing: Contains a special character (!@#$%^&* etc.)
   This is a very common password - avoid it

   Example 4 — Strong password

Enter password: Str0ng!Pass

Strength: Strong  (5/5 checks passed)
  Great password! All checks passed
