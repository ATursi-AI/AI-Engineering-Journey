#1. CONSTANTS: Google says values that never change and must be ALL CAPS
# This helps engineers know "Don't touch this number!."
COMPANY_TARGET = "Google"
MINIMUM_REQUIRED_SCORE = 0.85

#2. VARIABLES: Use "snake case" (all lowercase with underscores).
# Google forbids single-letter names like 'x' or 'y' unless they are for math.
user_name = "Alex"
current_skill_level = 0.92
is_enviornment_setup = True

#3. Logic: notice the spaces around the '>=' and '='
# Google is very strict about "breathing room" in code.
if current_skill_level >= MINIMUM_REQUIRED_SCORE:
    # We use f-strings for clean text output
    status_message = f"Candidate {user_name} has surpassed the {COMPANY_TARGET} threshold."
    is_eligible_for_interview = True
else:
    status_message = f"Keep Practicing, {user_name}, You are almost there!!"
    is_eligible_for_interview = False

#4. OUTPUT
print("--- Google Hiring Assessment ---")
print(status_message)
print(f"Interview Eligibility: {is_eligible_for_interview}")


