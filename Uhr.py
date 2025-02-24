import RPi.GPIO as GPIO
import time
from datetime import datetime

#setup für Ansteuerungsart der Pins
GPIO.setmode(GPIO.BOARD)
#Fehlermeldungen werden ignoriert
GPIO.setwarnings(False)

#Anlegen der Segmente als Dictionary
segmente = {
    'a': 5, 'b': 6, 'c': 13, 'd': 19,
    'e': 26, 'f': 16, 'g': 20, 'dp': 21
}

#Anlegen der Stellen als liste
stellen = [17, 27, 22, 23]

#setup der Segmente
for segment in segmente.values():
    GPIO.setup(segment, GPIO.OUT)
    GPIO.output(segment, GPIO.LOW)

#setup der Stellen
for stelle in stellen:
    GPIO.setup(stelle, GPIO.OUT)
    GPIO.output(stelle, GPIO.LOW)

#Legt fest welche Segmente für die jeweiligen Zahlen angesteuert werden muss
#Reihenfolge: a,b,c,d,e,f,g
#Speicherung wieder als Dictionary
zahlen_zu_segmenten = {
    '0': [1, 1, 1, 1, 1, 1, 0],
    '1': [0, 1, 1, 0, 0, 0, 0],
    '2': [1, 1, 0, 1, 1, 0, 1],
    '3': [1, 1, 1, 1, 0, 0, 1],
    '4': [0, 1, 1, 0, 0, 1, 1],
    '5': [1, 0, 1, 1, 0, 1, 1],
    '6': [1, 0, 1, 1, 1, 1, 1],
    '7': [1, 1, 1, 0, 0, 0, 0],
    '8': [1, 1, 1, 1, 1, 1, 1],
    '9': [1, 1, 1, 1, 0, 1, 1],
    ' ': [0, 0, 0, 0, 0, 0, 0]
}

#Funktion für die Anzeige der Ziffern
def stelle_anzeigen(stelle, wert, dp=False):
    #alle Stellen werden auf 0 gesetzt
    for s in stellen:
        GPIO.output(s, GPIO.LOW)
    #für jedes Segment im Dictionary "Segmente" wird die Funktion durchgeführt; dabei wird der string als "segment" und der Integer als "pin" festgelegt
    for segment, pin in segmente.items():
        if segment == 'dp':
            #bei dp wird der dp Pin auf High gesetzt
            GPIO.output(pin, GPIO.HIGH if dp else GPIO.LOW)
        else:
            #zahlen_zu_segmenten zeigt für die jeweilige anzuzeigende Zahl die benötigten segmente an
            #segmente.keys() liefert die Segmentnamen aus dem "segment" Dictionary (z.B. "a", "b" usw.)
            #list(segmente.keys()).index(segment) Index des aktuellen Segmentnamens in der Liste aller Segmentnamen wird ermittelt
            #gesamter Ausdruck "zahlen_zu_segmenten[wert][list(segmente.keys()).index(segment)" liefert entweder 1 (Segment soll leuchten) oder 0 (Segment soll aus sein) für das gerade betrachtete Segment.
            GPIO.output(pin, GPIO.HIGH if zahlen_zu_segmenten[wert][list(segmente.keys()).index(segment)] else GPIO.LOW)
    
    #entsprechende stelle wird für 0.005 s an- und dann wieder ausgeschalten
    GPIO.output(stellen[stelle], GPIO.HIGH)
    time.sleep(0.005)
    GPIO.output(stellen[stelle], GPIO.LOW)


#Dauerschleife für Uhrzeitanzeige
try:
    while True:
        #aktuelle Tageszeit wird aufgerufen und im Format hhmm in der Variable zeit_str gespeichert
        jetzt = datetime.now()
        zeit_str = jetzt.strftime("%H%M")
        for _ in range(100):  # 100 Durchläufe zur Stabilisierung des Bildes
            #vorher definierte Funktion für das Anzeigen der Stellen wird jeweils für jede Stelle aufgerufen und die Zahl die an dem Zeitpunkt in der Uhrzeit steht, wird dargestellt
            stelle_anzeigen(0, zeit_str[0])
            stelle_anzeigen(1, zeit_str[1], dp=True if jetzt.second % 2 == 0 else False) #dp blinkt jede Sekunde
            stelle_anzeigen(2, zeit_str[2])
            stelle_anzeigen(3, zeit_str[3])
#mit Strg + C wird das Programm beendet (verhindert Endlosschleife)
except KeyboardInterrupt:
    #Pinbelegungen und Konfiguration durch GPIO werden zurückgesetzt
     GPIO.cleanup()

