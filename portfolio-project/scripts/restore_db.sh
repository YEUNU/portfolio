#!/bin/bash

################################################################################
# PostgreSQL Database Restore Script
# 
# 이 스크립트는 백업 파일로부터 PostgreSQL DB를 복원합니다.
# pg_restore를 사용하여 custom format 백업 파일을 복원합니다.
#
# 사용법:
#   ./scripts/restore_db.sh [백업파일경로]
#   ./scripts/restore_db.sh                    # 최신 백업 파일 자동 선택
#   ./scripts/restore_db.sh backups/portfolio_db_2025-11-20_1200.dump
#
# 주의사항:
#   - 복원 시 기존 데이터가 유지되거나 충돌할 수 있습니다.
#   - 깨끗한 복원을 원하면 --clean 옵션을 사용하세요 (스크립트 내에서 설정 가능).
#   - 프로덕션 환경에서는 반드시 백업 후 복원하세요!
################################################################################

set -e  # 오류 발생 시 스크립트 중단

# 색상 정의
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 프로젝트 루트 디렉토리로 이동
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

echo -e "${BLUE}=== PostgreSQL Database Restore ===${NC}"
echo "프로젝트 경로: $PROJECT_DIR"

# .env 파일 확인
if [ ! -f ".env" ]; then
    echo -e "${RED}❌ .env 파일을 찾을 수 없습니다.${NC}"
    exit 1
fi

# 환경 변수 로드
source .env

BACKUP_DIR="$PROJECT_DIR/backups"

# 백업 파일 경로 결정
if [ -z "$1" ]; then
    # 인자가 없으면 최신 백업 파일 자동 선택
    echo "백업 파일이 지정되지 않았습니다. 최신 백업 파일을 찾는 중..."
    
    if [ ! -d "$BACKUP_DIR" ]; then
        echo -e "${RED}❌ 백업 디렉토리가 없습니다: $BACKUP_DIR${NC}"
        exit 1
    fi
    
    # 최신 .dump 파일 찾기
    BACKUP_FILE=$(ls -t "$BACKUP_DIR"/portfolio_db_*.dump 2>/dev/null | head -n 1)
    
    if [ -z "$BACKUP_FILE" ]; then
        echo -e "${RED}❌ 백업 파일을 찾을 수 없습니다.${NC}"
        echo "백업 파일을 직접 지정하거나 먼저 백업을 실행하세요:"
        echo "  ./scripts/backup_db.sh"
        exit 1
    fi
    
    echo -e "${GREEN}최신 백업 파일 발견: $(basename "$BACKUP_FILE")${NC}"
else
    # 인자로 받은 파일 경로 사용
    BACKUP_FILE="$1"
    
    # 상대 경로면 절대 경로로 변환
    if [[ "$BACKUP_FILE" != /* ]]; then
        BACKUP_FILE="$PROJECT_DIR/$BACKUP_FILE"
    fi
fi

# 백업 파일 존재 확인
if [ ! -f "$BACKUP_FILE" ]; then
    echo -e "${RED}❌ 백업 파일을 찾을 수 없습니다: $BACKUP_FILE${NC}"
    echo ""
    echo "사용 가능한 백업 파일:"
    ls -lh "$BACKUP_DIR"/portfolio_db_*.dump 2>/dev/null || echo "  (백업 파일 없음)"
    exit 1
fi

BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
echo ""
echo "복원할 백업 파일: $BACKUP_FILE"
echo "파일 크기: $BACKUP_SIZE"

# DB 컨테이너 확인
DB_CONTAINER=$(docker-compose ps -q db 2>/dev/null || docker compose ps -q db 2>/dev/null)

if [ -z "$DB_CONTAINER" ]; then
    echo -e "${RED}❌ DB 컨테이너가 실행 중이지 않습니다.${NC}"
    echo "다음 명령으로 컨테이너를 시작하세요: docker-compose up -d db"
    exit 1
fi

# 경고 메시지 및 확인
echo ""
echo -e "${YELLOW}⚠️  경고: 이 작업은 데이터베이스를 복원합니다.${NC}"
echo -e "${YELLOW}   기존 데이터와 충돌할 수 있습니다.${NC}"
echo ""
echo "대상 DB: $POSTGRES_DB"
echo "사용자: $POSTGRES_USER"
echo ""

# 사용자 확인 (자동화 스크립트에서는 -y 옵션 추가 가능)
read -p "계속하시겠습니까? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "복원 작업이 취소되었습니다."
    exit 0
fi

# 임시 파일명 생성
TEMP_RESTORE_FILE="/tmp/restore_$(basename "$BACKUP_FILE")"

echo ""
echo -e "${YELLOW}백업 파일을 컨테이너로 복사 중...${NC}"
docker cp "$BACKUP_FILE" "${DB_CONTAINER}:${TEMP_RESTORE_FILE}"

echo -e "${YELLOW}데이터베이스 복원 중...${NC}"
echo "이 작업은 몇 분이 걸릴 수 있습니다..."
echo ""

# pg_restore 실행
# 옵션 설명:
#   -U: 사용자명
#   -d: 데이터베이스명
#   -v: verbose (진행 상황 표시)
#   --clean: 기존 객체 삭제 후 복원 (선택사항 - 필요시 주석 해제)
#   --if-exists: clean 사용 시 객체가 없어도 오류 무시
#   --no-owner: 소유자 정보 무시 (권한 문제 방지)
#   --no-acl: 권한 정보 무시

# 기본 복원 (기존 데이터 유지, 중복 시 오류 발생 가능)
if docker exec -i "$DB_CONTAINER" pg_restore \
    -U "$POSTGRES_USER" \
    -d "$POSTGRES_DB" \
    -v \
    --no-owner \
    --no-acl \
    "$TEMP_RESTORE_FILE" 2>&1 | grep -v "ERROR.*already exists" || true; then
    
    echo ""
    echo -e "${GREEN}✅ 데이터베이스 복원 완료!${NC}"
else
    echo ""
    echo -e "${YELLOW}⚠️  일부 경고가 있었지만 복원이 완료되었습니다.${NC}"
    echo "기존 객체가 있어서 일부 중복 오류가 발생했을 수 있습니다."
fi

# 컨테이너 내부 임시 파일 삭제
echo ""
echo "임시 파일 정리 중..."
docker exec "$DB_CONTAINER" rm -f "$TEMP_RESTORE_FILE"

echo ""
echo -e "${GREEN}=== 복원 작업 완료 ===${NC}"
echo ""
echo "다음 단계:"
echo "  1. 애플리케이션을 재시작하세요: docker-compose restart backend"
echo "  2. 웹 브라우저에서 정상 동작을 확인하세요."
echo "  3. 데이터 무결성을 검증하세요."
echo ""
echo -e "${BLUE}💡 깨끗한 복원을 원한다면:${NC}"
echo "   1. DB를 완전히 초기화하고 복원하려면 다음 명령을 사용하세요:"
echo "      docker-compose down -v  # 볼륨 포함 컨테이너 삭제"
echo "      docker-compose up -d db  # DB 컨테이너만 시작"
echo "      ./scripts/restore_db.sh [백업파일]"
echo ""
