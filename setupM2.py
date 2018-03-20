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
    call(["Arduino/build/linux/work/install.sh"],shell=True)

#Copy hardware files to Arduino folder:
if not os.path.isdir("Arduino/build/linux/work/macchina")
    call(["cp -r macchina Arduino/build/linux/work/"], shell=True)

call(["chmod +x m2.py"], shell=True)
