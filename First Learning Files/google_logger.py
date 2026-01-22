import logging

#1. Setup the Logger to write to a file named 'system.log'
logging.basicConfig(
    filename='system.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def start_ai_service():
    """Simulates starting a Google AI service."""
    print("Check your folder after running this...")
    logging.info("AI Service started successfully.")
    
try:
    # Simulate a fake error
    x = 1 / 0
except ZeroDivisionError:
    logging.error("AI Service failed: Division by zero encountered.")

start_ai_service()
