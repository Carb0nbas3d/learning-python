import turtle
import random


def baum():

    rosi.pensize(random.randint(15,35))
    rosi.pencolor("brown")
    rosi.left(90)
    rosi.forward(random.randint(50,250))
    rosi.pencolor("green")
    rosi.fillcolor("green")
    rosi.right(90)
    rosi.pensize(1)
    rosi.begin_fill()
    rosi.circle(random.randint(45,150))
    rosi.end_fill()


rosi=turtle.Turtle()
rosi.speed(0)

for x in range(100):
	rosi.up()
	rosi.goto(random.randint(-700,700),random.randint(-400,400))
	rosi.down()
	baum()

turtle.exitonclick()
