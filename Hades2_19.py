from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub(observe_channels=[1])
hub.system.set_stop_button((Button.CENTER, Button.LEFT))

ultra = UltrasonicSensor(Port.A)
sensorE = ColorSensor(Port.C)
sensorD = ColorSensor(Port.D)
motorD = Motor(Port.E)
motorE = Motor(Port.F, Direction.COUNTERCLOCKWISE)
ultra.lights.off()

drive = DriveBase(motorE, motorD, wheel_diameter=32, axle_track=180)
drive.settings(200, 100, 350, 210)

integral = 0
ultimo_erro = 0

querry_estado = 2
estado = 0
ultimo_butao = []
butaoPress = []

hub.speaker.volume(50)

cores = [Color(165, 72, 34),Color(255, 255, 255),Color(192, 11, 52),Color.WHITE]

forcaBase = 200
_KP = 10
_KI = 0
_KD = 0.5

def ColorInRange(sensor, color):
    cormin = Color.NONE
    cormax = Color.NONE
    cormin = Color(cores[color].h - 20, cores[color].s - 20, cores[color].v - 20)
    cormax = Color(cores[color].h + 20, cores[color].s + 20, cores[color].v + 20)
    if sensor.hsv().h < cormax.h and sensor.hsv().h > cormin.h:
        if sensor.hsv().s < cormax.s and sensor.hsv().s > cormin.s:
            if sensor.hsv().v < cormax.v and sensor.hsv().v > cormin.v:
                return True
    return False

def zeraVars():
    ultimo_erro = 0
    integral = 0

def ChechaToque():
    global ultimo_butao,butaoPress,querry_estado, estado, ultimo_erro, integral

    if ultimo_butao != hub.buttons.pressed():
        if len(ultimo_butao) > len(hub.buttons.pressed()):
            for b in ultimo_butao:
                if b not in hub.buttons.pressed():
                    butaoPress.append(b)
    
    ultimo_butao = hub.buttons.pressed()        
        
    if estado == 0:
        if Button.LEFT in butaoPress:
            querry_estado -= 1
            if querry_estado < 1: 
                querry_estado = 2
        elif Button.RIGHT in butaoPress:
            querry_estado += 1
            if querry_estado > 2: 
                querry_estado = 1
        elif Button.CENTER in butaoPress:
            zeraVars()
            estado = querry_estado
            butaoPress = []
            return
        if querry_estado == 1:
            hub.light.on(Color(100, 100, 100))
        else:
            hub.light.on(Color(0, 100, 100))

    elif estado == 1:
        hub.light.on(Color(100, 100, 50))
        if Button.LEFT in butaoPress:
            cores[0] = sensorD.hsv()
            print("Verde: " + str(cores[0]))
        elif Button.RIGHT in butaoPress:
            cores[1] = sensorD.hsv()
            print("Prata: " + str(cores[1]))
        elif Button.CENTER in butaoPress:
            estado = 0
            butaoPress = []
            return
    elif estado == 2:
        hub.light.on(Color(0, 100, 50))
        if Button.CENTER in butaoPress:
            drive.stop()
            estado = 0

    butaoPress = []


def Pid():
    global integral, ultimo_erro  
    erro = sensorE.reflection() - sensorD.reflection()
    proporcional = erro * _KP
    integral += erro
    derivado = (erro - ultimo_erro) * _KD
    correcao = proporcional + (integral * _KI) + derivado
    motorE.run(forcaBase - correcao)
    motorD.run(forcaBase + correcao)

def ChecaUltra():
    if ultra.distance() <= 150:
        drive.settings(-forcaBase)
        drive.straight(300)
        drive.turn(90)
        drive.curve(-200, 180)

def ChecaVerde():
    if ColorInRange(sensorE, 0) or ColorInRange(sensorD, 0):
        hub.speaker.beep(1000, 250)
        drive.settings(200)
        drive.drive(50, 30)

        if ColorInRange(sensorE, 0):
            while True:
                print("esquerda")
                if ColorInRange(sensorD, 0):
                    VerdeVerde()
                    return
                if not ColorInRange(sensorE, 0):
                    break
            if sensorE.reflection() < 30:
                drive.straight(50)
                drive.turn(90)

        elif ColorInRange(sensorD, 0): 
            while True:
                print("direita")
                if ColorInRange(sensorE, 0):
                    VerdeVerde()
                    return
                if not ColorInRange(sensorD, 0):
                    break
            if sensorD.reflection() < 30:
                drive.straight(50)
                drive.turn(-90)

def VerdeVerde():
    print("beco")   
    while not ColorInRange(sensorE, 0) and not ColorInRange(sensorD, 0):
        wait(10)
    drive.stop()
    if ColorInRange(sensorE, 2) or ColorInRange(sensorD, 0):
        drive.straight(200)
        drive.turn(180)

while True:
    ChechaToque()
    if sensorD.reflection() < 50:
        print("preto")
    else:
        print("branco")
    if estado == 2:
        ChecaVerde()
        Pid()
