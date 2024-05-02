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

drive = DriveBase(motorE, motorD, wheel_diameter=56, axle_track=112)

erro = 0
integral = 0
ultimo_erro = 0

querry_estado = 0
estado = 0
ultimo_butao = []
butaoPress = []

hub.speaker.volume(100)

cores = [Color.NONE,Color.NONE,Color.BLACK,Color.WHITE]

forcaBase = 100
KP = 5
KI = 0
KD = 0.5

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
    erro = 0
    ultimo_erro = 0
    integral = 0

def ChechaToque():
    global ultimo_butao,butaoPress,querry_estado, estado, erro, ultimo_erro, integral

    if ultimo_butao != hub.buttons.pressed():
        if len(ultimo_butao) > len(hub.buttons.pressed()):
            for b in ultimo_butao:
                if b not in hub.buttons.pressed():
                    butaoPress.append(b)
    
    ultimo_butao = hub.buttons.pressed()

    if querry_estado == 0:
        hub.light.on(Color.GREEN)
    elif querry_estado == 1:
        hub.light.on(Color.BLUE)
    else:
        hub.light.on(Color.RED)
        
    if estado == 0:
        if Button.LEFT in butaoPress:
            querry_estado -= 1
            if querry_estado < 0: 
                querry_estado = 2
        elif Button.RIGHT in butaoPress:
            querry_estado += 1
            if querry_estado > 2: 
                querry_estado = 0
        elif Button.CENTER in butaoPress:
            zeraVars()
            estado = querry_estado
            butaoPress = []
            return

    elif estado == 1:
        if Button.LEFT in butaoPress:
            cores[0] = sensorD.hsv()
        elif Button.RIGHT in butaoPress:
            cores[1] = sensorD.hsv()
        elif Button.CENTER in butaoPress:
            estado = 0
            butaoPress = []
            return
    elif estado == 2:
        if Button.CENTER in butaoPress:
            drive.stop()
            estado = 0

    butaoPress = []


def Pid():
    global integral, ultimo_erro  
    erro = sensorE.reflection() - sensorD.reflection()
    proporcional = erro * KP
    integral += erro
    derivado = (erro - ultimo_erro) * KD
    correcao = proporcional + (integral * KI) + derivado
    motorE.run(forcaBase - correcao)
    motorD.run(forcaBase + correcao)
    #drive.drive(forcaBase, correcao)

def ChecaUltra():
    if ultra.distance() <= 150:
        drive.settings(-forcaBase)
        drive.straight(300)
        drive.turn(90)
        drive.curve(-200, 180)

def ChecaVerde():
    if ColorInRange(sensorE, 0) or ColorInRange(sensorD, 0):
        drive.settings(200)
        drive.drive(200, 5)

        if ColorInRange(sensorE, 0):
            while not ColorInRange(sensorE, 0):
                if ColorInRange(sensorD, 0):
                    VerdeVerde()
                    return
                wait(10)
            drive.stop()
            if ColorInRange(sensorE, 2):
                drive.straight(200)
                drive.turn(-90)

        elif ColorInRange(sensorD, 0):         
            while not ColorInRange(sensorD, 0):
                if ColorInRange(sensorE, 0):
                    VerdeVerde()
                    return
                wait(10)
            drive.stop()
            if ColorInRange(sensorD, 0):
                drive.straight(200)
                drive.turn(90)

def VerdeVerde():
    while not ColorInRange(sensorE, 0) and not ColorInRange(sensorD, 0):
        wait(10)
    drive.stop()
    if ColorInRange(sensorE, 2) or ColorInRange(sensorD, 0):
        drive.straight(200)
        drive.turn(180)

while True:
    ChechaToque()
    if estado == 2:
        ChecaVerde()
        Pid()
    continue
