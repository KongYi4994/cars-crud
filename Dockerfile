# 1. 声明基础镜像（默认从 Docker Hub 拉取，本地网络慢可以用下面的代理方式）
ARG BASE_IMAGE=python:3.12-slim
FROM ${BASE_IMAGE}

# 2. 设置工作目录
WORKDIR /app

# 3. 先复制依赖文件并安装（这样可以充分利用 Docker 的缓存，只改代码时不需要重新安装依赖）
COPY requirements.txt ./
RUN python -m pip install --no-cache-dir -r requirements.txt

# 4. 复制应用代码
COPY app/ ./app/

# 5. 创建数据目录并设置权限
RUN mkdir -p /data && chown 10001:10001 /data
USER 10001:10001
ENV CARS_DB_PATH=/data/cars.db

# 6. 暴露端口
EXPOSE 8000

# 7. 启动应用
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]