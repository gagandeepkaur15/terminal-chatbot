# app/config.py

import os

from dotenv import load_dotenv

from groq import Groq

load_dotenv()

# =======================================
# API
# =======================================

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL",
    "llama-3.3-70b-versatile"
)

client = Groq(
    api_key=GROQ_API_KEY
)

# =======================================
# Pricing
# =======================================

INPUT_COST_PER_MILLION = float(
    os.getenv(
        "INPUT_COST_PER_MILLION",
        0
    )
)

OUTPUT_COST_PER_MILLION = float(
    os.getenv(
        "OUTPUT_COST_PER_MILLION",
        0
    )
)

# =======================================
# Memory
# =======================================

WINDOW_SIZE = 12

SUMMARY_TRIGGER = 30

# =======================================
# Database
# =======================================

DATABASE_PATH = "data/chat.db"