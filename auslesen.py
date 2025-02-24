# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 15:09:06 2025

@author: niklwill
"""

import os
import glob
import time
import RPi.GPIO as GPIO

# 🌱 GPIO-Definitionen
FEUCHTIGKEIT_SENSOR_PIN = 4  # Funduino D0 an GPIO4
TEMPERATUR_SENSOR_PIN = 18  # KY-001 (DS18B20) an GPIO18

# 🌡 1-Wire Initialisierung (DS18B20)
def lese_temperatur():
    basis_pfad = "/sys/bus/w1/devices/"
    try:
        sensor_ordner = glob.glob(basis_pfad + "28*")[0]
        sensor_datei = sensor_ordner + "/w1_slave"

        with open(sensor_datei, "r") as datei:
            zeilen = datei.readlines()

        while "YES" not in zeilen[0]:  # Sensor antwortet nicht sofort
            time.sleep(0.2)
            with open(sensor_datei, "r") as datei:
                zeilen = datei.readlines()

        temp_pos = zeilen[1].find("t=")
        if temp_pos != -1:
            temp_wert = zeilen[1][temp_pos+2:]
            temp_celsius = float(temp_wert) / 1000.0
            return temp_celsius
    except:
        return None  # Falls kein Sensor erkannt wird

# 🌱 Feuchtigkeitssensor auslesen (digital)
def lese_feuchtigkeit():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(FEUCHTIGKEIT_SENSOR_PIN, GPIO.IN)

    if GPIO.input(FEUCHTIGKEIT_SENSOR_PIN) == GPIO.HIGH:
        return "Trocken"
    else:
        return "Feucht"

# 📊 Daten auslesen
try:
    while True:
        temperatur = lese_temperatur()
        feuchtigkeit = lese_feuchtigkeit()
        
        if temperatur is not None:
            print(f"🌡 Temperatur: {temperatur:.2f}°C")
        else:
            print("⚠ Fehler: Kein Temperatursensor gefunden")
        
        print(f"🌱 Bodenfeuchtigkeit: {feuchtigkeit}")
        print("-" * 30)

        time.sleep(5)  # Alle 5 Sekunden neue Werte
except KeyboardInterrupt:
    print("Beende Messung...")
    GPIO.cleanup()
