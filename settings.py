# from dotenv import load_dotenv
import os

# USE BELOW LINES FOR LOCAL MACHINE
# load_dotenv()
# GOOGLE_DIRECTION_API_KEY = os.getenv("GOOGLE_DIRECTION_API_KEY")
# HERE_API = os.getenv("HERE_API")

# USE BELOW LINES FOR Google Cloud Function
GOOGLE_DIRECTION_API_KEY = os.environ.get("GOOGLE_DIRECTION_API_KEY")
HERE_API = os.environ.get("HERE_API")

