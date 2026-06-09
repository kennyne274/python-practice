import os
import shutil

# 파일 이동 함수(부모 경로, 원본 파일 폴더, 목적지 폴더)
def file_move(parent_path, source_folder, target_folder):

    # 원본 폴더와 목적지 폴더의 경로를 생성합니다.
    source_path = os.path.join(parent_path, source_folder)   
    target_path = os.path.join(parent_path, target_folder) 

    os.makedirs(target_path, exist_ok=True) # target_path 폴더 생성

    try:
    
        for file in os.listdir(source_path):
            file_path = os.path.join(source_path, file)
            
            if os.path.isdir(file_path):
                            continue 
            # 확장자가 'py', ".ipynb"인 파일을 'target_path'로 이동함
            if file.lower().endswith((".py", ".ipynb")): 

                try: 
                    # 파일 이동
                    shutil.move(file_path, target_path)
                except PermissionError:
                    print(f"파일 권한이 없습니다.{file}")
                except shutil.Error:
                    print(f"파일 이동 실패. {file}")

    except FileNotFoundError:
        print("지정된 경로를 찾을 수 없습니다.")


if __name__ == "__main__":

    home = os.path.expanduser("~") # 홈 경로
    desktop = os.path.join(home, "Desktop") # 내 컴퓨터 바탕화면 경로

    file_move(desktop, "files", "my_file")
    print(os.listdir(os.path.join(desktop, "my_file")))

