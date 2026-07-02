FROM python:3.12-slim

WORKDIR /app

# 先复制依赖文件，利用缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 启动脚本：用 Python 检测 MySQL 就绪 → 启动 uvicorn
RUN printf '#!/usr/bin/python3\n\
import mysql.connector, os, time, sys\n\
host = os.getenv("MYSQL_HOST", "localhost")\n\
port = int(os.getenv("MYSQL_PORT", 3306))\n\
print(f"Waiting for MySQL at {host}:{port}...")\n\
while True:\n\
    try:\n\
        mysql.connector.connect(host=host, port=port, user="root", password=os.getenv("MYSQL_ROOT_PASSWORD", "root123"), database="capability_graph")\n\
        break\n\
    except Exception:\n\
        time.sleep(2)\n\
print("MySQL is ready!")\n\
os.execvp("uvicorn", ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"])\n' > /wait.py && \
sed -i 's/^import/#!\/usr\/bin\/python3\nimport/' /wait.py && \
chmod +x /wait.py

EXPOSE 8000

CMD ["python3", "/wait.py"]
