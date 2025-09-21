# --- 1단계: Vue.js 프론트엔드 빌드 ---
# Node.js 이미지를 빌드 환경으로 사용
FROM node:16-alpine as builder

WORKDIR /app

# frontend 폴더의 package.json 파일을 복사하여 의존성 설치
COPY ./frontend/package*.json ./
RUN npm install

# frontend 폴더의 나머지 소스코드 복사
COPY ./frontend/ ./

# 프로덕션용으로 애플리케이션 빌드
RUN npm run build

# --- 2단계: Nginx 프로덕션 환경 설정 ---
# 경량 Nginx 이미지를 최종 이미지로 사용
FROM nginx:stable-alpine

# 빌드 단계에서 생성된 정적 파일들을 Nginx의 기본 서빙 디렉터리로 복사
COPY --from=builder /app/dist /usr/share/nginx/html

# ✅ 수정된 부분: default.conf 파일의 경로를 정확히 지정
# 커스텀 Nginx 설정을 컨테이너로 복사
COPY ./nginx/default.conf /etc/nginx/conf.d/default.conf

# 80번 포트 노출
EXPOSE 80

# Nginx 서버 실행
CMD ["nginx", "-g", "daemon off;"]

