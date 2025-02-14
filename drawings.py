import customtkinter as ctk
from tkinter import messagebox

# Constants for padding
FRAME_PADX = 0
FRAME_PADY = 0
LABEL_PADY = 10
BUTTON_PADY = 5

class GridApp:
    def __init__(self, root):
        self.root = root
        self.root.title("10x10 Grid")
        self.canvases = []
        self.grid_visible = True

        self.create_grid()
        self.create_toggle_button()

    def create_grid(self):
        for row in range(10):
            row_canvases = []
            for col in range(10):
                canvas = ctk.CTkCanvas(self.root, width=50, height=50, bg="SystemButtonFace", highlightthickness=1)
                canvas.grid(row=row, column=col, padx=FRAME_PADX, pady=FRAME_PADY)
                canvas.bind("<Button-1>", lambda e, r=row, c=col: self.on_canvas_click(r, c))
                canvas.configure(highlightthickness=0)
                row_canvases.append(canvas)
            self.canvases.append(row_canvases)

    def create_toggle_button(self):
        self.toggle_button = ctk.CTkButton(self.root, text="Toggle Grid Borders", command=self.toggle_grid_borders)
        self.toggle_button.grid(row=10, column=0, columnspan=10)

    def on_canvas_click(self, row, col):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Select Component")
        popup.attributes('-topmost', True)  # Ensure the popup is on top

        label = ctk.CTkLabel(popup, text=f"Row: {row}, Column: {col}")
        label.pack(pady=LABEL_PADY)

        resistor_button = ctk.CTkButton(popup, text="Resistor", 
                                       command=lambda: [self.draw_component(row, col, "Resistor"), popup.destroy()])
        resistor_button.pack(pady=BUTTON_PADY)

        inductor_button = ctk.CTkButton(popup, text="Inductor", 
                                       command=lambda: [self.draw_component(row, col, "Inductor"), popup.destroy()])
        inductor_button.pack(pady=BUTTON_PADY)

        capacitor_button = ctk.CTkButton(popup, text="Capacitor", 
                                       command=lambda: [self.draw_component(row, col, "Capacitor"), popup.destroy()])
        capacitor_button.pack(pady=BUTTON_PADY)

        rotate_button = ctk.CTkButton(popup, text="Rotate 90°", 
                                    command=lambda: [self.rotate_component(row, col), popup.destroy()])
        rotate_button.pack(pady=BUTTON_PADY)

        close_button = ctk.CTkButton(popup, text="Close", command=popup.destroy)
        close_button.pack(pady=BUTTON_PADY)

    def draw_component(self, row, col, component_type):
        canvas = self.canvases[row][col]
        canvas.delete("all")  # Clear any existing drawings

        # Puntos centrales del canvas ajustados al tamaño del canvas
        x1, y1 = 0, canvas.winfo_height() // 2
        x2, y2 = canvas.winfo_width(), canvas.winfo_height() // 2

        # Guardar los elementos dibujados en una lista
        canvas.elements = []

        if component_type == "Resistor":
            # Dibujar resistencia
            line1 = canvas.create_line(x1, y1, x1 + 5, y1, fill="black", width=2)
            rect = canvas.create_rectangle(x1 + 5, y1 - 5, x2 - 5, y1 + 5, outline="black", width=2)
            line2 = canvas.create_line(x2 - 5, y1, x2, y1, fill="black", width=2)
            canvas.elements.extend([line1, rect, line2])

        elif component_type == "Inductor":
            # Dibujar inductor
            line1 = canvas.create_line(x1, y1, x1 + 5, y1, fill="black", width=2)
            arc1 = canvas.create_arc(x1 + 5, y1 - 5, x1 + 15, y1 + 5, start=0, extent=180, style='arc', outline="black", width=2)
            arc2 = canvas.create_arc(x1 + 15, y1 - 5, x1 + 25, y1 + 5, start=0, extent=180, style='arc', outline="black", width=2)
            arc3 = canvas.create_arc(x1 + 25, y1 - 5, x1 + 35, y1 + 5, start=0, extent=180, style='arc', outline="black", width=2)
            line2 = canvas.create_line(x2 - 5, y1, x2, y1, fill="black", width=2)
            canvas.elements.extend([line1, arc1, arc2, arc3, line2])

        elif component_type == "Capacitor":
            # Dibujar capacitor
            line1 = canvas.create_line(x1, y1, x1 + 15, y1, fill="black", width=2)
            line2 = canvas.create_line(x1 + 15, y1 - 10, x1 + 15, y1 + 10, fill="black", width=2)
            line3 = canvas.create_line(x1 + 25, y1 - 10, x1 + 25, y1 + 10, fill="black", width=2)
            line4 = canvas.create_line(x1 + 25, y1, x2, y1, fill="black", width=2)
            canvas.elements.extend([line1, line2, line3, line4])

        # Guardar el canvas en el frame para acceder a él más tarde
        canvas.canvas = canvas

    def rotate_component(self, row, col):
        canvas = self.canvases[row][col]
        if hasattr(canvas, 'elements'):
            for item in canvas.elements:
                coords = canvas.coords(item)
                if coords:  # Verificar que coords no es None
                    # Rotar coordenadas
                    center_x = canvas.winfo_width() / 2
                    center_y = canvas.winfo_height() / 2
                    new_coords = []
                    for i in range(0, len(coords), 2):
                        x = coords[i] - center_x
                        y = coords[i+1] - center_y
                        new_x = -y + center_x
                        new_y = x + center_y
                        new_coords.extend([new_x, new_y])
                    canvas.coords(item, *new_coords)

    def toggle_grid_borders(self):
        self.grid_visible = not self.grid_visible
        for row_canvases in self.canvases:
            for canvas in row_canvases:
                if self.grid_visible:
                    canvas.configure(highlightthickness=1)
                else:
                    canvas.configure(highlightthickness=0)

if __name__ == "__main__":
    root = ctk.CTk()
    app = GridApp(root)
    root.mainloop()
