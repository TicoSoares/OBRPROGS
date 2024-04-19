from pybricks.hubs import PrimeHub
from pybricks.pupdevices import Motor, ColorSensor, UltrasonicSensor, ForceSensor
from pybricks.parameters import Button, Color, Direction, Port, Side, Stop
from pybricks.robotics import DriveBase
from pybricks.tools import wait, StopWatch

hub = PrimeHub(broadcast_channel=1)

ultra = UltrasonicSensor(Port.A)

while True:
    data = ultra.distance()
    hub.ble.broadcast(data)