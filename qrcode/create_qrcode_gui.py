# pip install qrcode
# pip install pillow

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import qrcode
from PIL import Image, ImageTk
from tkinter import filedialog
import os

qr_pil_image = None
save_folder = ""
logo_path = ""

# QR 코드 생성
def generate_qr():
    global qr_pil_image
    try:
        url = input_text.get("1.0", "end").strip()
        if not url:
            messagebox.showerror("Error", "URL을 입력하세요!")
            return
        qr_color = color_combo.get()

        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )

        qr.add_data(url)
        qr.make(fit=True)

        qr_pil_image  = qr.make_image(fill_color=qr_color, back_color='white')

        if logo_path:
            qr_pil_image = add_logo(qr_pil_image, logo_path)

        img = qr_pil_image .resize((200, 200), Image.LANCZOS)  # 수정된 부분
        img_tk = ImageTk.PhotoImage(img)

        qr_image_label.config(image=img_tk)
        qr_image_label.image = img_tk # QR이미지 참조 유지

    except Exception as e:
        messagebox.showerror("오류", f"생성 중 문제가 발생했습니다.{str(e)}")

def add_logo(qr_img, logo_path):
    logo = Image.open(logo_path).convert("RGBA")

    qr_width, qr_height = qr_img.size

    # 로고 크기 = QR의 1/4
    logo_size = qr_width // 4
    logo = logo.resize((logo_size, logo_size), Image.LANCZOS)

    # 중앙 좌표 계산
    pos = (
        (qr_width - logo_size) // 2,
        (qr_height - logo_size) // 2
    )

    qr_img = qr_img.convert("RGBA")
    qr_img.paste(logo, pos, logo)  # 투명도 유지

    return qr_img

def choose_logo():
    global logo_path
    path = filedialog.askopenfilename(
        title="로고 이미지 선택",
        filetypes=[("Image Files", "*.png *.jpg *.jpeg")]
    )
    if path:
        logo_path = path
        messagebox.showinfo("로고 선택", "로고가 선택되었습니다.")

#QR 이미지 저장 
def save_qr():
    if qr_pil_image is None:
        messagebox.showwarning("경고", "먼저 QR 코드를 생성하세요!")
        return

    if not save_folder:
        messagebox.showwarning("경고", "저장 경로를 선택하세요!")
        return

    filename = file_entry.get().strip()
    if not filename:
        messagebox.showwarning("경고", "파일명을 입력하세요!")
        return

    # 확장자 제거
    filename = filename.replace(".png", "").replace(".jpg", "")
    file_type = file_combo.get()

    # 저장 경로 생성
    if file_type == "PNG":
        save_path = os.path.join(save_folder, filename + ".png")
    else:
        save_path = os.path.join(save_folder, filename + ".jpg")

    # 이미 파일이 존재하는지 확인
    if os.path.exists(save_path):
        overwrite = messagebox.askyesno(
            "덮어쓰기 확인",
            "같은 이름의 파일이 이미 존재합니다.\n덮어쓰시겠습니까?"
        )
        if not overwrite:
            return  # 저장 취소

    try:
        if file_type == "PNG":
            qr_pil_image.save(save_path)
        else:
            qr_pil_image.convert("RGB").save(save_path)

        messagebox.showinfo("완료", f"QR 코드가 저장되었습니다!\n\n{save_path}")

    except Exception:
        messagebox.showerror("오류", "파일 저장 실패")
    
# 경로 선택
def choose_save_path():
    global save_folder
    folder = filedialog.askdirectory()
    if folder:
        save_folder = folder
        messagebox.showinfo("경로 선택", f"저장 경로:\n{folder}")

# 리셋
def delete():
    global qr_pil_image, logo_path

    # 입력값 초기화
    input_text.delete(1.0, tk.END)

    # QR 이미지 제거
    qr_image_label.config(image="")
    qr_image_label.image = None

    # 내부 상태 초기화
    qr_pil_image = None
    logo_path = ""

   
root = tk.Tk()
root.title("QR코드 생성기")
root.geometry("560x600")
root.resizable(False, False)

# 마우스 우 클릭으로 복사
def paste_on_right_click(event):
    try:
        input_text.insert(tk.INSERT, root.clipboard_get())
    except tk.TclError:
        pass

# ===============================================================
# 상단 위젯
# ===============================================================

name_label = tk.Label(root,text="나만의 QR 코드 만들기>>", fg="green")
name_label.place(x=380, y=10)


input_frame = tk.LabelFrame(root, text="생성할 QR코드 내용 입력", padx=10, pady=10)
input_frame.place(x=10, y=40, width=540, height=150)

# 안내 문구
info_label = tk.Label(input_frame,text="* URL 또는 텍스트 내용 입력")
info_label.place(x=5, y=5)


close_btn = tk.Button(input_frame, text="닫기", width=10, command=root.destroy)
close_btn.place(x=430, y=0)

# 텍스트 입력창
input_text = tk.Text(input_frame)
input_text.bind("<Button-3>", paste_on_right_click)
input_text.place(x=5, y=30, width=510, height=85)

file_frame = tk.LabelFrame(root, text="저장할 QR코드 파일명 입력 :", padx=10, pady=10)
file_frame.place(x=10, y=200, width=540, height=60)

file_entry = tk.Entry(file_frame)
file_entry.place(x=5, y=5, width=510)

# 예시 텍스트
example_label = tk.Label(root, text="* 파일명 예시) my_qr01", fg="gray")
example_label.place(x=20, y=265)

path_btn = tk.Button(root, text="경로 선택", width=10, command=choose_save_path)
path_btn.place(x=360, y=265)
save_btn = tk.Button(root, text="파일 저장", width=10, command=save_qr)
save_btn.place(x=450, y=265)



# ===============================================================
# 하단 위젯 
# ===============================================================

# qr 이미지 생성 프레임
qr_frame = tk.LabelFrame(root, text="생성된 QR 코드", width=240, height=250)
qr_frame.place(x=20, y=300)

# 프레임 크기 고정 
qr_frame.pack_propagate(False)

# QR 이미지 출력 라벨 (프레임 안)
qr_image_label = tk.Label(qr_frame)
qr_image_label.place(relx=0.5, rely=0.5, anchor="center")

# QR 생성 버튼
generate_btn = tk.Button(root, text="QR코드 생성",width=15, command=generate_qr)
generate_btn.place(x=300, y=320)

# 지우기 버튼
delete_btn = tk.Button(root, text="지우기", width=13, command=delete)
delete_btn.place(x=430, y=320)

# 로고 선택
logo_btn = tk.Button(root, text="로고 선택", command=choose_logo, width=15)
logo_btn.place(x=300, y=375)

# 색상 선택
colors = ["black", "blue", "red", "green", "purple", "hotpink", "navy", "teal", "brown", "orange"]
tk.Label(root,text="QR 코드 색상 선택").place(x=300, y=420)
color_combo = ttk.Combobox(root, values=colors, state="readonly", width=18)
color_combo.place(x=300, y=445)
color_combo.set("black")

# 파일 형식 선택
tk.Label(root, text="저장 형식").place(x=300, y=475)

file_combo = ttk.Combobox(root, values=["PNG", "JPG"], state="readonly", width=18)
file_combo.place(x=300, y=500)
file_combo.set("PNG")



root.mainloop()
