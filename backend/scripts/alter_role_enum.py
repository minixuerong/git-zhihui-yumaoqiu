"""修改 users 表的 role 字段，添加 'hr' 枚举值"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from sqlalchemy import create_engine, text

DATABASE_URL = os.getenv("DATABASE_URL", "")
if not DATABASE_URL:
    print("❌ DATABASE_URL 未设置")
    sys.exit(1)

engine = create_engine(DATABASE_URL)
with engine.begin() as conn:
    result = conn.execute(text("SHOW COLUMNS FROM users WHERE Field = 'role'"))
    row = result.fetchone()
    if row:
        current_type = row[1]
        if "'hr'" not in current_type:
            conn.execute(text("ALTER TABLE users MODIFY COLUMN role ENUM('admin','user','hr') NOT NULL DEFAULT 'user'"))
            print("✅ role 字段已添加 'hr' 枚举值")
        else:
            print("✅ role 字段已包含 'hr'，无需修改")
    else:
        print("❌ 未找到 role 字段")
        sys.exit(1)
