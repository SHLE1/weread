FROM --platform=$BUILDPLATFORM python:3.9-slim

WORKDIR /app

ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码和配置
COPY config_manager.py .
COPY main.py .
COPY push.py .

# 设置环境变量默认值
ENV READ_COUNT=200
ENV PUSH_METHOD=none
ENV PUSHPLUS_TOKEN=""
ENV TG_BOT_TOKEN=""
ENV TG_CHAT_ID=""
ENV CONFIG_PATH=/app/config.json

CMD ["python", "main.py"]