# A list of confidence scores from an AI model
scores = [0.85, 0.92, 0.45, 0.78, 0.99]

print("Scanning AI Confidence Scores...")

for s in scores:
    if s > 0.80:
        print(f"Score {s}: HIGH CONFIDENCE")
    else:
        print(f"Score {s}: LOW CONFIDENCE - Requires Human Review")
        
print("Scan Complete")

           