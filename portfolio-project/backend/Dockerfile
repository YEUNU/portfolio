# 1. Python 베이스 이미지 선택
FROM python:3.13-slim

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Playwright requires some OS libraries - install them and then install Chromium
RUN apt-get update && apt-get install -y \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdbus-1-3 \
    libdrm2 \
    libgbm1 \
    libgtk-3-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    --no-install-recommends && rm -rf /var/lib/apt/lists/* \
  && python -m playwright install --with-deps chromium

# 4. 소스코드 복사
COPY ./app /app/app

# 5. uvicorn 서버 실행
# 0.0.0.0으로 바인딩하여 컨테이너 외부에서 접근 가능하게 함
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
