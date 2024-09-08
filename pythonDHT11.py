from vpython import *
import numpy as np
import serial

arduinoData = serial.Serial("com3", 115200)  # processing arduino data at given baud rate
sleep(1)

scene.center = vector(5, 0, 0)  # configuring size of visualization's frame
scene.width = 1050
scene.height = 600

boxX = 10
boxY = 6
boxZ = 0.4 

offsetRight = boxX / 2 + 2
arrowLength = boxY - 2
arrowThickness = 0.15
arrowZoffset = 0.5

tickL = 0.6
tickW = 0.1
tickH = 0.1 

# following code initializes the visualizations for humidity meter
systemLabel = label(text = "TEMPERATURE & HUMIDITY METER", height = 50, box = False, pos = vector(offsetRight - 1.4, 3.2, 2), color = color.white, font = "serif")

myCase = box(size = vector(boxX + 1, boxY + 0.8, boxZ), color = color.white, pos = vector(offsetRight, -0.5, boxZ / 2))

myArrow = arrow(length = arrowLength, color = color.red, shaftwidth = arrowThickness, pos = vector(offsetRight, (-boxY / 2) * 0.9, arrowZoffset))
mySphere = sphere(color = color.red, radius = 0.18, pos = vector(offsetRight, (-boxY / 2) * 0.9, arrowZoffset))

digValueHumidity = label(text = "0 %", height = 20, box = False, pos = vector(offsetRight - 0.18, -3, 1.3))

for angle in np.linspace(0, np.pi, 11):  # creating major tick marks for humidity meter
    tickMajor = box(pos = vector(1.1 * arrowLength * np.cos(angle) + offsetRight, 1.1 * arrowLength * np.sin(angle) - 0.9 * (boxY / 2), arrowZoffset), size = vector(tickL, tickW, tickH), color = color.black, axis = vector(arrowLength * np.cos(angle), arrowLength * np.sin(angle), 0))

tickF = 0.6
for angle in np.linspace(0, np.pi, 51):  # creating minor tick marks for humidity meter
    tickMinor = box(pos = vector(1.1 * arrowLength * np.cos(angle) + offsetRight, 1.1 * arrowLength * np.sin(angle) - 0.9 * (boxY / 2), arrowZoffset), size = vector(tickF * tickL, tickF * tickW, tickF * tickH), color = color.black, axis = vector(arrowLength * np.cos(angle), arrowLength * np.sin(angle), 0), opacity = 0.95)
    
num = 0
for angle in np.linspace(0, np.pi, 11):  # creating numerical labels for humidity meter
    lab = text(text = str(num), pos = vector(1.2 * arrowLength * np.cos(angle) + offsetRight, 1.2 * arrowLength * np.sin(angle) - 0.9 * (boxY / 2), arrowZoffset), axis = vector(arrowLength * np.cos(angle - np.pi / 2), arrowLength * np.sin(angle - np.pi /2), 0), color = color.black, height = 0.35, align = "center")
    num += 10


# following code initializes the visualizations for temperature meter
bulb = sphere(color = color.red, radius = 1, pos = vector(0, -3, 0))
cyl = cylinder(color = color.red, radius = 0.6, length = 6, axis = vector(0, 1, 0), pos = vector(0, -3, 0))

bulbGlass = sphere(radius = 1.2, color = color.white, opacity = 0.25, pos = vector(0, -3, 0))
cylGlass = cylinder(radius = 0.8, color = color.white, opacity = 0.25, length = 6, axis = vector(0, 1, 0), pos = vector(0, -3, 0))
digValueTemp = label(text = "20", height = 20, box = False, pos = vector(0.5, -2.5, 1.5))


for temp in range(0, 40, 5):  # creating tick marks for temperature meter
    tickPos = (5 / 35) * temp + 1
    tick = cylinder(radius = 0.7, color = color.black, length = 0.1, axis = vector(0, 1, 0), pos = vector(0, tickPos - 3, 0))
    label = text(text = str(temp), color = color.white, pos = vector(-1.65, tickPos - 3, 0), height = 0.3)

while True:  
    while (arduinoData.inWaiting() == 0):  # waits for arduino data
        pass
    dataPacket = arduinoData.readline()
    dataPacket = str(dataPacket, "utf-8")
    dataPacket = dataPacket.strip("\r\n")
    dataPacket = dataPacket.split(",")
    temp = float(dataPacket[0])
    hum = float(dataPacket[1])

    len = (4.5 / 35) * temp + 1.5
    cyl.length = len

    theta = (np.pi / 100) * hum
    myArrow.axis = vector(arrowLength * np.cos(theta), arrowLength * np.sin(theta), 0)

    digValueTemp.text = str(temp) + "°C"
    digValueHumidity.text = str(hum) + "%"
    
