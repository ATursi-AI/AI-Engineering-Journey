# Defining our reusable tool
def analyze_score(score):
    if score > 0.90:
        return "EXCELLENT"
    elif score > 0.70:
        return "GOOD"
    else:
        return "RE-TRAIN NEEDED"
    
    # *Using the tool (Calling the function)
result1 = analyze_score(0.95)
result2 = analyze_score(0.42)

print(f"Model A is {result1}")
print(f"Model B is {result2}")