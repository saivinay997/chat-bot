import os
from dotenv import load_dotenv, set_key
from pathlib import Path

def load_env_vars():
    """Load environment variables from .env file"""
    load_dotenv()

def save_to_env(key, value):
    """Save a key-value pair to .env file"""
    env_path = Path('.env')
    if not env_path.exists():
        env_path.touch()
    set_key(env_path, key, value)
    os.environ[key] = value
