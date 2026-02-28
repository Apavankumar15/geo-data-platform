import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "..", "outputs")

STAC_URL = "https://planetarycomputer.microsoft.com/api/stac/v1"

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

