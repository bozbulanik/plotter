import urwid
from plot import *
import time

class TerminalGraphWidget(urwid.WidgetWrap):
    def __init__(self, graph):
        self.text = urwid.Text("")
        self.graph = graph
        self.line_box = urwid.LineBox(self.text)
        self.filler = urwid.Filler(self.line_box)
        self.padding = urwid.Padding(self.filler)
        super().__init__(self.padding)

    def update(self):

        canvas = "\n".join("".join(row).replace('\033[96m', '').replace('\033[0m', '') for row in self.graph.canvas)
        
        self.text.set_text(canvas)

class PlotApp(object):
    def __init__(self):
        self.graph = TerminalGraph(width=80, height=20, x_label="X", y_label="Value", x_divisions=10, y_divisions=16, x_min=0, x_max=15, y_min=0, y_max=15)
        self.graph_widget = TerminalGraphWidget(self.graph)


    def exit_on_q(self, key):
        # Exit the application when 'q' is pressed
        if key in ('q', 'Q'):
            raise urwid.ExitMainLoop()

    def update_graph(self, loop, user_data):
        self.graph.clear()
        x_range = (0, 2 * math.pi)
        self.graph.plot_function(math.sin, x_range, x_shift=time.time(), y_shift=0)
        self.graph.add_axes()
        #self.graph.draw()
        self.graph_widget.update()
        self.loop.set_alarm_in(0.1, self.update_graph)
     
    def run(self):
        # Create and run the main loop
        self.loop = urwid.MainLoop(self.graph_widget, unhandled_input=self.exit_on_q)
        self.loop.set_alarm_in(0.1, self.update_graph)
        self.loop.run()

# Instantiate and run the application
if __name__ == "__main__":
    app = PlotApp()
    app.run()
