#! /usr/bin/python2.7

from subprocess import call
import apt
import os

#Install ant
cache = apt.Cache()
try:
    cache['ant'].is_installed
except KeyError:
    print "Installing ant"
    caller= "sudo apt install ant"
    call([caller],shell=True)

#Clone the Arduino repo
if not os.path.isdir("Arduino"):
    print("Setting up Arduino CLI Environment:\n")
    call(["git clone https://github.com/arduino/Arduino.git"],shell=True)
    call(["ant Arduino/build/dist"], shell=True)
    #call(["mkdir -p /home/$USER/.local/share/icons/hicolor/"], shell=True)
    call(["Arduino/build/linux/work/install.sh"],shell=True)

# if not os.path.isdir("M2"):
#     print("Setting up M2 Enviroment:\n")
#     call(["git clone https://github.com/DanielOved/M2.git"],shell=True)
