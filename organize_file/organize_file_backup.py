import shutil
from pathlib import Path
from datetime import datetime

def get_downloads_folder():
    """사용자의 다운로드 폴더 경로 반환"""
    home = Path.home()
    downloads = home / "Downloads"

    if downloads.exists():
        return downloads
    else: # 다운로드 폴더가 없으면, FileNotFoundError를 발생시킴
        raise FileNotFoundError("다운로드 폴더를 찾을 수 없습니다.")


def create_backup_folder(src):
    """백업 폴더 생성 및 경로 반환"""
    today = datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_folder = src/ f"Backup_{today}"
    backup_folder.mkdir(exist_ok=True)
    print(f"백업 폴더 생성: {backup_folder}")
    return backup_folder


def backup_file(file_path, backup_folder):
    """파일을 백업 폴더로 복사"""
    try:
        shutil.copy2(file_path, backup_folder)
        return True
    except Exception as e:
        print(f"백업 실패: {file_path.name} - {e}")
        return False


def organize_files():
    """다운로드 폴더 정리 + 백업 기능"""
    
    # 1. 원본 경로 설정
    source = get_downloads_folder()
    
    # 2. 백업 경로 설정
    home = Path.home()
    desktop = home / "Desktop" #
    backup_folder = create_backup_folder(desktop) # 바탕화면에 백업 폴더 생성

    # 3. 카테고리별 폴더 매핑
    categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.hwpx'],
        'code' : ['.py', '.ipynb', '.c', '.html', '.css', '.js'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov'],
        'music': ['.mp3', '.wav', '.flac'],
        'archives': ['.zip', '.rar', '.7z']
    }
    

    # 카테고리 폴더 미리 생성
    for category in categories.keys():
        (source / category).mkdir(exist_ok=True)

    moved = 0
    skipped = 0
    backed_up = 0

    print(f"\n'{source}' 폴더 정리 + 백업 시작...\n")

    for file in source.iterdir():
        if not file.is_file():
            continue

        ext = file.suffix.lower()
        backed_up_success = backup_file(file, backup_folder)

        if backed_up_success:
            backed_up += 1

        for category, exts in categories.items():
            if ext in exts:
                dest = source / category / file.name

                # 이름 충돌 처리
                if dest.exists():
                    counter = 1
                    original_name = file.stem
                    while (source / category / f"{original_name} ({counter}){ext}").exists():
                        counter += 1
                    dest = source / category / f"{original_name} ({counter}){ext}"

                try:
                    shutil.move(file, dest)
                    print(f"{category}로 이동: {file.name}")
                    moved += 1
                except Exception as e:
                    print(f"이동 실패: {file.name} - {e}")
                    skipped += 1
                break

        # 카테고리에 없는 파일은 others 폴더로
        else:           
            other = source / "others"
            other.mkdir(exist_ok=True)
            try:
                shutil.move(file, other / file.name)
                print(f"기타 폴더로 이동: {file.name}")
                moved += 1
            except Exception as e:
                print(f"이동 실패: {file.name} - {e}")
                skipped += 1

    print("\n" + "="*60)
    print("다운로드 폴더 정리 + 백업 완료!")
    print(f"백업된 파일: {backed_up}개")
    print(f"이동된 파일: {moved}개")
    print(f"실패한 파일: {skipped}개")
    print(f"백업 위치: {backup_folder}")
    print("="*60)


if __name__ == "__main__":
    try:
        organize_files()
    except Exception as e:
        print(f"예상치 못한 오류 발생: {e}")
