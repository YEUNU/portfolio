# 1. Python 베이스 이미지 선택
FROM python:3.13-slim

# 2. 작업 디렉터리 설정
WORKDIR /app

# 3. 의존성 파일 복사 및 설치
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# 4. 소스코드 복사
COPY ./app /app/app

# 5. uvicorn 서버 실행
# 0.0.0.0으로 바인딩하여 컨테이너 외부에서 접근 가능하게 함
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
