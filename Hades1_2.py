from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub(observe_channels=[1])

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

while True:
    #Pid(5,0,0.5)
    proporcional = (sensorA.reflection() - sensorB.reflection()) * KP
    integral += erro
    derivado = (erro - ultimo_erro) * KD
    correcao = proporcional + (integral * KI) + derivado

    data = hub.ble.observe(1) 
    print(data)
    drive.drive(forcaBase, correcao)
