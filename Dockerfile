FROM python:3.9-slim
WORKDIR /app
COPY . .
# MYSQL 관련 시스템 패키지 업데이트 및 필요한 패키지 설치
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    gcc
RUN pip install -r requirements.txt