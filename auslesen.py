import RPi.GPIO as GPIO
import time
import glob
import threading

# BCM-Pin-Nummern für die Segmente
segments = {
    'A': 5, 'B': 21, 'C': 16, 'D': 20, 'E': 12, 'F': 26, 'G': 19, 'DP': 6
}

# Digit-Pins für Multiplexing (4 Stellen)
digits = [22, 27, 17, 23]  

# Segment-Darstellung für Zahlen & Buchstaben
num = {
    '0': (1,1,1,1,1,1,0),
    '1': (0,1,1,0,0,0,0),
    '2': (1,1,0,1,1,0,1),
    '3': (1,1,1,1,0,0,1),
    '4': (0,1,1,0,0,1,1),
    '5': (1,0,1,1,0,1,1),
    '6': (1,0,1,1,1,1,1),
    '7': (1,1,1,0,0,0,0),
    '8': (1,1,1,1,1,1,1),
    '9': (1,1,1,1,0,1,1),
    'C': (1,0,0,1,1,1,0),
    ' ': (0,0,0,0,0,0,0)
}

# GPIO einrichten
GPIO.setmode(GPIO.BCM)
for segment in segments.values():
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, 0)

for digit in digits:
    GPIO.setup(digit, GPIO.OUT)
    GPIO.output(digit, 1)

# Temperatur-Sensor DS18B20 (1-Wire)
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

temperature = " 00C"  # Startwert für die Anzeige

def read_temp():
    """Liest die Temperatur und formatiert sie für die Anzeige"""
    global temperature
    while True:
        try:
            with open(device_file, 'r') as f:
                lines = f.readlines()
            
            while lines[0].strip()[-3:] != 'YES':
                time.sleep(0.2)
                with open(device_file, 'r') as f:
                    lines = f.readlines()

            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
                temp_string = lines[1][equals_pos+2:]
                temp_c = round(float(temp_string) / 1000.0)  # Aufrunden
                temperature = str(temp_c).rjust(2) + "C"  # Formatierung XX°C

        except Exception as e:
            print(f"Fehler beim Temperaturlesen: {e}")
            temperature = " ERR"
        
        time.sleep(1)  # 1 Sekunde warten

def display_loop():
    """Kontinuierlich Temperatur auf der Anzeige anzeigen"""
    while True:
        for digit in range(4):  # Multiplexing für 4 Stellen
            char = temperature[digit]
            if char in num:
                pattern = num[char]
            else:
                pattern = num[' ']  # Leerstelle bei Fehler

            # Segmente setzen
            for seg, val in zip(segments.values(), pattern):
                GPIO.output(seg, val)

            # Digit aktivieren
            GPIO.output(digits[digit], 0)
            time.sleep(0.003)  # Kürzere Wartezeit für flüssigere Anzeige
            GPIO.output(digits[digit], 1)  # Deaktivieren

try:
    # Starte Temperatur-Thread
    temp_thread = threading.Thread(target=read_temp, daemon=True)
    temp_thread.start()

    # Starte Anzeige-Thread
    display_thread = threading.Thread(target=display_loop, daemon=True)
    display_thread.start()

    while True:
        time.sleep(1)  # Hauptthread bleibt aktiv

except KeyboardInterrupt:
    print("Programm beendet.")

finally:
    GPIO.cleanup()
