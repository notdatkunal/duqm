import os
import subprocess
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

pg_server = None

def init_or_get_pgserver(base_path: str = r"C:\pg_data")->str:
    """
    Ensures a PostgreSQL server is available at the specified path.
    Automatically initializes one if it doesn't exist.
    Compatible with pgserver 0.x and 1.x structures.
    """
    global pg_server
    from dotenv import load_dotenv, set_key
    # Load .env file (or create one if missing)
    env_path = os.path.join(os.getcwd(), ".env")
    if base_path == r"C:\pg_data":
        load_dotenv(env_path)

        # Step 1: If URI already exists in .env → reuse it
        env_uri = os.getenv("POSTGRES_URI")
        if env_uri:
            print("[INFO] Loaded PostgreSQL URI from .env.")
            return env_uri

    base_path = os.path.abspath(base_path)
    print(f"[INFO] Checking for PostgreSQL data directory at: {base_path}")

    if not os.path.exists(base_path):
        print(f"[INFO] Directory does not exist. Creating: {base_path}")
        os.makedirs(base_path, exist_ok=True)

    db = None

    try:
        # Try modern style: pgserver.postgres_server.get_server()
        from pgserver.postgres_server import get_server as get_pg_server
        print("[INFO] Detected module: pgserver.postgres_server.get_server()")
        os.environ['PGHOST'] = 'localhost'
        db = get_pg_server(base_path)
    except ImportError:
        try:
            # Fallback to old style: pgserver.ensure_server() or get_server()
            from pgserver import get_server
            print("[INFO] Detected module: pgserver.get_server()")
            os.environ['PGHOST'] = 'localhost'
            db = get_server(base_path)
        except ImportError:
            print("[ERROR] pgserver installation is invalid or incomplete.")
            sys.exit(1)
    except Exception as e:
        print(f"[ERROR] Failed to start PostgreSQL server: {e}")
        sys.exit(1)

    pg_server = db

    try:
        import main
        main.pg_server = pg_server
    except ImportError:
        pass

    # Fetch database URI
    db_uri = db.get_uri()
    if db_uri.startswith("postgresql://"):
        db_uri = db_uri.replace("postgresql://", "postgresql+pg8000://", 1)

    print(f"[INFO] PostgreSQL URI: {db_uri}")
    # Step 3: Save to .env for persistence
    set_key(env_path, "POSTGRES_URI", db_uri)
    print(f"[INFO] Saved PostgreSQL URI to .env → {env_path}")
    return db_uri


def test_pg_connection(uri: str):
    """
    Test connection to PostgreSQL using SQLAlchemy.
    """
    print("[INFO] Testing PostgreSQL connection...")
    engine = create_engine(uri, echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        result = session.execute(text("SELECT 1")).fetchall()
        print("[SUCCESS] Connection test result:", result)
    except Exception as e:
        print("[ERROR] Database connection failed:", e)
    finally:
        session.close()
        engine.dispose()


