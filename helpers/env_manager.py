import os


def delete_env_file_at_exit():
    from dotenv import load_dotenv, set_key
    # Load .env file (or create one if missing)
    DOTENV_PATH = os.path.join(os.getcwd(), ".env")
    """Deletes the entire .env file when the script finishes."""
    print(f"\nRunning atexit cleanup: Attempting to delete {DOTENV_PATH}")
    if os.path.exists(DOTENV_PATH):
        try:
            os.remove(DOTENV_PATH)
            print(f"Successfully deleted {DOTENV_PATH}")
        except OSError as e:
            print(f"Error deleting file {DOTENV_PATH}: {e.strerror}")
    else:
        print(f"{DOTENV_PATH} not found, nothing to delete.")
