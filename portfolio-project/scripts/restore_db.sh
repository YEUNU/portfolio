#!/bin/bash

################################################################################
# PostgreSQL Database Restore Script
# 
# 백업 파일로부터 PostgreSQL 데이터베이스 복원
#
# 사용법:
#   ./scripts/restore_db.sh                           # 최신 백업 자동 선택
#   ./scripts/restore_db.sh backup_file.dump          # 특정 파일 지정
#   ./scripts/restore_db.sh -y backup_file.dump       # 확인 없이 실행
#
# 옵션:
#   -y, --yes     확인 메시지 건너뛰기
#   -c, --clean   기존 객체 삭제 후 복원 (깨끗한 복원)
################################################################################

set -e

# 색상
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 옵션 파싱
AUTO_YES=false
CLEAN_RESTORE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -y|--yes)
            AUTO_YES=true
            shift
            ;;
        -c|--clean)
            CLEAN_RESTORE=true
            shift
            ;;
        -*)
            echo "알 수 없는 옵션: $1"
            exit 1
            ;;
        *)
            BACKUP_FILE="$1"
            shift
            ;;
    esac
done

# 디렉토리 설정
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo -e "${BLUE}=== PostgreSQL 데이터베이스 복원 ===${NC}"
echo "프로젝트: $PROJECT_DIR"

# .env 확인 및 로드
if [ ! -f ".env" ]; then
    echo -e "${RED}오류: .env 파일이 없습니다${NC}"
    exit 1
fi
source .env

BACKUP_DIR="$PROJECT_DIR/backups"

# 백업 파일 선택
if [ -z "$BACKUP_FILE" ]; then
    echo "최신 백업 파일 찾는 중..."
    
    BACKUP_FILE=$(ls -t "$BACKUP_DIR"/portfolio_db_*.dump 2>/dev/null | head -n 1)
    
    if [ -z "$BACKUP_FILE" ]; then
        echo -e "${RED}오류: 백업 파일이 없습니다${NC}"
        echo "먼저 백업을 실행하세요: ./scripts/backup_db.sh"
        exit 1
    fi
    
    echo -e "${GREEN}최신 백업: $(basename "$BACKUP_FILE")${NC}"
else
    # 상대 경로 처리
    if [[ "$BACKUP_FILE" != /* ]]; then
        BACKUP_FILE="$PROJECT_DIR/$BACKUP_FILE"
    fi
fi

# 파일 존재 확인
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}오류: 백업 파일이 없습니다: $BACKUP_FILE${NC}"
    echo ""
    echo "사용 가능한 백업:"
    ls -lh "$BACKUP_DIR"/portfolio_db_*.dump 2>/dev/null || echo "  없음"
    exit 1
fi

BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo ""
echo "복원 파일: $(basename "$BACKUP_FILE")"
echo "파일 크기: $BACKUP_SIZE"

# 컨테이너 확인
DB_CONTAINER=$(docker compose ps -q db 2>/dev/null || docker-compose ps -q db 2>/dev/null)
if [ -z "$DB_CONTAINER" ]; then
    echo -e "${RED}오류: DB 컨테이너가 실행 중이 아닙니다${NC}"
    echo "시작: docker compose up -d db"
    exit 1
fi

# 경고 및 확인
echo ""
echo -e "${YELLOW}⚠️  경고: 데이터베이스를 복원합니다${NC}"
if [ "$CLEAN_RESTORE" = true ]; then
    echo -e "${YELLOW}   CLEAN 모드: 기존 데이터를 삭제합니다${NC}"
fi
echo ""
echo "대상: $POSTGRES_DB"
echo "사용자: $POSTGRES_USER"
echo ""

if [ "$AUTO_YES" = false ]; then
    read -p "계속하시겠습니까? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "취소됨"
        exit 0
    fi
fi

# 복원 실행
TEMP_FILE="/tmp/restore_$(basename "$BACKUP_FILE")"

echo ""
echo -e "${YELLOW}복원 준비 중...${NC}"
docker cp "$BACKUP_FILE" "${DB_CONTAINER}:${TEMP_FILE}"

echo -e "${YELLOW}복원 진행 중...${NC}"

RESTORE_CMD="pg_restore -U $POSTGRES_USER -d $POSTGRES_DB -v --no-owner --no-acl"
if [ "$CLEAN_RESTORE" = true ]; then
    RESTORE_CMD="$RESTORE_CMD --clean --if-exists"
fi
RESTORE_CMD="$RESTORE_CMD $TEMP_FILE"

if docker exec "$DB_CONTAINER" $RESTORE_CMD 2>&1 | grep -v "ERROR.*already exists" || true; then
    echo ""
    echo -e "${GREEN}✅ 복원 완료${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  경고와 함께 복원 완료${NC}"
fi

# 정리
docker exec "$DB_CONTAINER" rm -f "$TEMP_FILE"

echo ""
echo -e "${GREEN}=== 완료 ===${NC}"
echo ""
echo "다음 단계:"
echo "  docker compose restart backend"
echo ""
echo -e "${BLUE}💡 깨끗한 복원이 필요하다면:${NC}"
echo "  docker compose down -v"
echo "  docker compose up -d db"
echo "  ./scripts/restore_db.sh -c [파일]"
echo ""
