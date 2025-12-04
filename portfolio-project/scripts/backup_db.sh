#!/bin/bash

################################################################################
# PostgreSQL Database Backup Script
# 
# Docker Compose PostgreSQL 데이터베이스 백업 스크립트
# pg_dump custom format으로 백업 파일 생성
#
# ⚠️ 보안 주의사항:
# - 백업 파일은 ./backups/ 디렉토리에 저장됩니다
# - backups/ 디렉토리는 .gitignore에 포함되어 있어야 합니다
# - 백업 파일은 절대 git에 커밋하지 마세요 (민감한 데이터 포함)
#
# 사용법:
#   ./scripts/backup_db.sh
#
# 백업 위치: ./backups/portfolio_db_YYYY-MM-DD_HHMM.dump
################################################################################

set -e

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# 디렉토리 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo -e "${GREEN}=== PostgreSQL 데이터베이스 백업 ===${NC}"
echo "프로젝트: $PROJECT_DIR"

# .env 확인 및 로드
if [ ! -f ".env" ]; then
    echo -e "${RED}오류: .env 파일이 없습니다${NC}"
    exit 1
fi
source .env

# 백업 디렉토리 (반드시 .gitignore에 포함되어야 함)
BACKUP_DIR="$PROJECT_DIR/backups"
mkdir -p "$BACKUP_DIR"

# .gitignore 체크
if [ -f "$PROJECT_DIR/../.gitignore" ]; then
    if ! grep -q "backups/" "$PROJECT_DIR/../.gitignore" 2>/dev/null; then
        echo -e "${YELLOW}⚠️  경고: .gitignore에 'backups/'가 포함되어 있는지 확인하세요!${NC}"
    fi
fi

# 백업 파일명
TIMESTAMP=$(date +%Y-%m-%d_%H%M)
BACKUP_FILE="portfolio_db_${TIMESTAMP}.dump"
TEMP_PATH="/tmp/$BACKUP_FILE"

echo "데이터베이스: $POSTGRES_DB"
echo "백업 파일: $BACKUP_FILE"

# 컨테이너 확인
DB_CONTAINER=$(docker compose ps -q db 2>/dev/null || docker-compose ps -q db 2>/dev/null)
if [ -z "$DB_CONTAINER" ]; then
    echo -e "${RED}오류: DB 컨테이너가 실행 중이 아닙니다${NC}"
    exit 1
fi

# 백업 실행
echo -e "${YELLOW}백업 진행 중...${NC}"
docker exec "$DB_CONTAINER" pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -F c -b -v -f "$TEMP_PATH"

# 호스트로 복사
docker cp "${DB_CONTAINER}:${TEMP_PATH}" "$BACKUP_DIR/$BACKUP_FILE"
docker exec "$DB_CONTAINER" rm -f "$TEMP_PATH"

# 결과
BACKUP_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
echo -e "${GREEN}✅ 백업 완료${NC}"
echo "위치: $BACKUP_DIR/$BACKUP_FILE"
echo "크기: $BACKUP_SIZE"

# 7일 이상 된 백업 삭제
find "$BACKUP_DIR" -name "portfolio_db_*.dump" -type f -mtime +7 -delete 2>/dev/null || true

# 백업 목록
echo ""
echo "백업 파일 목록:"
ls -lh "$BACKUP_DIR"/portfolio_db_*.dump 2>/dev/null | tail -5 || echo "없음"

echo ""
echo -e "${GREEN}백업이 성공적으로 완료되었습니다.${NC}"
echo -e "${YELLOW}⚠️  주의: 백업 파일을 git에 커밋하지 마세요!${NC}"
