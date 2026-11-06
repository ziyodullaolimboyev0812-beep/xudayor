import os
import sys
import cv2; print(cv2._version
import turtle

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE = os.path.join(BASE_DIR, "spiderman.png")

img = cv2.imread(IMAGE, cv2.IMREAD_COLOR)

if img is None:
    print(f"Image not found: {IMAGE}")
    print("Place the image in the same folder as this script.")
    sys.exit()

# Resize
height = 700
ratio = height / img.shape[0]
width = int(img.shape[1] * ratio)
img = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Threshold
_, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

# Contours
contours, _ = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_NONE
)

# Filter small noise
contours = [c for c in contours if cv2.contourArea(c) > 15]
contours = sorted(contours, key=cv2.contourArea, reverse=True)

if not contours:
    print("No contours found. Try adjusting the threshold value.")
    sys.exit()

# Turtle setup
screen = turtle.Screen()
screen.bgcolor("white")
screen.setup(width=900, height=700)
screen.setworldcoordinates(-width / 2, -height / 2, width / 2, height / 2)
screen.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.pensize(2)
pen.color("black")
pen.hideturtle()

# Draw contours
for contour in contours:
    if len(contour) == 0:
        continue

    pen.penup()
    start_x = contour[0][0][0] - width / 2
    start_y = height / 2 - contour[0][0][1]
    pen.goto(start_x, start_y)
    pen.pendown()

    for point in contour:
        x = point[0][0] - width / 2
        y = height / 2 - point[0][1]
        pen.goto(x, y)

screen.update()
screen.exitonclick()