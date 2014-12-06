from time import sleep
from celery import Celery
import serial

app = Celery('tasks', broker='redis://localhost')
port = serial.Serial("/dev/ttyAMA0", baudrate=4800, timeout=1.0)

@app.task
def readSerial():
    while True:
        data = port.readline()
        if data:
            print ("\nreceived:\n"+data[:-1])
            sleep(0.1)
