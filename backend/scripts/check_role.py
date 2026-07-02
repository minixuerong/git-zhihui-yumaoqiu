from dotenv import load_dotenv; load_dotenv()
import os
from sqlalchemy import create_engine, text
e = create_engine(os.getenv('DATABASE_URL'))
r = e.execute(text("SHOW COLUMNS FROM users WHERE Field = 'role'"))
print('Type:', r.fetchone()[1])
