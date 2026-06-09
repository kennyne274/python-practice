import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from playsound3 import playsound
from gtts import gTTS
import threading
import uuid
import os

# 입력한 텍스트를 음성으로 변환하여 읽어주는 프로그램
# 프로그램을 실행하려면 gTTS와 playsound3 라이브러리를 설치해야 합니다.
# pip install gTTS
# pip install playsound3

# 텍스트를 음성으로 변환하는 gTTS 객체를 생성하는 함수
def generate_tts(text):
    #  콤보박스에서 가져온 키값으로 languages의 value에 접근
    lang = languages[input_lang.get()]
    speed = speed_menu.get()

    # slow를 선택하면 True, 아니면 False를 반환함
    if speed == "slow":
        slow = True
    else:
        slow = False
    # gTTS 객체 생성(텍스트 -> 음성 데이터)
    try:
        tts = gTTS(text ,
                    lang = lang, 
                    slow = slow)
        return tts
    except Exception as e:
        messagebox.showerror("에러", f"재생 중 에러가 발생했습니다\n{e}")
        return

# 음성을 생성하고 재생하는 함수(스레드에서 실행됨)
def play(text):
    tts = generate_tts(text)

    # 파일 이름 충돌 방지
    filename = f"{uuid.uuid4()}.mp3"
    # 음성 데이터를 MP3 파일로 저장
    tts.save(filename)
    # MP3 파일 재생
    playsound(filename)
    # 재생한 파일 삭제
    try:
        os.remove(filename)
    except PermissionError:
        pass

    root.after(0, lambda: speak_btn.config(state="normal"))
       
# 텍스트에 입력한 문자를 가져와서 읽도록 요청하는 함수
def speak_text():
    
    # 입력한 텍스트 가져오기
    text = text_area.get("1.0", tk.END).strip()

    # 입력없으면 경고
    if not text:
        messagebox.showwarning("Input Error", "문장을 입력하세요")
        return
    
    # 버튼 연타 방지
    speak_btn.config(state="disabled")       

    # 음성 생성 및 재생 작업을 별도의 스레드에서 실행
    # GUI 멈춤 방지
    thread = threading.Thread(target=play, args=(text,), daemon=True)
    thread.start()

    
# 음성 데이터를 MP3 파일로 저장
def save_audio():
    text = text_area.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Input Error", "문장을 입력하세요")
        return

    # 저장 경로 설정 및 파일 이름 선택
    file = filedialog.asksaveasfilename(
        defaultextension=".mp3",
        filetypes=[("MP3 files", "*.mp3")]
    )

    # 사용자가 취소하면 종료
    if not file:
        return

    tts = generate_tts(text)
    if not tts:
        root.after(0, lambda: speak_btn.config(state="normal"))
        return
    
    tts.save(file)

# 언어 목록
languages = {  
    "한국어": "ko",
    "영어": "en",
    "중국어(간체)": "zh-CN",
    "중국어 (번체)": "zh-TW",
    "일본어": "ja",
    "프랑스어": "fr",
    "독일어": "de",
    "스페인어": "es",
    "아랍어": "ar",
    "이탈리아어": "it",
    "러시아어": "ru",
    "태국어": "th",
    "폴란드어": "pl",
    "히브리어": "he",
    "베트남어": "vi",
    "힌디어": "hi"
}


# ================== GUI ================== #

root = tk.Tk()
root.title("text to speech converter")
root.geometry("600x480")
root.resizable(0, 0)

#제목
title_label = ttk.Label(root, text="AI 음성 서비스", font=("Arial", 18, "bold"))
title_label.pack(pady=10)

# text_frame
text_frame = tk.Frame(root)
text_frame.pack()

# scrollbar
scrollbar = tk.Scrollbar(text_frame)
scrollbar.pack(side="right", fill="y")

# text_area
text_area = tk.Text(text_frame, height=14, width=80, font=("Arial", 12, "bold"))
text_area.pack(side="left")
text_area.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=text_area.yview)

# Frame for options
options_frame = ttk.Frame(root)
options_frame.pack(pady=10)

# 음성 재생 속도
ttk.Label(options_frame, text="Speed :").grid(row=0, column=0)
speed_var = tk.StringVar(value="fast")
speed_menu = ttk.Combobox(options_frame, textvariable=speed_var, values=["fast", "slow"], width=15, state="readonly")
speed_menu.grid(row=0, column=1, pady=10, padx=10)

ttk.Label(options_frame, text="입력 언어").grid(row=0, column=2, pady=10, padx=10)

# 음성 언어 콤보박스 
input_lang = ttk.Combobox(options_frame, values=list((languages.keys())), state="readonly", width=15)
input_lang.grid(row=0, column=3, pady=10, padx=10)
input_lang.set("영어")


# 버튼 프레임
button_frame = ttk.Frame(root)
button_frame.pack(pady=15)

# 재생 버튼
speak_btn = tk.Button(button_frame, text="Speak", 
                      command=speak_text, 
                      width=10, 
                      height=1, 
                      font=("Times New Roman", 15, "bold"),
                      bg="#049F95", 
                      fg="white")
speak_btn.grid(row=0, column=2, padx=10)

# 저장 버튼
save_btn = tk.Button(button_frame, 
                     text="Save", 
                     command=save_audio, 
                     width=10, 
                     height=1, 
                     font=("Times New Roman", 15, "bold"),
                     bg="#1BA0F3", 
                     fg="white")
save_btn.grid(row=0, column=3, padx=10)


root.mainloop()
