import customtkinter as ctk
from tkinter import messagebox

# Constants for padding
LABEL_PADY = 10
BUTTON_PADY = 5

class CanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Single Canvas")
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=500, bg="SystemButtonFace", highlightthickness=1)
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)  # Bind mouse motion event
        self.canvas.elements = []
        self.coord_label = ctk.CTkLabel(self.root, text="")
        self.coord_label.pack()

        self.log_button = ctk.CTkButton(self.root, text="Print Log", command=self.print_log)
        self.log_button.pack(pady=BUTTON_PADY)


    def on_mouse_move(self, event):
        self.coord_label.configure(text=f"X: {event.x}, Y: {event.y}")

    def on_canvas_click(self, event):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Select Component")
        popup.attributes('-topmost', True)  # Ensure the popup is on top

        label = ctk.CTkLabel(popup, text=f"X: {event.x}, Y: {event.y}")
        label.pack(pady=LABEL_PADY)

        component_var = ctk.StringVar(value="Select Component")
        component_dropdown = ctk.CTkComboBox(popup, values=["Resistor", "Inductor", "Capacitor", "Resistor3"], variable=component_var)
        component_dropdown.pack(pady=BUTTON_PADY)

        select_button = ctk.CTkButton(popup, text="Select", 
                                      command=lambda: [self.draw_component(event.x, event.y, component_var.get()), popup.destroy()])
        select_button.pack(pady=BUTTON_PADY)

        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=BUTTON_PADY)

    def draw_component(self, x, y, component_type):
        # Puntos centrales del canvas ajustados al tamaño del canvas
        x1, y1 = x, y
        x2, y2 = x + 50, y

        if component_type == "Resistor":
            message = f"self.draw_resistor(self.canvas, [{x1}, {y1}], [{x2}, {y2}])"
            print(message)
            self.log_message(message)
            self.draw_resistor(self.canvas, [x1, y1], [x2, y2])
        elif component_type == "Inductor":
            message = f"self.draw_inductor(self.canvas, [{x1}, {y1}], [{x2}, {y2}])"
            print(message)
            self.log_message(message)
            self.draw_inductor(self.canvas, [x1, y1], [x2, y2])
        elif component_type == "Capacitor":
            message = f"self.draw_capacitor(self.canvas, [{x1}, {y1}], [{x2}, {y2}])"
            print(message)
            self.log_message(message)
            self.draw_capacitor(self.canvas, [x1, y1], [x2, y2])
        elif component_type == "Resistor3":
            message = f"self.draw_resistor3(self.canvas, [{x1}, {y1}], {x + 25}, {x + 50}, 'vertical', 40)"
            print(message)
            self.log_message(message)
            self.draw_resistor3(self.canvas, [x1, y1], x + 25, x + 50, "vertical", 40)

    def log_message(self, message):
        if not hasattr(self, 'log'):
            self.log = []
        self.log.append(message)

    def print_log(self):
        if len(self.log) > 1:
            import csv
            from tkinter import filedialog

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file, delimiter='|', quoting=csv.QUOTE_NONE, escapechar='|')
                    for item in self.log:
                        writer.writerow([item])

    def draw_resistor(self, canvas, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        line1 = canvas.create_line(x1, y1, x1 + 5, y1, fill="black", width=2)
        rect = canvas.create_rectangle(x1 + 5, y1 - 5, x1 + 15, y1 + 5, outline="black", width=2)
        line2 = canvas.create_line(x1 + 15, y1, x2, y2, fill="black", width=2)
        canvas.elements.extend([line1, rect, line2])

    def draw_resistor3(self, canvas, pmain, coord_center, coord_final, orientation, scale):
        #default orientation is horizontal

        if coord_center == "center" and orientation == "horizontal":
            coord_center = (pmain[0] + coord_final)/2

        if coord_center == "center" and orientation == "vertical":
            coord_center = (pmain[1] + coord_final)/2

        match orientation:
            case "horizontal":
                x1 = pmain[0]
                x2 = coord_center
                x3 = coord_final

                y=pmain[1]

                rectangle_width = 1 * scale
                rectangle_height = rectangle_width*(1/3)

                if rectangle_width >= (x3-x1):
                    rectangle_width = (x3-x1)*0.9

                line1 = canvas.create_line(x1, y, x2-rectangle_width/2, y, fill="black", width=2)

                rect = canvas.create_rectangle(x2-rectangle_width/2, y - rectangle_height/2, x2 + rectangle_width/2, y + rectangle_height/2, outline="black", width=2)

                line2 = canvas.create_line(x2 + rectangle_width/2, y, x3, y, fill="black", width=2)

            case "vertical":
                y1 = pmain[1]
                y2 = coord_center
                y3 = coord_final

                x=pmain[0]

                rectangle_height = 1 * scale
                rectangle_width = rectangle_height*(1/3)

                if rectangle_height >= (y3-y1):
                    rectangle_height = (y3-y1)*0.9

                line1 = canvas.create_line(x, y1, x, y2-rectangle_height/2, fill="black", width=2)

                rect = canvas.create_rectangle(x - rectangle_width/2, y2-rectangle_height/2, x + rectangle_width/2, y2 + rectangle_height/2, outline="black", width=2)

                line2 = canvas.create_line(x, y2 + rectangle_height/2, x, y3, fill="black", width=2)

        canvas.elements.extend([line1, rect, line2])
    
    def draw_inductor(self, canvas, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        line1 = canvas.create_line(x1, y1, x1 + 5, y1, fill="black", width=2)
        arc1 = canvas.create_arc(x1 + 5, y1 - 5, x1 + 15, y1 + 5, start=0, extent=180, style='arc', outline="black", width=2)
        arc2 = canvas.create_arc(x1 + 15, y1 - 5, x1 + 25, y1 + 5, start=0, extent=180, style='arc', outline="black", width=2)
        arc3 = canvas.create_arc(x1 + 25, y1 - 5, x1 + 35, y1 + 5, start=0, extent=180, style='arc', outline="black", width=2)
        line2 = canvas.create_line(x1 + 35, y1, x2, y2, fill="black", width=2)
        canvas.elements.extend([line1, arc1, arc2, arc3, line2])

    def draw_capacitor(self, canvas, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        line1 = canvas.create_line(x1, y1, x1 + 15, y1, fill="black", width=2)
        line2 = canvas.create_line(x1 + 15, y1 - 10, x1 + 15, y1 + 10, fill="black", width=2)
        line3 = canvas.create_line(x1 + 25, y1 - 10, x1 + 25, y1 + 10, fill="black", width=2)
        line4 = canvas.create_line(x1 + 25, y1, x2, y1, fill="black", width=2)
        canvas.elements.extend([line1, line2, line3, line4])

if __name__ == "__main__":
    root = ctk.CTk()
    app = CanvasApp(root)
    root.mainloop()
