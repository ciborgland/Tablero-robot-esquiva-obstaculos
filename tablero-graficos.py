from calendar import c
from tkinter import *
import tkinter
from turtle import color
from PIL import ImageTk, Image
import serial
import time

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

arduino = serial.Serial('COM3', 9600)
time.sleep(1)


figHumedad = plt.figure(figsize=(6,2))
ax = figHumedad.add_subplot(1,2,1)
xdatos, ydatos = [],[]

figTemperatura = plt.figure(figsize=(6,2))
ax2 = figTemperatura.add_subplot(1,2,1)
zdatos, idatos = [],[]

figDistancia = plt.figure(figsize=(10,3))
ax3 = figDistancia.add_subplot(1,2,1)
kdatos,ldatos = [],[]

figRpm = plt.figure(figsize=(10,3))
ax4 = figRpm.add_subplot(1,2,1)
pdatos,udatos = [],[]

def mostrarHumedad():  
    def animate(i,xdatos,ydatos):
        global respuesta
        respuesta = arduino.readline().decode('ascii')
        lista1 = respuesta.split(',')
        humedad = float(lista1[1])
        
        etiqueta_01['text']='Humedad: '+str(humedad)+" % "
        
        xdatos.append(i)
        ydatos.append(var2)
        ax.clear()
        ax.plot(xdatos,ydatos)     
    
    global ani
    ani = animation.FuncAnimation(figHumedad,animate, fargs=(xdatos,ydatos))
    canvas.draw()


def mostrarTemperatura():  
    def animate(i,zdatos,idatos):
        #respuesta = arduino.readline().decode('ascii')
        
        lista1 = respuesta.split(',') 
        var1 = float(lista1[0])

        etiqueta_02['text']='Temperatura: '+str(var1)+" C "

        zdatos.append(i)
        idatos.append(var1)
        ax2.clear()
        ax2.plot(zdatos,idatos,color='red')

    global ani2
    ani2 = animation.FuncAnimation(figTemperatura,animate, fargs=(zdatos,idatos))
    canvas2.draw()

def mostrarDistancia():  
    def animate(i,kdatos,ldatos):
        #respuesta = arduino.readline().decode('ascii')
        
        lista1 = respuesta.split(',') 
        var3 = float(lista1[2])
        if (var3 < 0):
            var3=0.0

        etiqueta_03['text']='Distancia: '+str(var3)+" cm"

        kdatos.append(i)
        ldatos.append(var3)
        ax3.clear()
        ax3.plot(kdatos,ldatos, color='m')

    global ani3
    ani3 = animation.FuncAnimation(figDistancia,animate, fargs=(kdatos,ldatos))
    canvas3.draw()

def mostrarRpm():  
    def animate(i,pdatos,udatos):
        #respuesta = arduino.readline().decode('ascii')
        
        lista1 = respuesta.split(',') 
        var4 = float(lista1[3])
        
        etiqueta_04['text']=' '+str(var4)+" rpm"

        pdatos.append(i)
        udatos.append(var4)
        ax4.clear()
        ax4.plot(pdatos,udatos, color='k')

    global ani4
    ani4 = animation.FuncAnimation(figRpm,animate, fargs=(pdatos,udatos))
    canvas4.draw()

def salir():
    arduino.close()
    exit()

def apagar():
    b='a'
    arduino.write(b.encode('ascii'))

def encender():
    b='e'
    arduino.write(b.encode('ascii'))


ventana = Tk()
ventana.title('Software Robot')
ventana.geometry('1900x1080')

frame = Frame(ventana, bg='white', bd=3)
frame.pack(expand=1, fill='both')

image = Image.open("logo.jpg").resize((500,500)) # Ingresar tu imagen de logo
photo = ImageTk.PhotoImage(image, master=frame)
label = Label(frame, image=photo)
label.image = image
label.place(x=1390, y=20)

etiqueta_01 = Label(frame, font='Monospace 28 bold')
etiqueta_01.place(x=80,y=80)

etiqueta_02 = Label(frame, font='Monospace 28 bold')
etiqueta_02.place(x=500,y=80)

etiqueta_03 = Label(frame, font='Monospace 28 bold')
etiqueta_03.place(x=170,y=550)

etiqueta_04 = Label(frame, font='Monospace 28 bold')
etiqueta_04.place(x=880,y=550)


canvas = FigureCanvasTkAgg(figHumedad, master=frame)
canvas.get_tk_widget().place(x=30, y=140)

canvas2 = FigureCanvasTkAgg(figTemperatura, master=frame)
canvas2.get_tk_widget().place(x=480, y=140)

canvas3 = FigureCanvasTkAgg(figDistancia, master=frame)
canvas3.get_tk_widget().place(x=0, y=600)

canvas4 = FigureCanvasTkAgg(figRpm, master=frame)
canvas4.get_tk_widget().place(x=600, y=600)

mostrarHumedad()
mostrarTemperatura()
mostrarDistancia()
mostrarRpm()


Button(frame, text='Apagar Motor', width=15,height=2,font='Monospace 18 bold',bg='LightSkyBlue2', command=apagar).place(x=1590, y=740)
Button(frame, text='Encender Motor', width=15,height=2,font='Monospace 18 bold',bg='LightSkyBlue2', command=encender).place(x=1290, y=740)

Button(frame, text='Salir', width=15,height=2, font='Monospace 18 bold',bg='LightSkyBlue2', command=salir).place(x=1590, y=860)

ventana.mainloop()
