# 베이스 이미지로 Python 3 기반 이미지 선택
FROM python:3.11

# 환경 변수 설정
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사(로컬에서 Docker 컨테이너 내부로)
COPY portfolio .
# gunicorn을 사용하여 Django 애플리케이션 실행 명령
CMD ["python", "manage.py", "runserver", "0.0.0.0:8993"]
