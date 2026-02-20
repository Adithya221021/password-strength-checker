import re

def check_password(password):

    score = 0
    feedback = []

    # Length
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Minimum 8 characters required")

    # Uppercase
    if re.search(r"[A-Z]", password):
        score += 1
    else:
        feedback.append("Add uppercase letter")

    # Lowercase
    if re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("Add lowercase letter")

    # Number
    if re.search(r"[0-9]", password):
        score += 1
    else:
        feedback.append("Add at least one digit")

    # Special char
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("Add special character")

    # Common password check
    with open("common_passwords.txt") as f:
        common = f.read().splitlines()

    if password.lower() in common:
        return {
            "strength": "WEAK",
            "score": 0,
            "feedback": ["Very common password"]
        }

    # Final result
    if score == 5:
        strength = "STRONG"
    elif score >= 3:
        strength = "MEDIUM"
    else:
        strength = "WEAK"

    return {
        "strength": strength,
        "score": score,
        "feedback": feedback
    }
