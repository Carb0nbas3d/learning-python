import turtle
import random
print("hallo")

#https://docs.python.org/3/library/turtle.html#turtle.circle


rosi=turtle.Turtle()
rosi.shape("turtle")
#rosi.forward(100)
#for x in range(5):
#    rosi.left(90)
#    rosi.forward(50)
#    rosi.right(90)
#   rosi.forward(50)
rosi.speed(0)
#kreis
for x in range (108):
    rosi.circle(15+x*1.5)
    rosi.left (10)

turtle.exitonclick()

