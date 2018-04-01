#! /usr/bin/python2.7

from tkinter import *
import m2
import serial

def sendEntry():
   print("ID: {}\nMessage: {}".format(e1.get(), e2.get()))
   m2.sendSerial(e1.get(),e2.get(),portVar.get())

def reloadPorts():
    portChoices = [p[0] for p in list(serial.tools.list_ports.comports())] or {'No ports available'}
    try:
        defaultPort = portChoices[0]
    except (IndexError, TypeError):
        defaultPort = "No board detected"
    portVar.set(defaultPort)


def uploadScript():
    if scriptVar.get() in m2.sketches:
        print("Uploading: " + scriptVar.get())
        if portVar.get() not in [p[0] for p in list(serial.tools.list_ports.comports())]:
            print("No board detected. Aborting upload.")
        else:
            m2.uploadScript(scriptVar.get(),portVar.get())
    else:
        print("Select a sketch to upload first")

master = Tk()
Label(master, text="ID").grid(row=2)
Label(master, text="Message").grid(row=3)

e1 = Entry(master)
e2 = Entry(master)

e1.grid(row=2, column=1)
e2.grid(row=3, column=1)

e1.insert(10,"3 Hex Chars")
e2.insert(10,"8 Hex Chars")

#Script Setup ==============================
scriptVar = StringVar(master)
choices = m2.sketches #take list of sketches from m2.py
scriptVar.set('Select Script') # set the default option

popupMenu = OptionMenu(master, scriptVar, *choices)
Label(master, text="Upload Script").grid(row = 0, column = 0)
popupMenu.grid(row = 0, column =1)
#===========================================

#Port Setup ================================
portVar = StringVar(master)
portChoices = [p[0] for p in list(serial.tools.list_ports.comports())] or {'No ports available'}
try:
    defaultPort = portChoices[0]
except (IndexError, TypeError):
    defaultPort = "No board detected"
portVar.set(defaultPort)

popupMenu2 = OptionMenu(master, portVar, *portChoices)
Label(master, text="Select Port").grid(row = 1, column = 0)
popupMenu2.grid(row = 1, column =1)
#============================================

#Button Setup ================================
Button(master,text='Upload', command=uploadScript).grid(row=0,column=2)
Button(master,text='Reload', command=reloadPorts).grid(row=1,column=2)
Button(master, text='Quit', command=master.quit).grid(row=4, column=0, sticky=W, pady=4)
Button(master, text='Send it!', command=sendEntry).grid(row=4, column=2, sticky=W, pady=4)
#============================================
mainloop( )
