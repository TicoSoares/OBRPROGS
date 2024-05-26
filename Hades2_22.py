from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub(observe_channels=[1])
hub.system.set_stop_button((Button.CENTER, Button.LEFT))
hub.speaker.volume(50)

sensorA = ColorSensor(Port.A)
sensorB = ColorSensor(Port.B)
ultra = UltrasonicSensor(Port.C)
# sensorC = ColorSensor(Port.C)
# sensorD = ColorSensor(Port.D)
motorD = Motor(Port.E)
motorE = Motor(Port.F, Direction.COUNTERCLOCKWISE)
ultra.lights.off()

drive = DriveBase(motorE, motorD, wheel_diameter=36, axle_track=131)
drive.settings(200, 100, 350, 210)
drive.settings()

integral = 0
ultimo_erro = 0

querry_estado = 2
estado = 0
ultimo_botao = []
botaoPress = []

cores = [Color(165, 72, 34),Color(255, 255, 255),Color(192, 11, 52),Color.WHITE]

forcaBase = 200
_KP = 10
_KI = 0
_KD = 0.5

def ColorInRange(sensor, color, rangee = 20):
    cormin = cormax = Color.NONE
    # cormin = Color.NONE
    # cormax = Color.NONE
    cormin = Color(cores[color].h - rangee, cores[color].s - rangee, cores[color].v - rangee)
    cormax = Color(cores[color].h + rangee, cores[color].s + rangee, cores[color].v + rangee)
    if sensor.hsv().h < cormax.h and sensor.hsv().h > cormin.h:
        if sensor.hsv().s < cormax.s and sensor.hsv().s > cormin.s:
            if sensor.hsv().v < cormax.v and sensor.hsv().v > cormin.v:
                return True
    return False

def zeraVars():
    ultimo_erro = 0
    integral = 0

def ChechaToque():
    global ultimo_botao,botaoPress,querry_estado, estado

    if ultimo_botao != hub.buttons.pressed():
        if len(ultimo_botao) > len(hub.buttons.pressed()):
            for b in ultimo_botao:
                if b not in hub.buttons.pressed():
                    botaoPress.append(b)
    
    ultimo_botao = hub.buttons.pressed()        
        
def ChangeState():
    global botaoPress,querry_estado, estado

    if estado == 0:
        if Button.LEFT in botaoPress:
            querry_estado -= 1
            if querry_estado < 1: 
                querry_estado = 2
        elif Button.RIGHT in botaoPress:
            querry_estado += 1
            if querry_estado > 2: 
                querry_estado = 1
        elif Button.CENTER in botaoPress:
            zeraVars()
            estado = querry_estado
            botaoPress = []
            return
        if querry_estado == 1:
            hub.light.on(Color(100, 100, 100))
        else:
            hub.light.on(Color(0, 100, 100))

    elif estado == 1:
        hub.light.on(Color(100, 100, 50))
        if Button.LEFT in botaoPress:
            cores[0] = sensorB.hsv()
            print("Verde: " + str(cores[0]))
        elif Button.RIGHT in botaoPress:
            cores[1] = sensorB.hsv()
            print("Prata: " + str(cores[1]))
        elif Button.CENTER in botaoPress:
            estado = 0
            botaoPress = []
            return
            
    elif estado == 2:
        hub.light.on(Color(0, 100, 50))
        if Button.CENTER in botaoPress:
            drive.stop()
            estado = 0

    botaoPress = []

def Pid():
    global integral, ultimo_erro  
    erro = sensorA.reflection() - sensorB.reflection()
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

def ChecaVerde():
    if ColorInRange(sensorA, 0) or ColorInRange(sensorB, 0):
        hub.speaker.beep(1000, 200)
        drive.drive(50, 30)

        if ColorInRange(sensorA, 0):
            print("esquerda")
            while True:
                if ColorInRange(sensorB, 0):
                    VerdeVerde()
                    return
                if not ColorInRange(sensorA, 0):
                    wait(150)
                    if sensorA.reflection() < 30:
                        drive.straight(50)
                        drive.turn(90)
                    break

        elif ColorInRange(sensorB, 0): 
            print("direita")
            while True:
                if ColorInRange(sensorA, 0):
                    VerdeVerde()
                    return
                if not ColorInRange(sensorB, 0):
                    wait(150)
                    if sensorB.reflection() < 30:
                        drive.straight(50)
                        drive.turn(-90)
                    break

def VerdeVerde():
    print("beco")   
    while not ColorInRange(sensorA, 0) and not ColorInRange(sensorB, 0):
        wait(10)
    drive.stop()
    if ColorInRange(sensorA, 2) or ColorInRange(sensorB, 0):
        drive.straight(200)
        drive.turn(180)

###########################################################
while True:
    bateria = (hub.battery.voltage() * hub.battery.current()) / 1000
    #print(bateria / 21)
    ChechaToque()
    ChangeState()

    if estado == 2:
        ChecaVerde()
        Pid()
