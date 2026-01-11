import shutil
import uuid
import io  # io 모듈 추가
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status
from PIL import Image  # Pillow 라이브러리 추가

from app import models
from app.api.v1 import deps

router = APIRouter()

# 업로드된 이미지를 저장할 디렉터리 경로
UPLOAD_DIRECTORY = Path("app/static/images/")
# 디렉터리가 없으면 생성
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@router.post("/")
async def upload_image(  # 비동기 처리를 위해 async 추가
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    이미지 파일을 서버에 업로드합니다. (관리자 권한 필요)
    
    업로드된 이미지는 WebP 포맷으로 변환되어 저장됩니다.
    업로드 성공 시, 이미지에 접근할 수 있는 URL 경로를 반환합니다.
    """
    # 이미지 파일인지 MIME 타입으로 확인
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not an image.",
        )
        
    # UUID를 사용하여 고유한 파일 이름 생성 (확장자는 항상 .webp)
    unique_filename = f"{uuid.uuid4()}.webp"
    file_path = UPLOAD_DIRECTORY / unique_filename
    
    try:
        # 파일을 메모리로 읽기 (shutil 대신)
        contents = await file.read()
        if not contents:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File is empty.",
            )

        # PIL을 사용하여 메모리 상의 이미지 열기
        img = Image.open(io.BytesIO(contents))

        # 리사이즈 로직 추가 (가로 최대 1024px, 비율 유지)
        MAX_WIDTH = 1024
        if img.width > MAX_WIDTH:
            aspect_ratio = img.height / float(img.width)
            target_height = int(MAX_WIDTH * aspect_ratio)
            img = img.resize((MAX_WIDTH, target_height), Image.Resampling.LANCZOS)
        
        # WebP 포맷으로 저장 (품질 90)
        img.save(file_path, "WEBP", quality=90)
            
    except HTTPException as e:
        # HTTP 예외는 그대로 다시 발생시킴
        raise e
    except Exception as e:
        # PIL 처리 중 예외 발생 가능 (예: 손상된 이미지 파일)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process image: {str(e)}",
        )
    finally:
        # FastAPI의 UploadFile 객체를 닫아줌
        await file.close()
        
    # 프론트엔드에서 사용할 수 있는 URL 경로 반환
    return {"file_path": f"/static/images/{unique_filename}"}
