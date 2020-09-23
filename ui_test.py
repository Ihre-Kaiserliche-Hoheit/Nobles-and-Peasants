import PySimpleGUI as sg

layout = [
    [
        sg.Graph(
            canvas_size=(400, 400),
            graph_bottom_left=(0, 0),
            graph_top_right=(400, 400),
            key="graph"
            )]
]

window = sg.Window("rect on image", layout)
window.Finalize()

graph = window.Element("graph")

graph.DrawImage(filename="tile_city.png", location=(0, 400))
graph.DrawRectangle((200, 200), (250, 300), line_color="red")

while True:
    event, values = window.Read()
    if event is None:
        break
                  
