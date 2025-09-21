import shutil
import uuid
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException, status

from app import models
from app.api.v1 import deps

router = APIRouter()

# 업로드된 이미지를 저장할 디렉터리 경로
UPLOAD_DIRECTORY = Path("app/static/images/")
# 디렉터리가 없으면 생성
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)

@router.post("/")
def upload_image(
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    이미지 파일을 서버에 업로드합니다. (관리자 권한 필요)
    
    업로드 성공 시, 이미지에 접근할 수 있는 URL 경로를 반환합니다.
    """
    # 이미지 파일인지 MIME 타입으로 확인
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not an image.",
        )
        
    # 파일 확장자 추출
    file_extension = Path(file.filename).suffix
    # UUID를 사용하여 고유한 파일 이름 생성
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = UPLOAD_DIRECTORY / unique_filename
    
    try:
        # 파일을 디스크에 저장
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    finally:
        file.file.close()
        
    # 프론트엔드에서 사용할 수 있는 URL 경로 반환
    return {"file_path": f"/static/images/{unique_filename}"}
