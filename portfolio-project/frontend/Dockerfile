# --- 1단계: 빌드 환경 ---
# Node.js 이미지를 기반으로 빌드 환경을 설정합니다.
FROM node:16-alpine as build-stage

WORKDIR /app

# package.json과 package-lock.json을 먼저 복사하여 의존성을 캐싱합니다.
COPY package*.json ./
RUN npm install

# 소스코드 전체를 복사합니다.
COPY . .

# 프로덕션용으로 애플리케이션을 빌드합니다.
RUN npm run build


# --- 2단계: 프로덕션 환경 ---
# 경량 Nginx 이미지를 기반으로 최종 이미지를 생성합니다.
FROM nginx:stable-alpine as production-stage

# 빌드 단계에서 생성된 정적 파일들을 Nginx의 기본 서빙 디렉터리로 복사합니다.
COPY --from=build-stage /app/dist /usr/share/nginx/html

# SPA(Single Page Application) 라우팅을 처리하기 위한 커스텀 Nginx 설정을 복사합니다.
# 이 설정이 있어야 /post/1과 같은 경로에서 404 에러가 발생하지 않습니다.
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Nginx 컨테이너가 80번 포트를 노출하도록 설정합니다.
EXPOSE 80

# Nginx 서버를 실행합니다.
CMD ["nginx", "-g", "daemon off;"]
