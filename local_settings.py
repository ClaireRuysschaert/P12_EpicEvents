import os
from dotenv import load_dotenv

load_dotenv()

postgresql = {
    "pguser": os.getenv('PGUSER'),
    "pgpasswd": os.getenv('PGPASSWORD'),
    "pghost": os.getenv('PGHOST'),
    "pgport": os.getenv('PGPORT'),
    "pgdb": os.getenv('PGDATABASE'),
}
