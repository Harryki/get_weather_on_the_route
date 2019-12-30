from dotenv import load_dotenv
import os

load_dotenv()

GOOGLE_DIRECTION_API_KEY = os.getenv("GOOGLE_DIRECTION_API_KEY")
HERE_API = os.getenv("HERE_API")

