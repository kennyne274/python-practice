from turtle import*
import time
import random

"""뱀이 먹이를 먹으면 점수가 올라가는 게임이야. 먹이를 먹을 수록 점수가 올라가고 
뱀의 몸이 길어져.자기 몸에 부딪히면 게임이 끝나."""

# 방향키 입력 함수

def up():
    if snakes[0].heading() != 270:
        snakes[0].setheading(90)

def down():
    if snakes[0].heading() != 90:
        snakes[0].setheading(270)

def right():
    if snakes[0].heading() != 180:
        snakes[0].setheading(0)

def left():
    if snakes[0].heading() != 0:
        snakes[0].setheading(180)

# 무작위 좌표 생성
def rand_pos():
    rand_x = random.randint(-250, 250)
    rand_y = random.randint(-250, 250)
    return rand_x, rand_y

# 점수 업데이트
def score_update():
    global score
    score += 1
    score_count.clear()
    score_count.write(f"점수 : {score}", font = ("Arial", 15, "bold"))

# 뱀 몸통 만들기
def create_snake(pos):
    snake_body = Turtle()
    snake_body.shape("square")
    snake_body.color("orange")
    snake_body.up()
    snake_body.goto(pos)
    snakes.append(snake_body)

def game_over():
    game_over_text = Turtle()
    game_over_text.hideturtle()
    game_over_text.penup()
    game_over_text.goto(0, 0)
    game_over_text.write("GAME OVER!", align="center", font=("Arial", 30, "bold"))

screen = Screen()
screen.setup(600, 600)
screen.title("Snake Game")
screen.bgcolor("olive")
screen.tracer(0)

start_pos = [(0,0), (-20,0), (-40,0)]
snakes = []

score = 0

for pos in start_pos:
    create_snake(pos)



# 먹이
food = Turtle()
food.shape("circle")
food.color("red")
food.up()
food.speed(0)
food.goto(rand_pos())

# 점수 표시
score_count = Turtle()
score_count.ht()
score_count.up()
score_count.goto(-270, 250)
score_count.write(f"SCORE : {score}", font = ("Arial", 15, "bold"))

screen.listen()
screen.onkeypress(up, "Up")
screen.onkeypress(down, "Down")
screen.onkeypress(left,"Left")
screen.onkeypress(right, "Right")

# 게임 진행 구간
game_on = True
while game_on:
    screen.update()
    time.sleep(0.1)
    for i in range(len(snakes) -1, 0, -1):
        snakes[i].goto(snakes[i-1].pos())
    snakes[0].forward(20)

    if snakes[0].distance(food) < 15:
        score_update()
        food.goto(rand_pos())
        create_snake(snakes[-1].pos())

    
    head_x = snakes[0].xcor()
    head_y = snakes[0].ycor()
    
    # X축: 왼쪽 끝 → 오른쪽 끝, 오른쪽 끝 → 왼쪽 끝
    if head_x > 290:
        snakes[0].setx(-290)
    elif head_x < -290:
        snakes[0].setx(290)
    
    # Y축: 위쪽 끝 → 아래쪽 끝, 아래쪽 끝 → 위쪽 끝
    if head_y > 290:
        snakes[0].sety(-290)
    elif head_y < -290:
        snakes[0].sety(290)

    #  자기 몸에 부딪히면 게임 오버 (종료 조건)
    for body in snakes[1:]:
        if snakes[0].distance(body) < 10:
            game_on = False
            game_over()
            break


screen.exitonclick()
