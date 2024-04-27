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
ultimo_botao = []
botaoPress = []

hub.speaker.volume(100)

cores = [0,0,0,0]

forcaBase = 100
KP = 5
KI = 0
KD = 0.5

def zeraVars():
    erro = 0
    ultimo_erro = 0
    integral = 0

def ChechaToque():
    global ultimo_botao ,botaoPress ,querry_estado, estado, erro, ultimo_erro, integral

    #Identifica quais botões estão sendo apertados
    botao = ()
    while not botao:
        botao = hub.buttons.pressed()
        wait(10)
    
    # Wait for the button to be released.
    while hub.buttons.pressed():
        wait(10)

    #Troca a cor pra diferenciar as programações
    if querry_estado == 0:
        hub.light.on(Color.GREEN)
    elif querry_estado == 1:
        hub.light.on(Color.BLUE)
    else:
        hub.light.on(Color.RED)
        
    if estado == 0:
        if Button.LEFT in botao:
            querry_estado -= 1
            if querry_estado < 0: 
                querry_estado = 2
        elif Button.RIGHT in botao:
            querry_estado += 1
            if querry_estado > 2: 
                querry_estado = 0
        elif Button.CENTER in botao:
            zeraVars()
            estado = querry_estado
            botao = []
            return

    elif estado == 1:
        if Button.LEFT in botao:
            cores[0] = sensorD.hsv()
        elif Button.RIGHT in botao:
            cores[1] = sensorD.hsv()
        elif Button.CENTER in botao:
            estado = 0
            cores[2] = Color.BLACK
            cores[3] = Color.WHITE
            sensorD.detectable_colors(cores)
            sensorE.detectable_colors(cores)
            botao = []
            return
    elif estado == 2:
        if Button.CENTER in botao:
            drive.stop()
            estado = 0

    botao = []


def Pid():
    global integral, ultimo_erro  
    drive.settings(500)
    erro = sensorE.reflection() - sensorD.reflection()
    proporcional = erro * KP
    integral += erro
    derivado = (erro - ultimo_erro) * KD
    correcao = proporcional + (integral * KI) + derivado
    motorE.run(forcaBase - correcao)
    motorD.run(forcaBase + correcao)

def ChecaUltra():
    if ultra.distance() <= 150:
        drive.settings(-forcaBase)
        drive.straight(300)
        drive.turn(90)
        drive.curve(-200, 180)

def ChecaVerde():
    if sensorE.color() == cores[0] or sensorD.color() == cores[0]:
        drive.drive(200, 5)

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
    print(str(querry_estado) + "q")
    print(estado)
    ChechaToque()
    if estado == 2:
        ChecaVerde()
        Pid()
    continue
