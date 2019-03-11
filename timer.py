#!/usr/bin/python
# -*- coding: utf-8 -*-
import schedule
import time
import RPi.GPIO as GPIO #Para controlar los pines de entrada y salida
import threading
from pad4pi import rpi_gpio

GPIO.setmode(GPIO.BCM) #Para usar números de pin de placa y no del procesador
GPIO.setwarnings(False)

#Keypad
KEYPAD = [
         [1,2,3,':'],
         [4,5,6,'S'],
         [7,8,9,'N'],
         ['*',0,'#','D']
         ]

row_pins = [4,14,15,17]
column_pins = [18,27,22]

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=KEYPAD, row_pins=row_pins, col_pins=column_pins)

def printKey(key):
    if key==1:
        print("Se ha seleccionado la opción", option,", riego 1.")
        time.sleep(1)
        exit_1.set()
        exit_2.clear()
        t_1=threading.Thread(target=run_schedule_1, args=(exit_1,))
        t_1.start()

    elif key==2:
        print("Se ha seleccionado la opción", option,", riego 2.")
        time.sleep(1)
        exit_1.clear()
        exit_2.set()
        t_2=threading.Thread(target=run_schedule_2, args=(exit_2,))
        t_2.start()
    GPIO.cleanup()

keypad.registerKeyPressHandler(printKey)
#Configuración de pines GPIO

valve_1= 5
valve_2= 6
valve_3= 13
valve_4= 19
valve_5= 26
valve_6= 12
valve_7= 16
valve_8= 20
main_valve= 21

button_1=25
button_2=24

reset= 23

GPIO.setup(valve_1, GPIO.OUT)
GPIO.setup(valve_2, GPIO.OUT)

GPIO.setup(25, GPIO.IN, pull_up_down=PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down=PUD_DOWN)

GPIO.setup(reset, GPIO.IN, pull_up_down=PUD_DOWN)

state_1= GPIO.input(25)
state_2= GPIO.input(24)

#Funciones de abrir y cerrar válvulas

def open_valve():
    print("Abriendo válvulas")
    GPIO.output(valve_1,1)
    GPIO.output(valve_2,1)
    GPIO.output(valve_3,1)
    GPIO.output(valve_4,1)
    GPIO.output(valve_5,1)
    GPIO.output(valve_6,1)
    GPIO.output(valve_7,1)
    GPIO.output(valve_8,1)
    GPIO.output(main_valve,1)

def close_valve():
    print("close")
    GPIO.output(valve_1,0)
    GPIO.output(valve_2,0)
    GPIO.output(valve_3,0)
    GPIO.output(valve_4,0)
    GPIO.output(valve_5,0)
    GPIO.output(valve_6,0)
    GPIO.output(valve_7,0)
    GPIO.output(valve_8,0)
    GPIO.output(main_valve,0)

#Horario del timer

on_1 = ["06:00", "06:15", "06:30", "06:45", "07:00", "07:15", "07:30", "07:45",
            "08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45",
            "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45",
            "16:00", "16:15", "16:30", "16:45", "17:00"]
off_1 = ["06:01", "06:16", "06:31", "06:46", "07:01", "07:16", "07:31", "07:46",
            "08:01", "08:16", "08:31", "08:46", "09:01", "09:16", "09:31", "09:46",
            "10:01", "10:16", "10:31", "10:46", "11:01", "11:16", "11:31", "11:46",
            "12:01", "12:16", "12:31", "12:46", "13:01", "13:16", "13:31", "13:46",
            "14:01", "14:16", "14:31", "14:46", "15:01", "15:16", "15:31", "15:46",
            "16:01", "16:16", "16:31", "16:46", "17:01"]
on_2 = ["06:00", "06:15", "06:30", "06:45", "07:00", "07:15", "07:30", "07:45",
            "08:00", "08:15", "08:30", "08:45", "09:00", "09:15", "09:30", "09:45",
            "10:00", "10:15", "10:30", "10:45", "11:00", "11:15", "11:30", "11:45",
            "12:00", "12:15", "12:30", "12:45", "13:00", "13:15", "13:30", "13:45",
            "14:00", "14:15", "14:30", "14:45", "15:00", "15:15", "15:30", "15:45",
            "16:00", "16:15", "16:30", "16:45", "17:00"]
off_2 = ["06:02", "06:17", "06:32", "06:47", "07:02", "07:17", "07:32", "07:47",
            "08:02", "08:17", "08:32", "08:47", "09:02", "09:17", "09:32", "09:47",
            "10:02", "10:17", "10:32", "10:47", "11:02", "11:17", "11:32", "11:47",
            "12:02", "12:17", "12:32", "12:47", "13:02", "13:17", "13:32", "13:47",
            "14:02", "14:17", "14:32", "14:47", "15:02", "15:17", "15:32", "15:47",
            "16:02", "16:17", "16:32", "16:47", "17:02"]

def load_schedule(on_times, off_times):

    for t in on_times:
        schedule.every(1).dat.at(t).do(open_valve)
    for t in off_times:
        schedule.every(1).dat.at(t).do(close_valve)

def run_schedule_1(exit_1):
    schedule.clear()
    load_schedule(on_1, off_1)
    while exit_1.is_set():
         print("Se está aplicando el riego de 1 minuto")
         schedule.run_pending()
         time.sleep(1)

def run_schedule_2(exit_2):
    schedule.clear()
    load_schedule(on_2, off_2)
    while exit_2.is_set():
         print("Se está aplicando el riego de 30 segundos")
         schedule.run_pending()
         time.sleep(1)

exit_1=threading.Event()
exit_1.clear()

exit_2=threading.Event()
exit_2.clear()

while true:
        time.sleep(1)
