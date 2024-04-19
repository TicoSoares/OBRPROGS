from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub(observe_channels=[1])

estado = 0

cores = {}

motorD = Motor(Port.E)
motorE = Motor(Port.F, Direction.COUNTERCLOCKWISE)

drive = DriveBase(motorE, motorD, wheel_diameter=56, axle_track=112)
drive.settings(200)

sensorA = ColorSensor(Port.D)
sensorB = ColorSensor(Port.C)

forcaBase = 70
erro = 0
integral = 0
ultimo_erro = 0

KP = 5
KI = 0
KD = 0.5

def Pid():
    hub.display.char("P")
    global integral, ultimo_erro  
    erro = sensorA.reflection() - sensorB.reflection()
    proporcional = erro * KP
    integral += erro
    derivado = (erro - ultimo_erro) * KD
    correcao = proporcional + (integral * KI) + derivado
    drive.drive(forcaBase, correcao)

def ChecaVerde():
    verdeverde = False
    if sensorA.color() == Color.GREEN or sensorB.color() == Color.GREEN:
        hub.display.char("V")
        drive.stop()
        if sensorA.color() == Color.GREEN and sensorB.color() != Color.GREEN:
            while sensorA.color() == Color.GREEN or not verdeverde: 
                drive.straight(25)
                if sensorB.color() == Color.GREEN:
                    verdeverde = True
                    break
            if sensorA.color() == Color.BLACK:
                hub.light.on(Color.GREEN)
                drive.straight(200)
                drive.turn(90)
                hub.light.off()
        elif sensorB.color() == Color.GREEN and sensorA.color() != Color.GREEN:
            while sensorB.color() == Color.GREEN or not verdeverde: 
                drive.straight(25)
                if sensorA.color() == Color.GREEN:
                    verdeverde = True
                    break
            if sensorB.color() == Color.BLACK:
                hub.light.on(Color.GREEN)
                drive.straight(200)
                drive.turn(-90)
                hub.light.off()
        if verdeverde:
            while sensorB.color == Color.GREEN and sensorA.color == Color.GREEN : 
                drive.straight(25)
            if sensorA.color() == Color.BLACK and sensorB.color() == Color.BLACK :
                hub.light.on(Color.GREEN)
                drive.turn(180)
                hub.light.off()

while True:
    while hub.buttons.pressed() == Button.CENTER:
        print("AAAAAAA")


    if hub.buttons.pressed() == Button.RIGHT:
        estado = 1
    if estado == 1:
        if hub.buttons.pressed() == Button.LEFT:
            cores["Verde"] = sensorA.color()
    if estado == 0:
        ChecaVerde()
        Pid()
    continue
