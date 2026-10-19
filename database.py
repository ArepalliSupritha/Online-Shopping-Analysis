
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "shopping_data.csv"
DB_DIR = BASE_DIR / "database"
DB_FILE = DB_DIR / "shopping.db"


def create_database():
    DB_DIR.mkdir(exist_ok=True)

    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "Dataset not found. Run python generate_data.py first."
        )

    df = pd.read_csv(DATA_FILE)

    with sqlite3.connect(DB_FILE) as connection:
        df.to_sql("orders", connection, if_exists="replace", index=False)

    print("Database created successfully!")


def load_data():
    if not DB_FILE.exists():
        create_database()

    with sqlite3.connect(DB_FILE) as connection:
        return pd.read_sql_query("SELECT * FROM orders", connection)


if __name__ == "__main__":
    create_database()