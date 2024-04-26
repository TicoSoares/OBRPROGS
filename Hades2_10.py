from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub(observe_channels=[1])

ultra = UltrasonicSensor(Port.A)
toque = ForceSensor(Port.B)
sensorE = ColorSensor(Port.C)
sensorD = ColorSensor(Port.D)
motorD = Motor(Port.E)
motorE = Motor(Port.F, Direction.COUNTERCLOCKWISE)
ultra.lights.off()

drive = DriveBase(motorE, motorD, wheel_diameter=56, axle_track=112)

erro = 0
integral = 0
ultimo_erro = 0

toqueTimer = StopWatch()
toqueTimer.pause()
toqueTimer.reset()
waitToRelease = False

estado = 0
hub.speaker.volume(100)

cores = []

forcaBase = 70
KP = 5
KI = 0
KD = 0.5

def ChechaToque():
    global waitToRelease, estado, erro, ultimo_erro, integral
    if toque.pressed():
        if not waitToRelease:
            toqueTimer.resume()
        else:
            toqueTimer.pause()
            toqueTimer.reset()
        if toqueTimer.time >= 1000:
            if estado == 2:
                hub.speaker.beep(1020, 250)
                waitToRelease = True
                estado = 0
                return
        elif toqueTimer.time >= 500:
            if estado == 0:
                hub.speaker.beep(1020, 250)
                waitToRelease = True
                estado = 2
                return

    elif not toque.pressed() and toqueTimer.time > 0:
        if estado == 0:
            estado = 1

        elif estado == 1:
            drive.stop()
            estado, erro, ultimo_erro, integral = 0

        elif estado == 2:
            if toqueTimer.time >= 500:
                #anota cor prata
                cores[1] = sensorD.hsv()
            else:
                #anota cor verde
                cores[0] = sensorD.hsv()
            cores[2] = Color.BLACK
            cores[3] = Color.WHITE
            sensorD.detectable_colors(cores)
            sensorE.detectable_colors(cores)

        waitToRelease = False
        toqueTimer.pause()
        toqueTimer.reset()


    if estado == 0:
        ultra.lights.off()
    elif estado == 1:
        sensorE.lights.on()
        ultra.lights.on([100, 0, 100, 0])
    else:
        sensorE.lights.off()
        ultra.lights.on(100)

def Pid():
    hub.display.char("P")
    global integral, ultimo_erro  
    erro = sensorA.reflection() - sensorB.reflection()
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
    if sensorE.color() == cores[0] or sensorD.color() == cores[0]:
        hub.display.char("V")
        drive.settings(200)
        drive.drive(200)

        if sensorE == cores[0]:
            while not sensorE.color() == cores[0]:
                if sensorD.color() == cores[0]:
                    VerdeVerde()
                    return
                wait(10)
            drive.stop()
            if sensorE.color() == Color.BLACK:
                drive.straight(200)
                drive.turn(-90)

        elif sensorD == cores[0]:         
            while not sensorD.color() == cores[0]:
                if sensorE.color() == cores[0]:
                    VerdeVerde()
                    return
                wait(10)
            drive.stop()
            if sensorD.color() == Color.BLACK:
                drive.straight(200)
                drive.turn(90)

def VerdeVerde():
    while not sensorE.color() == cores[0] and not sensorD.color() == cores[0]:
        wait(10)
    drive.stop()
    if sensorE.color() == Color.BLACK or sensorD.color() == Color.BLACK :
        drive.straight(200)
        drive.turn(180)
    
while True:
    ChechaToque()
    if estado == 1:
        ChecaVerde()
        Pid()
    continue
