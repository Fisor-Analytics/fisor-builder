# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")
