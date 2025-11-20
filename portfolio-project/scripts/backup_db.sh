#!/bin/bash

################################################################################
# PostgreSQL Database Backup Script
# 
# 이 스크립트는 Docker Compose로 실행 중인 PostgreSQL DB를 백업합니다.
# pg_dump를 사용하여 논리 백업(custom format)을 생성합니다.
#
# 사용법:
#   ./scripts/backup_db.sh
#
# 백업 파일 위치: ./backups/
# 백업 파일명 형식: portfolio_db_YYYY-MM-DD_HHMM.dump
################################################################################

set -e  # 오류 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 프로젝트 루트 디렉토리로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo -e "${GREEN}=== PostgreSQL Database Backup ===${NC}"
echo "프로젝트 경로: $PROJECT_DIR"

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env 파일을 찾을 수 없습니다.${NC}"
    exit 1
fi

# 환경 변수 로드
source .env

# 백업 디렉토리 생성
BACKUP_DIR="$PROJECT_DIR/backups"
mkdir -p "$BACKUP_DIR"

# 백업 파일명 생성 (타임스탬프 포함)
TIMESTAMP=$(date +%Y-%m-%d_%H%M)
BACKUP_FILE="portfolio_db_${TIMESTAMP}.dump"
TEMP_BACKUP_PATH="/tmp/$BACKUP_FILE"

echo "백업 대상 DB: $POSTGRES_DB"
echo "백업 파일명: $BACKUP_FILE"

# DB 컨테이너 확인
DB_CONTAINER=$(docker-compose ps -q db 2>/dev/null || docker compose ps -q db 2>/dev/null)

if [ -z "$DB_CONTAINER" ]; then
    echo -e "${RED}❌ DB 컨테이너가 실행 중이지 않습니다.${NC}"
    echo "다음 명령으로 컨테이너를 시작하세요: docker-compose up -d db"
    exit 1
fi

echo -e "${YELLOW}백업 중...${NC}"

# pg_dump 실행 (컨테이너 내부)
if docker-compose exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c -b -v -f "$TEMP_BACKUP_PATH" 2>/dev/null; then
    :
elif docker compose exec -T db pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c -b -v -f "$TEMP_BACKUP_PATH" 2>/dev/null; then
    :
else
    echo -e "${RED}❌ pg_dump 실행 실패${NC}"
    exit 1
fi

# 컨테이너에서 호스트로 백업 파일 복사
echo "백업 파일을 호스트로 복사 중..."
docker cp "${DB_CONTAINER}:${TEMP_BACKUP_PATH}" "$BACKUP_DIR/$BACKUP_FILE"

# 컨테이너 내부 임시 파일 삭제
docker exec "$DB_CONTAINER" rm -f "$TEMP_BACKUP_PATH"

# 백업 파일 크기 확인
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)

echo -e "${GREEN}✅ 백업 완료!${NC}"
echo "백업 파일: $BACKUP_DIR/$BACKUP_FILE"
echo "파일 크기: $BACKUP_SIZE"

# 오래된 백업 파일 정리 (선택사항: 7일 이상 된 파일 삭제)
echo ""
echo "오래된 백업 파일 정리 중 (7일 이상)..."
find "$BACKUP_DIR" -name "portfolio_db_*.dump" -type f -mtime +7 -delete 2>/dev/null || true

# 현재 백업 파일 목록 표시
echo ""
echo "현재 백업 파일 목록:"
ls -lh "$BACKUP_DIR"/portfolio_db_*.dump 2>/dev/null || echo "백업 파일이 없습니다."

echo ""
echo -e "${GREEN}백업이 성공적으로 완료되었습니다.${NC}"
