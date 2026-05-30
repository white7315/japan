import os
import mimetypes
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# 구글 드라이브 접근 권한 범위 (파일 생성 및 읽기 권한)
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def get_gdrive_service():
    creds = None
    # 이전에 인증한 토큰이 있는지 확인
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # 인증 토큰이 없거나 만료된 경우 재인증
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "프로젝트 루트 디렉토리에 'credentials.json' 파일이 없습니다. "
                    "구글 클라우드 콘솔에서 다운로드하여 E:\\japan\\credentials.json 경로에 넣어주세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            # 로컬 웹서버를 띄워 인증 처리 (웹 브라우저가 열림)
            creds = flow.run_local_server(port=0)
            
        # 다음 실행을 위해 인증 자격 증명(토큰) 저장
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('drive', 'v3', credentials=creds)

def create_folder(service, folder_name):
    """구글 드라이브에 폴더를 생성하고 폴더 ID 반환"""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata, fields='id').execute()
    print(f"구글 드라이브에 폴더가 생성되었습니다. 폴더명: {folder_name} (ID: {file.get('id')})")
    return file.get('id')

def upload_file(service, file_path, folder_id):
    """지정된 폴더 안에 파일 업로드"""
    if not os.path.exists(file_path):
        print(f"파일을 찾을 수 없습니다: {file_path}")
        return None
        
    file_name = os.path.basename(file_path)
    mime_type, _ = mimetypes.guess_type(file_path)
    if not mime_type:
        mime_type = 'application/octet-stream'
        
    file_metadata = {
        'name': file_name,
        'parents': [folder_id]
    }
    
    media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)
    file = service.files().create(
        body=file_metadata,
        media_body=media,
        fields='id, webViewLink'
    ).execute()
    
    print(f"업로드 완료: {file_name} -> 링크: {file.get('webViewLink')}")
    return file.get('id')

def upload_sourced_images():
    try:
        service = get_gdrive_service()
        
        # 1. '피규어1' 폴더 생성
        folder_id = create_folder(service, '피규어1')
        
        # 2. 업로드할 이미지 목록 (E 드라이브 워크스페이스 내 파일들)
        images = [
            'shiroko_nendoroid_1780104752389.png',
            'j_stage_case_1780104770979.png',
            'arona_nendoroid_1780104791379.png'
        ]
        
        # 3. 차례대로 업로드
        for img in images:
            img_path = os.path.join(os.getcwd(), img)
            upload_file(service, img_path, folder_id)
            
        print("\n모든 파일이 성공적으로 구글 드라이브에 업로드되었습니다!")
        
    except Exception as e:
        print(f"에러 발생: {e}")

if __name__ == "__main__":
    # 실행 시 프로젝트 루트 디렉토리를 작업 경로로 고정
    os.chdir(r"E:\japan")
    upload_sourced_images()
