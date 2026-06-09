import os
import shutil
from datetime import datetime 

# 스크린샷 파일 날짜별 정리

def organize_screenshots(source_dir):
    # 대상 경로 생성  
    target_base = os.path.join(source_dir, "Screenshots")
    os.makedirs(target_base, exist_ok=True)
    
    for file in os.listdir(source_dir):
        filepath = os.path.join(source_dir, file)

        # 파일만 처리
        if not os.path.isfile(filepath):
            continue

        # 키워드 필터링
        if "스크린샷" not in file:
            continue

        # 파일 수정 시간 가져오기
        timestamp = os.path.getmtime(filepath)
        date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")

        # 날짜 폴더 생성
        date_folder = os.path.join(target_base, date)
        os.makedirs(date_folder, exist_ok=True)

        # 이동 경로
        target_path = os.path.join(date_folder, file)

        # 이름 충돌 방지
        name, ext = os.path.splitext(file)
        counter = 1
        while os.path.exists(target_path):
            new_name = f"{name} ({counter}){ext}"
            target_path = os.path.join(date_folder, new_name)
            counter += 1

        try:
            shutil.move(filepath, target_path)
            print(f"이동: {file} → {date}/")
        except Exception as e:
            print(f"오류: {file} → {e}")

# 실행
if __name__ == "__main__":
    path = input("폴더 경로 입력: ")
    organize_screenshots(path)
