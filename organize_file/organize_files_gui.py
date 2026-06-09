import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox, scrolledtext
from datetime import datetime
import shutil
import os
from pathlib import Path
from send2trash import send2trash 
import threading


# ====================== 확장자 카테고리 ======================
categories = {
        'images': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        'documents': ['.pdf', '.doc', '.docx', '.txt', '.xlsx', '.pptx', '.hwpx'],
        'code' : ['.py', '.ipynb', '.c', '.html', '.css', '.js'],
        'videos': ['.mp4', '.avi', '.mkv', '.mov'],
        'music': ['.mp3', '.wav', '.flac'],
        'archives': ['.zip', '.rar', '.7z']
    }
# ====================== 함수 정의 ======================

# 경로를 선택합니다
def select_folder(entry_folder):
    folder = filedialog.askdirectory()
    if folder:
        entry_folder.delete(0, tk.END)
        entry_folder.insert(0, folder)

# 작업 
def worker(task, folder):
    try:
        if task == "📁 파일 정리와 백업":
            organize_files(folder)
        elif task == "🧹 빈 폴더 삭제":
            delete_empty_folder(folder)
        elif task == "🗑 선택 항목 휴지통 이동":
            move_file_to_trash(folder)
    finally:
        # 작업 끝난 후 메인 스레드에서 버튼 다시 활성화
        root.after(0, lambda: run_button.config(state="normal"))

# 선택한 작업을 실행합니다
def run_program(entry_folder):
    folder = entry_folder.get()

    if not folder:
        messagebox.showwarning("경고", "폴더를 선택하세요.")
        return

    run_button.config(state="disabled")
    ui_clear_log()
    ui_progress(0)

    t = threading.Thread(
        target=worker,
        args=(task_combo.get(), folder),
        daemon=True
    )
    t.start()


def ui_log(msg):
    root.after(0, lambda: (log_box.insert(tk.END, msg), log_box.see(tk.END)))

def ui_progress(value):
    root.after(0, lambda: p_var.set(value))

def ui_clear_log():
    root.after(0, lambda: log_box.delete(1.0, tk.END))


def ui_message(kind, title, msg):
    if kind == "info":
        root.after(0, lambda: messagebox.showinfo(title, msg))
    elif kind == "warn":
        root.after(0, lambda: messagebox.showwarning(title, msg))
    elif kind == "error":
        root.after(0, lambda: messagebox.showerror(title, msg))


# 백업 폴더를 생성하는 함수
def create_backup_folder(src):
    today = datetime.now().strftime("%Y-%m-%d_%H-%M")
    backup_folder = src / f"Backup_{today}"
    backup_folder.mkdir(exist_ok=True)
    return backup_folder

# 파일을 백업 폴더로 복사하는 함수
def backup_file(file_path, backup_folder):
    try:
        shutil.copy2(file_path, backup_folder)
        return True
    except Exception as e:
        ui_log(f"[백업 실패] {file_path.name} - {e}\n")
        return False
    
# 작업 결과를 txt파일로 저장하는 함수
def save_log_to_file():
    content = log_box.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("알림", "저장할 내용이 없습니다.")
        return
    
    # 파일 저장 경로 선택
    save_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text File", "*.txt")],
        initialfile="log.txt",  
        title="파일 저장")
    
    if not save_path:
        return

    # 덮어쓰기 확인 (명확하게 제어)
    if os.path.exists(save_path):
        overwrite = messagebox.askyesno("확인", "파일이 이미 존재합니다. 덮어쓸까요?")
        if not overwrite:
            return
    
    try:
        with open(save_path, "w", encoding="utf-8") as f:
            f.write(content)

        messagebox.showinfo("완료", "작업이 저장되었습니다.")
    except Exception as e:
        messagebox.showerror("오류", f"저장 실패: {e}")


# 파일 정리 및 백업 함수
def organize_files(folder_path):
    source = Path(folder_path)
    desktop = Path.home() / "Desktop"
    backup_folder = create_backup_folder(desktop)

    moved = skipped = backup = 0

    files = [f for f in source.iterdir() if f.is_file()]
    total = len(files)

    for i, file in enumerate(files, 1):
        ext = file.suffix.lower()

        # 백업
        if backup_file(file, backup_folder):
            backup += 1

        for category, exts in categories.items():
            if ext in exts:
                dest_dir = source / category
                dest_dir.mkdir(exist_ok=True)

                dest = dest_dir / file.name
                counter = 1
                while dest.exists():
                    dest = dest_dir / f"{file.stem} ({counter}){file.suffix}"
                    counter += 1

                try:
                    shutil.move(file, dest)
                    ui_log(f"[이동] {file.name} → {category}\n")
                    moved += 1
                except Exception as e:
                    ui_log(f"[실패] {file.name} - {e}\n")
                    skipped += 1

                break

        else: 
            other = source / "others"
            other.mkdir(exist_ok=True)

            dest = other / file.name
            try:
                shutil.move(file, dest)
                ui_log(f"[기타] {file.name}\n")
                moved += 1
            except Exception as e:
                ui_log(f"[이동 실패] {file.name} - {e}\n")
                skipped += 1

        # 진행률 업데이트
        if i % 10 == 0:
            progress = (i / total) * 100 if total else 0
            ui_progress(progress)

    ui_log(f"\n완료: {moved}개 파일 이동 / {skipped} 파일 실패 / {backup}개 파일 백업\n")
    ui_progress(100)

# 파일과 디렉토리를 휴지통으로 이동하는 함수.
def move_file_to_trash(folder_path):
    source = Path(folder_path)
    items = list(source.iterdir())

    total = len(items)
    count = 0
    moved_file = 0
    moved_folder = 0

    for item in items:
        count += 1

        try:
            if item.is_file() and opt_file.get():
                send2trash(str(item))
                ui_log(f"[파일] {item.name} → 휴지통\n")
                moved_file += 1

            elif item.is_dir() and opt_folder.get():
                send2trash(str(item))
                ui_log(f"[폴더] {item.name} → 휴지통\n")
                moved_folder += 1

        except Exception as e:
            ui_log(f"[실패] {item.name} - {e}\n")

        if count % 10 == 0:
            progress = (count / total) * 100 if total else 0
            ui_progress(progress)

    ui_log(f"\n완료: 파일 {moved_file}개, 폴더 {moved_folder}개 휴지통으로 이동\n")
    ui_progress(100)

# 빈폴더를 삭제하는 함수
def delete_empty_folder(folder_path):
    source = Path(folder_path)

    all_dirs = []
    for path, dirs, _ in os.walk(source):
        for d in dirs:
            all_dirs.append(Path(path) / d)

    all_dirs.sort(key=lambda x: len(x.parts), reverse=True)

    total = len(all_dirs)
    deleted = 0

    for i, dir_path in enumerate(all_dirs, 1):
        try:
            if not any(dir_path.iterdir()):
                dir_path.rmdir()
                ui_log(f"[삭제] {dir_path}\n")
                deleted += 1
        except Exception as e:
            ui_log(f"[이동 실패] {dir_path} - {e}\n")

        if i % 10 == 0:
            progress = (i / total) * 100 if total else 0
            ui_progress(progress)

    ui_log(f"\n{deleted}개 폴더가 삭제되었습니다.\n")
    ui_progress(100)
   
# ====================== 메인 윈도우 ======================
root = tk.Tk()
root.title("파일 정리 프로그램")
root.geometry("520x630")
root.resizable(False, False)

# ====================== 1. 작업 선택 ======================
frame1 = ttk.LabelFrame(root, text="수행할 작업을 선택하세요")
frame1.pack(fill="x", padx=10, pady=5)

task_combo = ttk.Combobox(
    frame1,values=["📁 파일 정리와 백업",
    "🧹 빈 폴더 삭제",
    "🗑 선택 항목 휴지통 이동"],
    state="readonly"
)
task_combo.current(0)
task_combo.pack(fill="x", padx=5, pady=5)

# ====================== 1-1. 삭제 옵션 ======================
option_frame = ttk.LabelFrame(root, text="삭제 옵션")
option_frame.pack(fill="x", padx=10, pady=5)

# 안내 텍스트
option_label = ttk.Label(
    option_frame,
    text="※ '휴지통 보내기' 작업시 선택하세요.",
    foreground="gray"
)
option_label.pack(anchor="w", padx=5, pady=(2, 5), side="left")

# 체크박스 영역
check_frame = ttk.Frame(option_frame)
check_frame.pack(fill="x", padx=10, pady=5, side="left")

opt_file = tk.BooleanVar(value=True)
opt_folder = tk.BooleanVar(value=True)

chk_file = ttk.Checkbutton(
    check_frame,
    text="📄 파일",
    variable=opt_file
)

chk_folder = ttk.Checkbutton(
    check_frame,
    text="📁 폴더",
    variable=opt_folder
)

chk_file.pack(side="left", padx=15)
chk_folder.pack(side="left", padx=15)

# ====================== 2. 문자 입력 ======================
frame2 = ttk.LabelFrame(root, text="📁 작업 결과 출력")
frame2.pack(fill="x", padx=10, pady=5)

ttk.Label(frame2, text="작업 경로").pack(anchor="w", padx=5)

# 작업 결과 출력
log_box = scrolledtext.ScrolledText(frame2, width=70, height=18)
log_box.pack()


# ====================== 3. 폴더 선택 ======================
frame3 = ttk.LabelFrame(root, text="작업할 폴더를 선택하세요")
frame3.pack(fill="x", padx=10, pady=5)

folder_frame = ttk.Frame(frame3)
folder_frame.pack(fill="x", padx=5, pady=5)



entry_folder = ttk.Entry(folder_frame)
entry_folder.pack(side="left", fill="x", expand=True, ipady=4)

ttk.Button(folder_frame, text="찾아보기", command=lambda: select_folder(entry_folder)).pack(side="left", ipady=5, padx=5)

# ====================== 4. 프로그레스바 ======================
frame4 = ttk.LabelFrame(root, text="진행상황")
frame4.pack(fill="x", padx=10, pady=5)

p_var = tk.DoubleVar()
progress = ttk.Progressbar(frame4, maximum=100, variable=p_var)
progress.pack(fill="x", padx=5, pady=10)

# ====================== 5. 버튼 영역 ======================
frame5 = ttk.Frame(root)
frame5.pack(fill="x", padx=10, pady=10)

run_button = ttk.Button(frame5, text="프로그램 실행", command=lambda: run_program(entry_folder))
run_button.pack(side="left", expand=True, ipady=7, ipadx=20)
save_button = ttk.Button(frame5, text="💾 작업 저장", command=save_log_to_file)
save_button.pack(side="left", expand=True, ipady=7, ipadx=20)
ttk.Button(frame5, text="❎ 종료(닫기)", command=root.quit).pack(side="left", expand=True, ipady=7, ipadx=20)

# ====================== 실행 ======================
root.mainloop()
