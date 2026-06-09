# tkinter로 만든 다국어 번역기 
# 다양한 언어로 번역이 가능하며 자동으로 언어를 감지하여 번역하는 기능을 추가했습니다.
# 추가로 번역하고 싶은 코드는 딕셔너리 안에 언어 코드를 직접 넣어주세요.
# 구글 translator 기능 사용

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# deep-translator에서 구글 번역기 불러오기
# pip install deep-translator -> 명령 프롬프트에서 설치
from deep_translator import GoogleTranslator

#  번역 함수
def translate():
    try:
        input_str = input_text.get("1.0", "end").strip()
        # 입력이 없으면 경고 메세지 띄우고 리턴    
        if not input_str:
            messagebox.showwarning("경고", "텍스트를 입력해주세요!")
            return
            
            # 선택한 언어 코드 가져오기
        source_lang = languages[input_lang.get()]
        target_lang = languages[output_lang.get()]
        # 입력 언어와 출력 언어과 같으면 경고 메시지 띄우고 리턴
        if source_lang == target_lang:
            messagebox.showinfo("알림", "원본 언어와 번역할 언어가 같아요!")
            return
            
            # 번역 실행
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(input_str)
        
        # 결과 보여주기
        output_text.delete("1.0", "end")
        output_text.insert("1.0", translated)

    # 예외처리
    except KeyboardInterrupt:
        messagebox.showwarning("오류", "프로그램을 종료합니다.")
    except ConnectionError:
        messagebox.showerror("오류", "인터넷 연결을 확인하세요.")
    except Exception as e:
        messagebox.showwarning("오류", "알 수 없는 오류.")

    
# 삭제 함수
def delete():
    input_text.delete(1.0, tk.END)
    output_text.delete(1.0, tk.END)

# 객체 생성
root = tk.Tk()
root.title("다국어 번역기")
root.geometry("620x630")
root.resizable(False, False)

# 번역 가능 언어 목록
languages = {  
    "자동 감지": "auto",
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

languages2 = {  
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

tk.Label(root, text="입력 언어").place(x=30, y=20)

# 입력 언어 콤보박스 
input_lang = ttk.Combobox(root, values=list((languages.keys())), state="readonly", width=22)
input_lang.place(x=130, y=20)
input_lang.set("자동 감지")

tk.Label(root, text="출력 언어").place(x=30, y=60)

# 출력 언어 콤보박스
output_lang = ttk.Combobox(root, values=list(languages2.keys()), state="readonly", width=22)
output_lang.place(x=130, y=60)
output_lang.set("한국어")



tk.Label(root, text="번역할 텍스트").place(x=30, y=110)


input_frame = tk.Frame(root)
input_frame.place(x=30, y=140)

# 번역을 할 문장을 입력 텍스트
input_text = tk.Text(
    input_frame,
    width=69,
    height=9,
    font=("맑은 고딕", 11)
)
input_text.pack(side="left")
# 입력창 스크롤바 생성 및 배치
input_scroll = tk.Scrollbar(input_frame)
input_scroll.pack(side="right", fill="y")

input_text.config(yscrollcommand=input_scroll.set)
input_scroll.config(command=input_text.yview)
tk.Label(root, text="번역 결과").place(x=30, y=340)

#번역한 문장을 입력하는 텍스트
output_frame = tk.Frame(root)
output_frame.place(x=30, y=370)

output_text = tk.Text(
    output_frame,
    width=69,
    height=9,
    font=("맑은 고딕", 11),
    wrap = "word"
)
output_text.pack(side="left")
#출력창 스크롤바 생성 및 배치
output_scroll = tk.Scrollbar(output_frame)
output_scroll.pack(side="right", fill="y")

output_text.config(yscrollcommand=output_scroll.set)
output_scroll.config(command=output_text.yview)


# 번역, 리셋 선택 버튼
btn1 = tk.Button(root, text="번역", width=10, height=1, command=translate)
btn1.place(x=220, y=575)
btn2 = tk.Button(root, text="리셋", width=10, height=1, command=delete)
btn2.place(x=320, y=575)

root.mainloop()
