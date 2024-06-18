# Released by rdb under the Unlicense (unlicense.org)
# Based on information from:
# https://www.kernel.org/doc/Documentatio ... ck-api.txt

# 20181231 modified by Ingmar Stapel, changes released under 
# the Unlicense.

import os, struct, array
from fcntl import ioctl

# Das Programm L298NHBridge.py wird als Modul geladen.
# import L298NHBridge as HBridge

# Das Programm L298NHBridgePCA9685.py wird als Modul geladen.
import L298NHBridgePCA9685 as HBridge

# Variablen Definition der linken und rechten Geschwindigkeit der
# Motoren des Roboter-Autos.
speedleft = 0
speedright = 0

# We'll store the states here.
axis_states = {}
button_states = {}

# These constants were borrowed from linux/input.h
axis_names = {
    0x00 : 'x',
    0x01 : 'y',
    0x02 : 'z',
    0x03 : 'rx',
    0x04 : 'ry',
    0x05 : 'rz',
    0x06 : 'trottle',
    0x07 : 'rudder',
    0x08 : 'wheel',
    0x09 : 'gas',
    0x0a : 'brake',
    0x10 : 'hat0x',
    0x11 : 'hat0y',
    0x12 : 'hat1x',
    0x13 : 'hat1y',
    0x14 : 'hat2x',
    0x15 : 'hat2y',
    0x16 : 'hat3x',
    0x17 : 'hat3y',
    0x18 : 'pressure',
    0x19 : 'distance',
    0x1a : 'tilt_x',
    0x1b : 'tilt_y',
    0x1c : 'tool_width',
    0x20 : 'volume',
    0x28 : 'misc',
}

button_names = {
    0x120 : 'trigger',
    0x121 : 'thumb',
    0x122 : 'thumb2',
    0x123 : 'top',
    0x124 : 'top2',
    0x125 : 'pinkie',
    0x126 : 'base',
    0x127 : 'base2',
    0x128 : 'base3',
    0x129 : 'base4',
    0x12a : 'base5',
    0x12b : 'base6',
    0x12f : 'dead',
    0x130 : 'a',
    0x131 : 'b',
    0x132 : 'c',
    0x133 : 'x',
    0x134 : 'y',
    0x135 : 'z',
    0x136 : 'tl',
    0x137 : 'tr',
    0x138 : 'tl2',
    0x139 : 'tr2',
    0x13a : 'select',
    0x13b : 'start',
    0x13c : 'mode',
    0x13d : 'thumbl',
    0x13e : 'thumbr',

    0x220 : 'dpad_up',
    0x221 : 'dpad_down',
    0x222 : 'dpad_left',
    0x223 : 'dpad_right',

    # XBox 360 controller uses these codes.
    0x2c0 : 'dpad_left',
    0x2c1 : 'dpad_right',
    0x2c2 : 'dpad_up',
    0x2c3 : 'dpad_down',
}

axis_map = []
button_map = []

# Die Funktion printscreen() gibt immer das aktuelle Menue aus
# sowie die Geschwindigkeit der linken und rechten Motoren wenn
# es aufgerufen wird.
def printscreen():
    # der Befehl os.system('clear') leert den Bildschirmihalt vor
    # jeder Aktualisierung der Anzeige. So bleibt das Menue stehen
    # und die Bildschirmanzeige im Terminal Fenster steht still.
    os.system('clear')
    buf = array.array('c', ['\0'] * 64)
    ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)    
    js_name = buf.tostring()   
    print("========== Joystick Robotersteuerung ==========")
    print('Joystick Name: %s' % js_name) 
    print("===============================================")     
    print("==========           Menue           ==========")  
    print("===============================================")       
    print("Button O:   Motoren stoppen")
    print("Button X:   Programm beenden")
    print("===============================================")      
    print("==========  Geschwindigkeitsanzeige  ==========")
    print("Geschwindigkeit linker Motor:  ", speedleft)
    print("Geschwindigkeit rechter Motor: ", speedright)
    print("===============================================")      


# Oeffene das Joystick Geraet / device.
fn = '/dev/input/js0'
jsdev = open(fn, 'rb')

# Lese den Namen des Joystick devices.
buf = array.array('c', ['\0'] * 64)
ioctl(jsdev, 0x80006a13 + (0x10000 * len(buf)), buf) # JSIOCGNAME(len)
js_name = buf.tostring()

# Lese die Anzahl der Achsen und Knoepfe aus.
buf = array.array('B', [0])
ioctl(jsdev, 0x80016a11, buf) # JSIOCGAXES
num_axes = buf[0]

buf = array.array('B', [0])
ioctl(jsdev, 0x80016a12, buf) # JSIOCGBUTTONS
num_buttons = buf[0]

# Lese das Mapping der Achsen aus.
buf = array.array('B', [0] * 0x40)
ioctl(jsdev, 0x80406a32, buf) # JSIOCGAXMAP

for axis in buf[:num_axes]:
    axis_name = axis_names.get(axis, 'unknown(0x%02x)' % axis)
    axis_map.append(axis_name)
    axis_states[axis_name] = 0.0

# Lese das Mapping der Buttons aus.
buf = array.array('H', [0] * 200)
ioctl(jsdev, 0x80406a34, buf) # JSIOCGBTNMAP

for btn in buf[:num_buttons]:
    btn_name = button_names.get(btn, 'unknown(0x%03x)' % btn)
    button_map.append(btn_name)
    button_states[btn_name] = 0

# In der Hauptschleife werden die Eingaben am Joystick gelesen
# sowie die Werte fuer die Steuerung der Motoren ausgelesen.
while True:
    evbuf = jsdev.read(8)
    if evbuf:
        time, value, type, number = struct.unpack('IhBB', evbuf)

# Hier werden die Buttons ausgelesen die gedrueckt wurden.
# So wird mit den beiden Buttons X und O z. B. Program beendet oder
# die Werte fuer die Motoren auf Null gesetzt. 
# Hier koennten auch weitere Buttons ausgelesen werden um Funktionen
# auszufuehren.
        if type & 0x01:
            button = button_map[number]
            if button:
                button_states[button] = value
                if button == "a" and value == 1:
                    print("Das Programm wurde beendet!")
                    speedleft = 0
                    speedright = 0
                    HBridge.setMotorLeft(speedleft)
                    HBridge.setMotorRight(speedright)                   
                    break
                elif button == "b" and value == 1:
                    speedleft = 0
                    speedright = 0
                    HBridge.setMotorLeft(speedleft)
                    HBridge.setMotorRight(speedright)       
                    printscreen()                  
# Mit dieser IF-Abfragen werden die Achsen ausgelesen um die
# Geschwindigkeit der linken und rechten Motoren setzen zu koennen.
        if type & 0x02:
            axis = axis_map[number]
            if axis == "y":
                fvalue = value / 32767.0
                speedleft = round(value / 32767.0, 2) *-1
                axis_states[axis] = fvalue
                #print "%s: %.3f" % (axis, fvalue)
            elif axis == "ry":
                fvalue = value / 32767.0
                speedright = round(value / 32767.0, 2) *-1
                axis_states[axis] = fvalue
                #print "%s: %.3f" % (axis, fvalue)
            HBridge.setMotorLeft(speedleft)
            HBridge.setMotorRight(speedright)
            printscreen()
 # Ende des Programms             