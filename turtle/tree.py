# 재귀나무

import turtle as t
import random

size = 110
t.bgcolor("black")
t.color("peru")
t.speed(0)
t.left(90)
t.penup()
t.goto(0, -250)
t.pendown()
t.hideturtle()

# 나무 그리기
def tree(i):
    if i < 10:
        t.dot(10)
        return
    else:
    
        t.pensize((i/12))
        t.forward(i)
       
        angle = random.uniform(20, 35)
        length = random.uniform(0.7, 0.85)

        # 왼쪽 가지
        t.left(angle)
        tree(i * length)

        # 오른쪽 가지
        t.right(angle * 2)
        tree(i * length)

        # Return to previous branch position
        t.left(angle)
        t.backward(i)

tree(size)
t.done()
