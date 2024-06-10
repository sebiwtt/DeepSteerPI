#!/usr/bin/env python
# coding:   latin-1
# Autor:    Ingmar Stapel
# Datum:    20190810
# Version:  2.1
# Homepage: http://custom-build-robots.com

# Dieses Programm wurde fuer die Ansteuerung der linken und rechten
# Motoren des Roboter-Autos entwickelt. Es geht dabei davon aus,
# dass eine L298N H-Bruecke als Motortreiber eingesetzt wird.

# Dieses Programm muss von einem uebergeordneten Programm aufgerufen 
# werden, das die Steuerung des Programms L298NHBridge übernimmt.

# Es wird die Klasse RPi.GPIO importiert, die die Ansteuerung
# der GPIO-Pins des Raspberry Pi ermoeglicht.
import RPi.GPIO as io
io.setmode(io.BCM)

# Mit der Variable DC_MAX wird die maximale Drehgeschwindigkeit der 
# Motoren festgelegt. DC steht dabei für DutyCicle.
# Die Geschwindigkeit wird initial auf den Wert 70 festgelegt welcher einer 
# Leistung der H-Bruecke von 70% also einer Drosselung entspricht.
# Diese Minderung der Leistung am Anfang hilft mit der Steuerung des Roboter-
# Autos besser zurechtzukommen. Soll das Roboter-Auto schneller 
# fahren, kann hier der Wert von 70 % auf maximal 100 % gesetzt werden.

DC_MAX = 70
# Mit dem folgenden Aufruf werden Warnungen deaktiviert, die die 
# Klasse RPi.GPIO eventuell ausgibt.
io.setwarnings(False)

# Im folgenden Programmabschnitt wird die logische Verkabelung des 
# Raspberry Pi im Programm abgebildet. Dazu werden den vom Motortreiber 
# bekannten Pins die GPIO-Adressen zugewiesen.

# --- START KONFIGURATION GPIO-Adressen ---
ENA = 18
IN1 = 6
IN2 = 13
IN3 = 19
IN4 = 26
ENB = 12
# --- ENDE KONFIGURATION GPIO-Adressen ---

# Der Variable leftmotor_in1_pin wird die Variable IN1 zugeordnet. 
# Der Variable leftmotor_in2_pin wird die Variable IN2 zugeordnet. 
leftmotor_in1_pin = IN1
leftmotor_in2_pin = IN2
# Beide Variablen leftmotor_in1_pin und leftmotor_in2_pin werden als
# Ausgaenge "OUT" definiert. Mit den beiden Variablen wird die
# Drehrichtung der Motoren gesteuert.
io.setup(leftmotor_in1_pin, io.OUT)
io.setup(leftmotor_in2_pin, io.OUT)
# Der Variable rightmotor_in1_pin wird die Variable IN1 zugeordnet. 
# Der Variable rightmotor_in2_pin wird die Variable IN2 zugeordnet. 
rightmotor_in1_pin = IN3
rightmotor_in2_pin = IN4
# Beide Variablen rightmotor_in1_pin und rightmotor_in2_pin werden 
# als Ausgaenge "OUT" definiert. Mit den beiden Variablen wird die
# Drehrichtung der Motoren gesteuert.
io.setup(rightmotor_in1_pin, io.OUT)
io.setup(rightmotor_in2_pin, io.OUT)

# Die GPIO-Pins des Raspberry Pi werden initial auf False gesetzt.
# So ist sichergestellt, dass kein HIGH-Signal anliegt und dass der 
# Motortreiber nicht unbeabsichtigt aktiviert wird.
io.output(leftmotor_in1_pin, False)
io.output(leftmotor_in2_pin, False)
io.output(rightmotor_in1_pin, False)
io.output(rightmotor_in2_pin, False)
# Der Variable leftmotorpwm_pin wird die Variable ENA zugeordnet.
# Der Variable rightmotorpwm_pin wird die Variable ENB zugeordnet.
leftmotorpwm_pin = ENA
rightmotorpwm_pin = ENB

# Die Variablen leftmotorpwm_pin und rightmotorpwm_pin werden 
# als Ausgaenge "OUT" definiert. Mit den beiden Variablen wird die
# Drehgeschwindigkeit der Motoren über ein PWM-Signal gesteuert.
io.setup(leftmotorpwm_pin, io.OUT)
io.setup(rightmotorpwm_pin, io.OUT)

# Die Variablen leftmotorpwm_pin und rightmotorpwm_pin werden 
# zusätzlich zu ihrer Eigenschaft als Ausgaenge als "PWM"-Ausgaenge
# definiert. Mit io.PWM(GPIO-Nummer, Frequenz) wird für einen bestimmten GPIO
# die Frequenz angegeben. In diesem Beispiel wird 100 Herz als Frequenz
# festgelegt. Manche Motortreiber benötigen aber z. B. 500 Herz. Hier muessen
# wenn das Roboter-Auto nicht losfaehrt mit der Herzzahl etwas 
# experimentieren. 
leftmotorpwm = io.PWM(leftmotorpwm_pin,100)
rightmotorpwm = io.PWM(rightmotorpwm_pin,100)

# Die linken Motoren stehen still, da das PWM-Signal mit 
# ChangeDutyCycle(0) auf 0 gesetzt wurde.
leftmotorpwm.start(0)
leftmotorpwm.ChangeDutyCycle(0)

# Die rechten Motoren stehen still, da das PWM-Signal mit 
# ChangeDutyCycle(0) auf 0 gesetzt wurde.
rightmotorpwm.start(0)
rightmotorpwm.ChangeDutyCycle(0)

# Die Funktion setMotorMode(motor, mode) legt die Drehrichtung der 
# Motoren fest. Die Funktion verfügt über zwei Eingabevariablen.
# motor      -> Diese Variable legt fest, ob der linke oder rechte 
#               Motor ausgewaehlt wird.
# mode       -> Diese Variable legt fest, welcher Modus gewaehlt ist
# Beispiel:
# setMotorMode(leftmotor, forward)  Die linken Motoren sind  gewaehlt
#                                   und drehen vorwaerts.
# setMotorMode(rightmotor, reverse) Die rechten Motoren sind  ausgewaehlt 
#                                   und drehen rueckwaerts.
# setMotorMode(rightmotor, stopp)   Der rechte Motor ist ausgewaehlt
#                                   und wird gestoppt.

def setMotorMode(motor, mode):
   if motor == "leftmotor":
      if mode == "reverse":
         io.output(leftmotor_in1_pin, True)
         io.output(leftmotor_in2_pin, False)
      elif  mode == "forward":
         io.output(leftmotor_in1_pin, False)
         io.output(leftmotor_in2_pin, True)
      else:
         io.output(leftmotor_in1_pin, False)
         io.output(leftmotor_in2_pin, False)
   elif motor == "rightmotor":
      if mode == "reverse":
         io.output(rightmotor_in1_pin, False)
         io.output(rightmotor_in2_pin, True)
      elif  mode == "forward":
         io.output(rightmotor_in1_pin, True)
         io.output(rightmotor_in2_pin, False)
      else:
         io.output(rightmotor_in1_pin, False)
         io.output(rightmotor_in2_pin, False)
   else:
      io.output(leftmotor_in1_pin, False)
      io.output(leftmotor_in2_pin, False)
      io.output(rightmotor_in1_pin, False)
      io.output(rightmotor_in2_pin, False)
# Die Funktion setMotorLeft(power) setzt die Geschwindigkeit der 
# linken Motoren. Die Geschwindigkeit wird als Wert zwischen -1
# und 1 uebergeben. Bei einem negativen Wert sollen sich die Motoren 
# rueckwaerts drehen, ansonsten vorwaerts. 
# Anschliessend werden aus den uebergebenen Werten die notwendigen 
# Prozentwerte fuer das PWM-Signal berechnet.

# Beispiel:
# Die Geschwindigkeit kann mit +1 (max) und -1 (min) gesetzt werden.
# Das Beispiel erklaert, wie die Geschwindigkeit berechnet wird.
# SetMotorLeft(0)     -> der linke Motor dreht mit 0 %, ist also gestoppt
# SetMotorLeft(0.75)  -> der linke Motor dreht mit 75 % vorwaerts
# SetMotorLeft(-0.5)  -> der linke Motor dreht mit 50 % rueckwaerts
# SetMotorLeft(1)     -> der linke Motor dreht mit 100 % vorwaerts
def setMotorLeft(power):
   int(power)
   if power < 0:
      # Rueckwaertsmodus fuer den linken Motor
      setMotorMode("leftmotor", "reverse")
      pwm = -int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   elif power > 0:
      # Vorwaertsmodus fuer den linken Motor
      setMotorMode("leftmotor", "forward")
      pwm = int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   else:
      # Stoppmodus fuer den linken Motor
      setMotorMode("leftmotor", "stopp")
      pwm = 0
   leftmotorpwm.ChangeDutyCycle(pwm)

# Die Funktion setMotorRight(power) setzt die Geschwindigkeit der 
# rechten Motoren. Die Geschwindigkeit wird als Wert zwischen -1 
# und 1 uebergeben. Bei einem negativen Wert sollen sich die Motoren 
# rueckwaerts drehen, ansonsten vorwaerts. 
# Anschliessend werden aus den uebergebenen Werten die notwendigen 
# Prozentwerte fuer das PWM-Signal berechnet.

# Beispiel:
# Die Geschwindigkeit kann mit +1 (max) und -1 (min) gesetzt werden.
# Das Beispiel erklaert, wie die Geschwindigkeit berechnet wird.
# setMotorRight(0)     -> der linke Motor dreht mit 0 %, ist also gestoppt
# setMotorRight(0.75)  -> der linke Motor dreht mit 75 % vorwaerts
# setMotorRight(-0.5)  -> der linke Motor dreht mit 50 % rueckwaerts
# setMotorRight(1)     -> der linke Motor dreht mit 100 % vorwaerts
def setMotorRight(power):
   int(power)
   if power < 0:
      # Rueckwaertsmodus fuer den rechten Motor
      setMotorMode("rightmotor", "reverse")
      pwm = -int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   elif power > 0:
      # Vorwaertsmodus fuer den rechten Motor
      setMotorMode("rightmotor", "forward")
      pwm = int(DC_MAX * power)
      if pwm > DC_MAX:
         pwm = DC_MAX
   else:
      # Stoppmodus fuer den rechten Motor
      setMotorMode("rightmotor", "stopp")
      pwm = 0
   rightmotorpwm.ChangeDutyCycle(pwm)

# Die Funktion exit() setzt die Ausgaenge, die den Motortreiber 
# steuern, auf False. So befindet sich der Motortreiber nach dem 
# Aufruf derFunktion in einem gesicherten Zustand und die Motoren 
# sind gestoppt.
def exit():
   io.output(leftmotor_in1_pin, False)
   io.output(leftmotor_in2_pin, False)
   io.output(rightmotor_in1_pin, False)
   io.output(rightmotor_in2_pin, False)
   io.cleanup()

# Ende des Programms
