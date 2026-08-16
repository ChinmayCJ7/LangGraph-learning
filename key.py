from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise EnvironmentError("GOOGLE_API_KEY not set. Add it to your .env file.")