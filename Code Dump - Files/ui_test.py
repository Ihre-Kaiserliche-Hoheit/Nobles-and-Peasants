import PySimpleGUI as sg

sg.theme("BluePurple")

layout = [  [sg.T("Tipped stuff:"), sg.T(size=(15,1), key="-OUTPUT-")],
            [sg.In(key="-IN-")],
            [sg.B("Show"), sg.B("Exit")]]

window = sg.Window("Stayer Title", layout)

while True:
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Show":
        window["-OUTPUT-"].update(values["-IN-"])

window.close()
                  
