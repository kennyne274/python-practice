import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta, date

# 날짜 계산기

# 오늘 날짜
today = date.today()
# 10일 전 날짜
after10 = today + timedelta(days=+10)

def calculate_difference():
    """두 날짜 사이의 일수 차이를 계산해서 결과창에 보여줍니다"""
    try:
        # 입력된 날짜를 datetime 객체로 변환
        date1 = datetime.strptime(entry_date1.get(), "%Y-%m-%d")
        date2 = datetime.strptime(entry_date2.get(), "%Y-%m-%d")
        # 두 날짜 차이 계산
        difference = (date2 - date1).days
        # 엔트리 초기화 후 출력
        entry_result.delete(0, tk.END)
        entry_result.insert(0, f"날짜 차이 : {difference}일")
        # 날짜 형식을 잘못 입력하면 오류 메세지를 보여줍니다
    except:
        messagebox.showerror("오류", "올바른 날짜 형식(YYYY-MM-DD)을 입력하세요")

def calculate_date():
    """기준 날짜로부터 N일 전/후의 날짜를 계산하여 결과창에 보여줍니다"""

    def get_text(num):
        if num < 0:
            return "전" 
        else:
            return "후"
        
    try:
        # 입력된 기준 날짜를 datetime 객체로 변환
        base_date = datetime.strptime(entry_base_date.get(), "%Y-%m-%d")
        days = int(entry_days.get())
        # 미래/과거 날짜 계산
        future_date = base_date + timedelta(days=days)
        # 엔트리 초기화 후 출력
        entry_result2.delete(0, tk.END)
        entry_result2.insert(0, f"{abs(days)}일 {get_text(days)}의 날짜는 {future_date.strftime('%Y-%m-%d')}")
    except:
        messagebox.showerror("오류", "날짜, 또는 일수를 바르게 입력하세요.")
#============================================================
# GUI 
#============================================================
root = tk.Tk()
root.geometry("445x220")
root.title("날짜 계산기")
root.resizable(0, 0)

# 날짜 차이 계산 구간
label_date1 = tk.Label(root, text="첫 번째 날짜 (YYYY-MM-DD):")
label_date1.grid(row=0, column=0, padx=5, pady=5)
entry_date1 = tk.Entry(root)
entry_date1.grid(row=0, column=1, padx=5, pady=5)
entry_date1.insert(0, str(today))

# 날짜 차이 계산 버튼
button_calculate = tk.Button(root, text="날짜 차이 계산", height=3, command=calculate_difference)
button_calculate.grid(row=0, column=2, rowspan=2, padx=5, pady=3)

label_date2 = tk.Label(root, text="두 번째 날짜 (YYYY-MM-DD):")
label_date2.grid(row=1, column=0, padx=5, pady=5)
entry_date2 = tk.Entry(root)
entry_date2.grid(row=1, column=1, padx=5, pady=5)
entry_date2.insert(0, str(after10))

# 계산 결과 입력창
entry_result = tk.Entry(root, justify="right")
entry_result.grid(row=2, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

# 구분선
separator = tk.Label(root, text="")
separator.grid(row=3, column=0, columnspan=3)

# 미래/과거 날짜 계산 구간
label_base_date = tk.Label(root, text="기준 날짜 (YYYY-MM-DDD):")
label_base_date.grid(row=4, column=0, padx=5, pady=5)

entry_base_date = tk.Entry(root)
entry_base_date.grid(row=4, column=1, padx=5, pady=5)
entry_base_date.insert(0, str(today))
label_days = tk.Label(root, text="(+/-) 일수:")
label_days.grid(row=5, column=0, padx=5, pady=5)
entry_days = tk.Entry(root)
entry_days.insert(0, str(10))
entry_days.grid(row=5, column=1, padx=5, pady=5)

#미래/과거 날짜 계산 버튼
button_calculate_future = tk.Button(root, text="미래/과거\n날짜 계산", height=3, command=calculate_date)
button_calculate_future.grid(row=4, column=2, rowspan=2, sticky="ew", padx=5, pady=5)

# 계산 결과 입력창
entry_result2 = tk.Entry(root, justify="right")
entry_result2.grid(row=6, column=0, columnspan=3, sticky="ew", padx=5, pady=5)

root.mainloop()
