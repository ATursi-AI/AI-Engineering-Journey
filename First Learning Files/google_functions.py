# We define a function to calculate a "Performance Score"
# 'base_score' must be a float (decimal)
# 'bonus' must be an integer (whole number)
# The '-> float' means the results will be a decimaL
def calculate_ai_readiness(base_score: float, bonus: int) -> float:
    """Calculates the final readiness score for a candidate,"""
    final_score = base_score + (bonus / 100)
    return final_score

# Now we use the function
my_score = calculate_ai_readiness(0.85, 10)

print(f"Final AI Readiness Score: {my_score}")
