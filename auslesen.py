# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 13:19:08 2025

@author: niklwill
"""

import RPi.GPIO as GPIO
import time

DHT_PIN = 4  # GPIO-Pin, an den der DHT11 angeschlossen ist

def read_dht11():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DHT_PIN, GPIO.OUT)
    
    # Startsignal an den Sensor senden
    GPIO.output(DHT_PIN, GPIO.LOW)
    time.sleep(0.018)  # Mindestens 18ms Low-Signal
    GPIO.output(DHT_PIN, GPIO.HIGH)
    time.sleep(0.00002)  # 20µs warten

    # Wechsel zu Eingabemodus
    GPIO.setup(DHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # Antwortsignal des Sensors abwarten
    timeout = time.time() + 0.1  # Timeout für fehlerhafte Messungen
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        if time.time() > timeout:
            print("Fehler: Kein Antwortsignal vom Sensor")
            GPIO.cleanup()
            return None
    while GPIO.input(DHT_PIN) == GPIO.LOW:
        pass
    while GPIO.input(DHT_PIN) == GPIO.HIGH:
        pass

    # Datenbits auslesen (40 Bits = 5 Bytes)
    data = []
    for i in range(40):
        while GPIO.input(DHT_PIN) == GPIO.LOW:
            pass  # Start jedes Bits

        start_time = time.time()
        while GPIO.input(DHT_PIN) == GPIO.HIGH:
            pass  # Länge des High-Signals messen

        bit_length = time.time() - start_time
        data.append(1 if bit_length > 0.00004 else 0)  # Ungefähr 40µs = 0,00004s

    # Bytes zusammensetzen
    humidity = sum([data[i] << (7 - (i % 8)) for i in range(8)])
    temperature = sum([data[i + 16] << (7 - (i % 8)) for i in range(8)])

    GPIO.cleanup()
    return temperature, humidity

while True:
    result = read_dht11()
    if result:
        temp, hum = result
        print(f"Temperatur: {temp}°C, Feuchtigkeit: {hum}%")
    else:
        print("Fehlgeschlagene Messung, versuche es erneut.")
    
    time.sleep(30)  # 30 Sekunden warten
