import sys
from pathlib import Path
from PIL import Image

# --- 설정 ---

# 이 스크립트 파일이 있는 위치를 기준으로
# app/static/images/ 폴더의 경로를 설정합니다.
# (이 스크립트가 프로젝트 루트에 있다고 가정)
try:
    BASE_DIR = Path(__file__).resolve().parent
    UPLOAD_DIRECTORY = BASE_DIR / "app" / "static" / "images"
except NameError:
    # 대화형 환경 등에서 실행 시
    BASE_DIR = Path.cwd()
    UPLOAD_DIRECTORY = BASE_DIR / "app" / "static" / "images"

# UPLOAD_DIRECTORY = "backend/app/static/images"
# 리사이즈할 기준 가로 크기
TARGET_WIDTH = 512

# 처리할 이미지 확장자
SUPPORTED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}

# --- 스크립트 본문 ---

def resize_existing_images():
    """
    UPLOAD_DIRECTORY 내의 모든 이미지를 TARGET_WIDTH (512px)로 리사이즈합니다.
    비율은 유지하며, 원본 파일을 덮어씁니다.
    """
    if not UPLOAD_DIRECTORY.exists():
        print(f"오류: 디렉터리를 찾을 수 없습니다: {UPLOAD_DIRECTORY}")
        print("스크립트가 프로젝트 루트 디렉터리에 있는지 확인하세요.")
        sys.exit(1)

    print(f"이미지 일괄 리사이즈 작업을 시작합니다...")
    print(f"대상 디렉터리: {UPLOAD_DIRECTORY}")
    print(f"목표 가로 크기: {TARGET_WIDTH}px (비율 유지)")
    print("-" * 40)

    processed_count = 0
    skipped_count = 0
    failed_count = 0

    # 디렉터리 내의 모든 파일 순회
    for file_path in UPLOAD_DIRECTORY.glob('*'):
        # 파일이 아니거나 지원하는 확장자가 아니면 건너뜀
        if not file_path.is_file() or file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            # 이미지 열기
            with Image.open(file_path) as img:
                original_width, original_height = img.size
                
                # 이미 목표 가로 크기와 같은 경우
                if original_width == TARGET_WIDTH:
                    print(f"[SKIP] {file_path.name} (이미 {TARGET_WIDTH}px 입니다)")
                    skipped_count += 1
                    continue
                
                # 리사이즈 로직 (API 스크립트와 동일)
                aspect_ratio = original_height / float(original_width)
                target_height = int(TARGET_WIDTH * aspect_ratio)
                
                # 고품질 Lanczos 필터 사용
                img_resized = img.resize((TARGET_WIDTH, target_height), Image.Resampling.LANCZOS)
                
                # 저장 옵션 준비 (API 스크립트와 동일)
                save_kwargs = {}
                file_extension = file_path.suffix.lower()
                
                if file_extension in [".jpg", ".jpeg"]:
                    save_kwargs['quality'] = 90
                    if img_resized.mode in ("RGBA", "P", "LA"):
                        img_resized = img_resized.convert("RGB")
                elif file_extension == ".png":
                    save_kwargs['optimize'] = True
                
                # 원본 파일 덮어쓰기
                img_resized.save(file_path, **save_kwargs)
                
                print(f"[OK] {file_path.name} ({original_width}px -> {TARGET_WIDTH}px)")
                processed_count += 1

        except Exception as e:
            print(f"[FAIL] {file_path.name} 처리 중 오류 발생: {e}")
            failed_count += 1

    print("-" * 40)
    print("작업 완료.")
    print(f"요약: 성공={processed_count}, 스킵={skipped_count}, 실패={failed_count}")

if __name__ == "__main__":
    # Pillow 라이브러리가 설치되어 있는지 확인
    try:
        from PIL import Image
    except ImportError:
        print("오류: 'Pillow' 라이브러리가 설치되지 않았습니다.")
        print("스크립트를 실행하기 전에 'pip install Pillow'를 실행해주세요.")
        sys.exit(1)
        
    resize_existing_images()
