FROM python:3.12-slim

WORKDIR /app

# 安装 MySQL 客户端（用于等待 MySQL 就绪）
RUN apt-get update && apt-get install -y --no-install-recommends \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# 先复制依赖文件，利用缓存
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 启动脚本：等待 MySQL 就绪 → 启动 uvicorn
RUN printf '#!/bin/sh\n\
echo "Waiting for MySQL at $MYSQL_HOST:$MYSQL_PORT..."\n\
while ! mysqladmin ping -h "$MYSQL_HOST" -P "$MYSQL_PORT" --silent 2>/dev/null; do\n\
  sleep 2\n\
done\n\
echo "MySQL is ready!"\n\
exec uvicorn app.main:app --host 0.0.0.0 --port 8000\n' > /start.sh && chmod +x /start.sh

EXPOSE 8000

CMD ["/start.sh"]
