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

# 리사이즈할 기준 가로 크기
TARGET_WIDTH = 512

@router.post("/")
async def upload_image(  # 비동기 처리를 위해 async 추가
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_admin_user)
):
    """
    이미지 파일을 서버에 업로드합니다. (관리자 권한 필요)
    
    업로드된 이미지는 가로 {TARGET_WIDTH}px로 리사이즈되며, 비율은 유지됩니다.
    업로드 성공 시, 이미지에 접근할 수 있는 URL 경로를 반환합니다.
    """
    # 이미지 파일인지 MIME 타입으로 확인
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is not an image.",
        )
        
    # 파일 확장자 추출 (소문자로 통일)
    file_extension = Path(file.filename).suffix.lower()
    # UUID를 사용하여 고유한 파일 이름 생성
    unique_filename = f"{uuid.uuid4()}{file_extension}"
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
        
        # 원본 이미지 크기 확인
        original_width, original_height = img.size
        
        if original_width == TARGET_WIDTH:
            # 리사이즈가 필요 없는 경우 (가로 크기가 이미 512px)
            # 원본 파일 그대로 저장
            with file_path.open("wb") as buffer:
                buffer.write(contents)
        else:
            # 리사이즈가 필요한 경우
            # 원본 비율에 맞춰 새로운 세로 크기 계산
            aspect_ratio = original_height / float(original_width)
            target_height = int(TARGET_WIDTH * aspect_ratio)
            
            # 이미지 리사이즈 (고품질 Lanczos 필터 사용)
            img_resized = img.resize((TARGET_WIDTH, target_height), Image.Resampling.LANCZOS)
            
            # 저장 옵션 준비
            save_kwargs = {}
            if file_extension in [".jpg", ".jpeg"]:
                save_kwargs['quality'] = 90  # JPEG 품질 설정
                # PNG 같은 투명 이미지를 JPEG로 저장할 경우 RGB로 변환
                if img_resized.mode in ("RGBA", "P", "LA"): 
                    img_resized = img_resized.convert("RGB")
            elif file_extension == ".png":
                save_kwargs['optimize'] = True # PNG 최적화
            
            # 리사이즈된 이미지 디스크에 저장
            # format을 명시하지 않아도 Pillow가 확장자로부터 추론하지만,
            # save_kwargs를 사용하기 위해 이 방식을 사용합니다.
            img_resized.save(file_path, **save_kwargs)
            
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
