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


fig = plt.figure(figsize=(6,2))
ax = fig.add_subplot(1,2,1)
xdatos, ydatos = [],[]

fig2 = plt.figure(figsize=(6,2))
ax2 = fig2.add_subplot(1,2,1)
zdatos, idatos = [],[]

fig3 = plt.figure(figsize=(10,3))
ax3 = fig3.add_subplot(1,2,1)
kdatos,ldatos = [],[]

fig4 = plt.figure(figsize=(10,3))
ax4 = fig4.add_subplot(1,2,1)
pdatos,udatos = [],[]

def graficar1():  
    def animate(i,xdatos,ydatos):
        global respuesta
        respuesta = arduino.readline().decode('ascii')
        lista1 = respuesta.split(',') 
        var1 = lista1[0]
        var2 = lista1[1]
        var1 = float(var1)
        var2 = float(var2)
        
        etiqueta_01['text']='Humedad: '+str(var2)+" % "
        etiqueta_02['text']='Temperatura: '+str(var1)+" C "
        
        xdatos.append(i)
        ydatos.append(var2)
        ax.clear()
        ax.plot(xdatos,ydatos)     
    
    global ani
    ani = animation.FuncAnimation(fig,animate, fargs=(xdatos,ydatos))
    canvas.draw()

    graficar2()
    graficar3()
    graficar4()

def graficar2():  
    def animate(i,zdatos,idatos):
        #respuesta = arduino.readline().decode('ascii')
        
        lista1 = respuesta.split(',') 
        var1 = lista1[0]
        var2 = lista1[1]
        var1 = float(var1)
        var2 = float(var2)

        zdatos.append(i)
        idatos.append(var1)
        ax2.clear()
        ax2.plot(zdatos,idatos,color='red')

    global ani2
    ani2 = animation.FuncAnimation(fig2,animate, fargs=(zdatos,idatos))
    canvass.draw()

def graficar3():  
    def animate(i,kdatos,ldatos):
        #respuesta = arduino.readline().decode('ascii')
        
        lista1 = respuesta.split(',') 
        var1 = lista1[0]
        var2 = lista1[1]
        var3 = lista1[2]
        var1 = float(var1)
        var2 = float(var2)
        var3 = float(var3)
        if (var3 < 0):
            var3=0.0

        etiqueta_03['text']='Distancia: '+str(var3)+" cm"

        kdatos.append(i)
        ldatos.append(var3)
        ax3.clear()
        ax3.plot(kdatos,ldatos, color='m')

    global ani3
    ani3 = animation.FuncAnimation(fig3,animate, fargs=(kdatos,ldatos))
    canvasss.draw()

def graficar4():  
    def animate(i,pdatos,udatos):
        #respuesta = arduino.readline().decode('ascii')
        
        lista1 = respuesta.split(',') 
        var1 = lista1[0]
        var2 = lista1[1]
        var3 = lista1[2]
        var4 = lista1[3]
        var1 = float(var1)
        var2 = float(var2)
        var3 = float(var3)
        var4 = float(var4)

        etiqueta_04['text']=' '+str(var4)+" rpm"

        pdatos.append(i)
        udatos.append(var4)
        ax4.clear()
        ax4.plot(pdatos,udatos, color='k')

    global ani4
    ani4 = animation.FuncAnimation(fig4,animate, fargs=(pdatos,udatos))
    canvassss.draw()

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


canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().place(x=30, y=140)

canvass = FigureCanvasTkAgg(fig2, master=frame)
canvass.get_tk_widget().place(x=480, y=140)

canvasss = FigureCanvasTkAgg(fig3, master=frame)
canvasss.get_tk_widget().place(x=0, y=600)

canvassss = FigureCanvasTkAgg(fig4, master=frame)
canvassss.get_tk_widget().place(x=600, y=600)



graficar1()

Button(frame, text='Apagar Motor', width=15,height=2,font='Monospace 18 bold',bg='LightSkyBlue2', command=apagar).place(x=1590, y=740)
Button(frame, text='Encender Motor', width=15,height=2,font='Monospace 18 bold',bg='LightSkyBlue2', command=encender).place(x=1290, y=740)

Button(frame, text='Salir', width=15,height=2, font='Monospace 18 bold',bg='LightSkyBlue2', command=salir).place(x=1590, y=860)

ventana.mainloop()
