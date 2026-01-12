# The AI Gatekeeper with a Safety Net
print("--- AI Security System ---")

try:
    # We "try" to run this code
    age_input = input("Please enter your age: ")
    age = int(age_input)

    if age >= 18:
        print("Access Granted.")
    else:   
        print("Access Denied.")
    
except ValueError:
    # If the user types a word instead of a number, we "catch" the error here
    print("Error: Please enter age usingnumbers only (e.g., 25).")

print("System check complete.")
    

