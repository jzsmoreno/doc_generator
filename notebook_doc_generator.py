import signal
import sys

from core.main import cancel_generation, process_notebooks
from openai import OpenAI


def signal_handler(signum, frame):
    """Handle Ctrl+C signal to gracefully cancel generation."""
    print("\n\nCtrl+C detected! Requesting cancellation...")
    cancel_generation()
    print("Please wait for current task to finish...")


# Register signal handler
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


# Example API call setup (replace with your actual API URL and key if needed)
api_url = "http://127.0.0.1:1234/v1"
client = OpenAI(base_url=api_url, api_key="lm-studio")
model = "gemma-3-4b-it"

# Running the program
process_notebooks(client, model, "notebooks")
