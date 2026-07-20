"""
Password Complexity Checker
Prodigy InfoTech Internship Task-03

A GUI tool (built with Tkinter) that evaluates password strength based on:
- Length
- Uppercase letters
- Lowercase letters
- Numbers
- Special characters

It gives live feedback and a strength score/bar as the user types.
"""

import re
import tkinter as tk
from tkinter import ttk


# ---------------------------------------------------------------------------
# Core logic: analyze a password and return score + feedback
# ---------------------------------------------------------------------------
def analyze_password(password: str):
    """
    Returns a dict with:
        score        -> int (0 to 5)
        checks       -> dict of rule_name: bool
        strength     -> str label ("Very Weak" ... "Very Strong")
        suggestions  -> list of missing-criteria messages
    """
    checks = {
        "Length (8+ characters)": len(password) >= 8,
        "Uppercase letter (A-Z)": bool(re.search(r"[A-Z]", password)),
        "Lowercase letter (a-z)": bool(re.search(r"[a-z]", password)),
        "Number (0-9)": bool(re.search(r"[0-9]", password)),
        "Special character (!@#$...)": bool(re.search(r"[^A-Za-z0-9]", password)),
    }

    # Bonus point for longer passwords (12+), on top of the 5 base checks
    score = sum(checks.values())
    if len(password) >= 12 and score == 5:
        score = 6  # cap handled below

    max_score = 6
    score = min(score, max_score)

    if len(password) == 0:
        strength = "No Password"
    elif score <= 1:
        strength = "Very Weak"
    elif score == 2:
        strength = "Weak"
    elif score == 3:
        strength = "Moderate"
    elif score == 4:
        strength = "Strong"
    else:
        strength = "Very Strong"

    suggestions = [name for name, passed in checks.items() if not passed]

    return {
        "score": score,
        "max_score": max_score,
        "checks": checks,
        "strength": strength,
        "suggestions": suggestions,
    }


# ---------------------------------------------------------------------------
# GUI
# ---------------------------------------------------------------------------
class PasswordCheckerApp(tk.Tk):
    STRENGTH_COLORS = {
        "No Password": "#888888",
        "Very Weak": "#e74c3c",
        "Weak": "#e67e22",
        "Moderate": "#f1c40f",
        "Strong": "#2ecc71",
        "Very Strong": "#27ae60",
    }

    def __init__(self):
        super().__init__()
        self.title("Password Complexity Checker")
        self.geometry("440x480")
        self.resizable(False, False)
        self.configure(bg="#1e1e2f")

        self._build_widgets()

    def _build_widgets(self):
        title = tk.Label(
            self,
            text="🔒 Password Complexity Checker",
            font=("Segoe UI", 16, "bold"),
            bg="#1e1e2f",
            fg="white",
        )
        title.pack(pady=(20, 10))

        # --- Password entry frame ---
        entry_frame = tk.Frame(self, bg="#1e1e2f")
        entry_frame.pack(pady=5)

        self.show_password = tk.BooleanVar(value=False)

        self.password_var = tk.StringVar()
        self.password_var.trace_add("write", self._on_password_change)

        self.entry = tk.Entry(
            entry_frame,
            textvariable=self.password_var,
            font=("Segoe UI", 13),
            width=26,
            show="*",
            relief="flat",
            bg="#2c2c40",
            fg="white",
            insertbackground="white",
        )
        self.entry.pack(side="left", ipady=6, padx=(0, 8))

        toggle_btn = ttk.Checkbutton(
            entry_frame,
            text="Show",
            variable=self.show_password,
            command=self._toggle_visibility,
        )
        toggle_btn.pack(side="left")

        # --- Strength label ---
        self.strength_label = tk.Label(
            self,
            text="Strength: —",
            font=("Segoe UI", 12, "bold"),
            bg="#1e1e2f",
            fg="white",
        )
        self.strength_label.pack(pady=(15, 5))

        # --- Progress bar ---
        style = ttk.Style(self)
        style.theme_use("default")
        style.configure(
            "Strength.Horizontal.TProgressbar",
            troughcolor="#2c2c40",
            background="#2ecc71",
            thickness=18,
        )
        self.progress = ttk.Progressbar(
            self,
            style="Strength.Horizontal.TProgressbar",
            orient="horizontal",
            length=380,
            mode="determinate",
            maximum=6,
        )
        self.progress.pack(pady=(0, 15))

        # --- Checklist ---
        checklist_frame = tk.Frame(self, bg="#1e1e2f")
        checklist_frame.pack(fill="x", padx=30)

        self.check_labels = {}
        rules = [
            "Length (8+ characters)",
            "Uppercase letter (A-Z)",
            "Lowercase letter (a-z)",
            "Number (0-9)",
            "Special character (!@#$...)",
        ]
        for rule in rules:
            lbl = tk.Label(
                checklist_frame,
                text=f"✗  {rule}",
                font=("Segoe UI", 10),
                bg="#1e1e2f",
                fg="#e74c3c",
                anchor="w",
            )
            lbl.pack(fill="x", pady=2)
            self.check_labels[rule] = lbl

        # --- Suggestions box ---
        self.feedback_label = tk.Label(
            self,
            text="Start typing a password to see feedback.",
            font=("Segoe UI", 9, "italic"),
            bg="#1e1e2f",
            fg="#aaaaaa",
            wraplength=380,
            justify="left",
        )
        self.feedback_label.pack(pady=(15, 0), padx=30, anchor="w")

    def _toggle_visibility(self):
        self.entry.config(show="" if self.show_password.get() else "*")

    def _on_password_change(self, *args):
        password = self.password_var.get()
        result = analyze_password(password)

        # Update strength label + color
        color = self.STRENGTH_COLORS[result["strength"]]
        self.strength_label.config(text=f"Strength: {result['strength']}", fg=color)

        # Update progress bar
        style = ttk.Style(self)
        style.configure("Strength.Horizontal.TProgressbar", background=color)
        self.progress["value"] = result["score"]

        # Update checklist
        for rule, passed in result["checks"].items():
            lbl = self.check_labels[rule]
            if passed:
                lbl.config(text=f"✓  {rule}", fg="#2ecc71")
            else:
                lbl.config(text=f"✗  {rule}", fg="#e74c3c")

        # Update suggestions
        if not password:
            self.feedback_label.config(text="Start typing a password to see feedback.")
        elif result["suggestions"]:
            tips = ", ".join(result["suggestions"])
            self.feedback_label.config(text=f"To improve, add: {tips}.")
        else:
            self.feedback_label.config(text="Great job! This is a strong password.")


if __name__ == "__main__":
    app = PasswordCheckerApp()
    app.mainloop()
