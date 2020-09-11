#from tkinter import *
#import pygame
import PySimpleGUI as sg

T = 0
OUTPUT_1 = 0
OUTPUT_2 = 0

sg.theme('DarkAmber')	# Add a touch of color
# All the stuff inside your window.
layout = [  [sg.Text('Some text on Row 1')],
            [sg.Text(OUTPUT_1)],
            [sg.Text(OUTPUT_2)],
            [sg.Button('Start'), sg.Button('Cancel')] ]
     
# Create the Window
window = sg.Window('Window Title', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':	# if user closes window or clicks cancel
        break
    
    if event == "Start":
        OUTPUT_1 = 1
    
window.close()
