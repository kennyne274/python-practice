import random
import time

# 초보용 가위바위보 게임 프로젝트

choices = ["가위", "바위", "보"]

wins = 0
losses = 0
draws = 0

print("="*30)
print("가위 바위 보 게임을 시작합니다")
print("게임을 중단하고 싶으면 'q'를 입력하세요.")
print("="*30)

# 게임 진행 구간
while True:

    try:
        user = input("가위, 바위, 보! : ").strip()
        if user == 'q' or user == 'Q': # 'q', 혹은 'Q'를 입력하면 게임 종료
            print("게임 종료") 
            break
    
        if user not in choices:
            raise ValueError # 가위, 바위, 보가 아니면 ValueError를 발생시킴

    except ValueError:
        print("가위, 바위, 보 중에 하나만 입력하세요.")
        print("종료를 원하면 q를 입력하세요.")
        continue
    

    computer = random.choice(choices)

    time.sleep(1)
    print(f"당신의 선택 {user}")
    time.sleep(1)
    print(f"컴퓨터의 선택 {computer}")
    time.sleep(1)
    if user == computer:
        print("비겼습니다 🤔 한판 더?")
        draws += 1
    elif(user == "가위" and computer == "보") or \
        (user == "바위" and computer == "가위") or\
        (user == "보" and computer == "바위"):
        print("당신이 이겼습니다 😓")
        wins += 1
    else:
        print("컴퓨터의 승리 😂 약 오르지?")
        losses += 1

# 통계 출력 및 승률 계산 
total = wins + draws + losses
if total > 0:
    wins_rate = wins/total * 100  # 승률 계산
else:
    wins_rate = 0

print("="*30)
print(f"승: {wins} | 패: {losses} | 무: {draws}")
print(f"승률 {wins_rate:.2f}%")
print("="*30)

