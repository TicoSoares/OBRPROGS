from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub()

motorD = Motor(Port.E, Direction.CLOCKWISE)
motorE = Motor(Port.F, Direction.COUNTERCLOCKWISE)
motorG = Motor(Port.C, Direction.CLOCKWISE)

drive = DriveBase(motorE, motorD, wheel_diameter=56, axle_track=112)
drive.settings(200)

sensorA = ColorSensor(Port.A)
sensorB = ColorSensor(Port.B)

ultra = UltrasonicSensor(Port.D)

forcaBase = 50
integral = 0
ultimo_erro = 0

def Pid(kp, ki, kd):
    proporcional = (sensorA.reflection() - sensorB.reflection()) * kp
    integral += erro
    derivado = (erro - ultimo_erro) * kd
    correcao = proporcional + (integral * ki) + derivado

    drive.drive(forcaBase, correcao)

def ChecaVerde():
    verdeverde = False
    if sensorA.color() == Color.GREEN or sensorB.color() == Color.GREEN:
        drive.stop()
        if sensorA.color() == Color.GREEN and sensorB.color() != Color.GREEN:
            while sensorA.color == Color.GREEN or !verdeverde: 
                drive.straight(50)
                if sensorB.color() == Color.GREEN:
                    verdeverde = True
                    break
        else if sensorB.color() == Color.GREEN and sensorA.color() != Color.GREEN:
            while sensorB.color == Color.GREEN or !verdeverde: 
                drive.straight(50)
                if sensorA.color() == Color.GREEN:
                    verdeverde = True
                    break
        if verdeverde:


def ChecaUltra():


while True:
    Pid(5,0,0.5)
    verde()
