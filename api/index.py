import sys
import os
from pathlib import Path

# Get the absolute path to backend directory
current_dir = Path(__file__).resolve().parent
backend_path = current_dir.parent / 'backend'
sys.path.insert(0, str(backend_path))

# Change working directory to backend for relative imports
os.chdir(str(backend_path))

# Import the Flask app
from app import app

# Vercel serverless handler
def handler(request, context):
    return app(request, context)

# Export for Vercel
app = app
