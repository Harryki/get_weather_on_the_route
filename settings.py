# from dotenv import load_dotenv
import os

# load_dotenv()
# GOOGLE_DIRECTION_API_KEY = os.getenv("GOOGLE_DIRECTION_API_KEY")
# HERE_API = os.getenv("HERE_API")

# google cloud function
GOOGLE_DIRECTION_API_KEY = os.environ.get("GOOGLE_DIRECTION_API_KEY")
HERE_API = os.environ.get("HERE_API")

