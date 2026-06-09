# GUI버젼 로또 생성기입니다. 
# 버튼을 클릭하여 한번에 10개의 로또 번호를 생성하거나 복사할 수 있습니다. 

import tkinter as tk
import random

# 색상 선택
BG_MAIN = "#3c2f2f" 
BG_TEXT = "#2b1e1e"
FG_GOLD = "#D7CDC8"
BTN_BG =  "#945620"
BTN_FG = "#000000"

TITLE_TEXT = "로또 번호 10세트 자동 생성기"

# 로또 생성 함수(본번호 + 보너스 10세트)
def generate_lotto_sets():
    title.config(text=TITLE_TEXT)
    result_box.config(state="normal")
    result_box.delete("1.0", tk.END)

    for i in range(10):
        numbers = random.sample(range(1, 46), 7)
        main = sorted(numbers[:6])
        bonus = numbers[6]

        line = f"{i+1}게임  본번호: {', '.join(map(str, main))} : 보너스: {bonus}\n"
        result_box.insert(tk.END, line)

    result_box.config(state="disabled")

# 클립보드로 복사 
def copy_to_clipboard():
    root.clipboard_clear()
    text = result_box.get("1.0", tk.END)
    root.clipboard_append(text)
    title.config(text="📋복사완료")


# GUI 기본 설정 
root = tk.Tk()
root.title("로또 번호 생성기")
root.geometry("580x460")
root.config(bg=BG_MAIN)
root.resizable(False, False)

# 제목
title = tk.Label(
    root,
    text=TITLE_TEXT,font=("휴먼편지체",15,"bold"), fg=FG_GOLD, bg=BG_MAIN)
title.pack(pady=(30,5))


# 결과 출력
text_frame = tk.Frame(root, bg=BG_MAIN)
text_frame.pack()

scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

result_box = tk.Text(text_frame, width=55, height=15,bg=BG_TEXT,fg=FG_GOLD, 
    font=("함초롱바탕", 12,"bold"), yscrollcommand=scrollbar.set)
result_box.pack(pady=10)

scrollbar.config(command=result_box.yview)
result_box.config(state="disabled")

# 버튼 생성 및 배치
btn_frame = tk.Frame(root, bg=BG_MAIN)
btn_frame.pack(pady=10)

btn1 = tk.Button(
    btn_frame, text="로또 번호 추천", font=("함초롱바탕", 14, "bold"), 
    bg=BTN_BG, fg=BTN_FG, width=12, height=2,
    command=generate_lotto_sets
)
btn1.pack(side="left", padx=5)

btn2 = tk.Button(
    btn_frame, text="복사하기", font=("함초롱바탕", 14, "bold"),
    bg=BTN_BG, fg=BTN_FG, width=10, height=2,
    command=copy_to_clipboard
)
btn2.pack(side="left", padx=5)

btn3 = tk.Button(btn_frame, text="닫기", font=("함초롱바탕", 14, "bold"),
    bg=BTN_BG, fg=BTN_FG, width=7, height=2,command=root.destroy
)
btn3.pack(side="left", padx=5)

# 창유지
root.mainloop()
