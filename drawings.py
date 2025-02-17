import customtkinter as ctk
from tkinter import messagebox
import math


# Constants for padding
LABEL_PADY = 10
PADDING = 5
LINE_WIDTH = 2  # Constant for line width

class CanvasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Single Canvas")

        self.created_dots = []
        
        self.canvas = ctk.CTkCanvas(self.root, width=500, height=500, bg="SystemButtonFace", highlightthickness=1)
        self.canvas.pack()

        self.canvas.bind("<Button-1>", self.on_canvas_click)    # Bind click event
        self.canvas.bind("<Motion>", self.on_mouse_move)  # Bind mouse motion event

        self.canvas.elements = []   # List to store all elements
        self.component_options = ["Select Component", "Resistor", "Inductor", "Capacitor", "Resistor3"]
        self.len_component_options = len(self.component_options)

        self.parameters_labels = ["point 1","offset point 2"," offset point 3","orientation","scale"]

        
        self.coord_label = ctk.CTkLabel(self.root, text="")
        self.coord_label.pack()

        self.log_button = ctk.CTkButton(self.root, text="Print Log", command=self.print_log)
        self.log_button.pack(pady=PADDING)

        self.log_button_dots = ctk.CTkButton(self.root, text="Print Dots", command=lambda: print(self.created_dots))
        self.log_button_dots.pack(pady=PADDING)

        self.log_button_dots_1 = ctk.CTkButton(self.root, text="Print Dots 1", command=lambda: print(self.created_dots[0][0]))
        self.log_button_dots_1.pack(pady=PADDING)


    def on_mouse_move(self, event):
        if hasattr(event, '_generated'):
            return
        
        for dot in self.created_dots:
            dot_x, dot_y = dot
            distance = ((event.x - dot_x)**2 + (event.y - dot_y)**2)**0.5
            
            if distance < 10:
                self.coord_label.configure(text=f"X: {dot_x}, Y: {dot_y}")
                self.canvas.create_rectangle(dot_x - 10, dot_y - 10, dot_x + 10, dot_y + 10, outline="red", tag="cursor_marker")
                self.x_pos = dot_x
                self.y_pos = dot_y
                break
        else:
            self.coord_label.configure(text=f"X: {event.x}, Y: {event.y}")
            self.canvas.delete("cursor_marker")
            self.x_pos = event.x
            self.y_pos = event.y
        

    def on_canvas_click(self, event):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Select Component")
        popup.attributes('-topmost', True)  # Ensure the popup is on top
        popup.geometry("300x700")  # Define the dimensions of the popup
        #popup.grab_set()  # Configure grab_set to prevent interaction with other windows

        self.coord_x = self.x_pos    #save the coordinates of the click
        self.coord_y = self.y_pos    #save the coordinates of the click



        label = ctk.CTkLabel(popup, text=f"X: {self.coord_x}, Y: {self.coord_y}")  #show the coordinates of the click

        frame_paremeters=ctk.CTkFrame(popup)    #frame for parameters
        parameters_data = self.create_parameters_frames(frame_paremeters)

        self.position_parameters_frames(parameters_data)

        parameters_data[0][2].insert(0, f"[{self.coord_x}, {self.coord_y}]")
        #parameters_data[1][2].insert(0, str(self.coord_y))

        parameters_data[0][2].configure(state='disabled')
        #parameters_data[1][2].configure(state='disabled')
        
        component_dropdown = ctk.CTkComboBox(popup, values=self.component_options)
        component_dropdown.set(self.component_options[-1])
        self.item_selected = component_dropdown.get()
        component_dropdown.configure(command=lambda value: self.set_item_selected(value))

        #select_button = ctk.CTkButton(popup, text="Select", command=lambda: [self.draw_component(coord_x, coord_y, component_var.get()), popup.destroy()])
        select_button = ctk.CTkButton(popup, text="Select", command=lambda: self.draw_component(self.coord_x, self.coord_y, self.item_selected, parameters_data))
        
        
        popup.grid_columnconfigure(0, weight=1)  # Make the column expandable
        label.grid(row=0, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        component_dropdown.grid(row=1, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        select_button.grid(row=2, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        frame_paremeters.grid(row=3, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
 
        frame_paremeters.grid_rowconfigure(0, weight=1)  # Make frame1 occupy all the space of its container
        frame_paremeters.grid_columnconfigure(0, weight=1)  # Make frame1 occupy all the space of its container


        self.created_dots.append([self.coord_x, self.coord_y])

    def set_item_selected(self, value):
        self.item_selected = value

    def position_parameters_frames(self, parameters_data):
        for i in range(len(self.parameters_labels)):
            frame_items = parameters_data[i]
            frame_items[0].grid(row=i, column=0, pady=PADDING, padx=PADDING, sticky='nsew')

            frame_items[0].grid_columnconfigure(0, weight=1)
            frame_items[0].grid_columnconfigure(1, weight=1)
            frame_items[0].grid_rowconfigure(i, weight=1)


            frame_items[1].grid(row=0, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
            frame_items[2].grid(row=0, column=1, pady=PADDING, padx=PADDING, sticky='e')

    def create_parameters_frames(self, frame_paremeters):
        frames_parameters = []
        for i in range(len(self.parameters_labels)):
            frame_items =[]
            if i == 3:
                
                frame_item = ctk.CTkFrame(frame_paremeters)
                frame_item_label = ctk.CTkLabel(frame_item, text=self.parameters_labels[i], justify='center')
                combo_options = ["N", "S", "E", "W"]
                frame_item_entry = ctk.CTkComboBox(frame_item, values=combo_options)
                frame_item_entry.set(combo_options[0])
            else:
                
                frame_item = ctk.CTkFrame(frame_paremeters)
                frame_item_label = ctk.CTkLabel(frame_item, text=self.parameters_labels[i], justify='center')
                frame_item_entry = ctk.CTkEntry(frame_item, justify='center')

            frame_items.append(frame_item)
            frame_items.append(frame_item_label)
            frame_items.append(frame_item_entry)

            frames_parameters.append(frame_items)
            

        return frames_parameters

    def draw_component(self, x, y, component_type, parameters_data):
        # Puntos centrales del canvas ajustados al tamaño del canvas
        x1, y1 = x, y
        x2, y2 = x + 50, y

        point_1 = [self.coord_x, self.coord_y]
        offset_point_2 = parameters_data[1][2].get()
        offset_point_3 = parameters_data[2][2].get()
        orientation = parameters_data[3][2].get()
        scale = parameters_data[4][2].get()

        

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
            self.draw_capacitor(self.canvas, point_1, [x2, y2])
        elif component_type == "Resistor3":
            message = f"self.draw_resistor3(self.canvas, [{x1}, {y1}], {offset_point_2}, {offset_point_3}, {orientation}, {scale})"
            print(message)
            self.log_message(message)
            self.draw_resistor3(self.canvas, point_1, offset_point_2, int(offset_point_3), orientation, int(scale))

        #self.print_all_data_entries(parameters_data)

    def print_all_data_entries(self, frames_parameters):
        for frame_items in frames_parameters:
            entry = frame_items[2]  # Assuming the entry widget is the third item in the list
            print(entry.get())

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
        line1 = canvas.create_line(x1, y1, x1 + 5, y1, fill="black", width=LINE_WIDTH)
        rect = canvas.create_rectangle(x1 + 5, y1 - 5, x1 + 15, y1 + 5, outline="black", width=LINE_WIDTH)
        line2 = canvas.create_line(x1 + 15, y1, x2, y2, fill="black", width=LINE_WIDTH)
        canvas.elements.extend([line1, rect, line2])

    def draw_resistor4(self, canvas, pmain, offset_center, offset_final, orientation, scale):


        #-----------------------------------------offset center feature-----------------------------------------

        if offset_center == "c":
            point_center_var = offset_final*0.5

        else:
            if int(offset_center) >= int(offset_final):
                point_center_var = int(offset_final * 0.9)
                print("-----------------------------------------maximum offset center reached-----------------------------------------")
            else:
                point_center_var = int(offset_center)

        #-----------------------------------------coordinates definition-----------------------------------------

        match orientation:
            case "N":
                y1 = pmain[1]
                y2 = pmain[1] - point_center_var
                y3 = pmain[1] - int(offset_final)

                x = pmain[0]
                x3 = x
            case "S":
                y1 = pmain[1]
                y2 = pmain[1] + point_center_var
                y3 = pmain[1] + int(offset_final)

                x = pmain[0]
                x3 = x
            case "E":
                x1 = pmain[0]
                x2 = pmain[0] + point_center_var
                x3 = pmain[0] + int(offset_final)

                y = pmain[1]
                y3 = y
            case "W":
                x1 = pmain[0]
                x2 = pmain[0] - point_center_var
                x3 = pmain[0] - int(offset_final)

                y = pmain[1]
                y3 = y

        self.created_dots.append([x3,y3])

        #-----------------------------------------rectangle size definition-----------------------------------------

        if orientation == "E" or orientation == "W":
            
            rectangle_width = 1 * scale
            rectangle_height = int(round(rectangle_width * 0.4))
            
            if rectangle_width >= abs(x3-x1):
                rectangle_width = abs(x3-x1)*0.9
                print("-----------------------------------------maximum total width available-----------------------------------------")

            if offset_center != "c" and (rectangle_width*0.5 >= abs(y2-y1) or rectangle_width*0.5 >= abs(y3-y2)):
                if abs(y3-y2) > abs(y2-y1):
                    rectangle_width = abs(y2-y1)*0.9

                if abs(y2-y1) > abs(y3-y2):
                    rectangle_width = abs(y3-y2)*0.9

                print("-----------------------------------------maximum width to one side available-----------------------------------------")

        if orientation == "N" or orientation == "S":
            
            rectangle_height = 1 * scale
            rectangle_width = int(round(rectangle_height * 0.4))

            if rectangle_height >= abs(y3-y1):
                rectangle_height = abs(y3-y1)*0.9
                print("-----------------------------------------maximum total height reached-----------------------------------------")            

            if offset_center != "c" and (rectangle_height*0.5 >= abs(y2-y1) or rectangle_height*0.5 >= abs(y3-y2)):
                if abs(y3-y2) > abs(y2-y1):
                    rectangle_height = abs(y2-y1)*0.9

                if abs(y2-y1) > abs(y3-y2):
                    rectangle_height = abs(y3-y2)*0.9

                print("-----------------------------------------maximum height to one side available-----------------------------------------")

        aux_sign_h = 1  #only for rectangle dimensions
        aux_sign_v = 1  #only for rectangle dimensions

        match orientation:
            case "E" | "W":

                if orientation == "W":
                    aux_sign_h = -1

                line1 = canvas.create_line(x1, y, x2 - aux_sign_h * rectangle_width/2, y, fill="black", width=LINE_WIDTH)

                rect = canvas.create_rectangle(x2-aux_sign_h * rectangle_width/2, y - aux_sign_h * rectangle_height/2,
                                                x2 + aux_sign_h * rectangle_width/2, y + aux_sign_h * rectangle_height/2,
                                                  outline="black", width=LINE_WIDTH)

                line2 = canvas.create_line(x2 + aux_sign_h * rectangle_width/2, y, x3, y, fill="black", width=LINE_WIDTH)

            case "N" | "S":

                if orientation == "N":
                    aux_sign_v = -1

                line1 = canvas.create_line(x, y1, x, y2 - aux_sign_v * rectangle_height/2, fill="black", width=LINE_WIDTH)

                rect = canvas.create_rectangle(x - aux_sign_v * rectangle_width/2, y2 - aux_sign_v * rectangle_height/2,
                                                x + aux_sign_v * rectangle_width/2, y2 + aux_sign_v * rectangle_height/2,
                                                  outline="black", width=LINE_WIDTH)

                line2 = canvas.create_line(x, y2 + aux_sign_v * rectangle_height/2, x, y3, fill="black", width=LINE_WIDTH)

        canvas.elements.extend([line1, rect, line2])

    def draw_resistor3(self, canvas, pmain, offset_center, offset_final, orientation, scale):

        #-----------------------------------------offset center feature-----------------------------------------

        if offset_center == "":
            offset_center_var = int(offset_final) * 0.5
            offset_final_var = int(offset_final) * 0.5
        else:
            offset_center_var = int(offset_center)
            offset_final_var = int(offset_final)

        #-------------------------------------------points definition-----------------------------------------


        p_start = pmain
        p_ref_center = [p_start[0] + offset_center_var, p_start[1]]  # center of rectangle
        p_ref_final = [p_start[0] + offset_final_var + offset_center_var, p_start[1]]

        #-------------------------------------------rectangle size definition-----------------------------------------

        ASPECT_RATIO = 0.4
        MIN_WIDTH = 10

        if scale == "":
            rectangle_width = MIN_WIDTH
        else:
            rectangle_width = int(round(scale))

        if rectangle_width >= 0.9 *abs(p_ref_center[0] - p_start[0]) or rectangle_width >= 0.9 * abs(p_ref_center[0] - p_ref_final[0]):
            if abs(p_ref_center[0] - p_start[0]) > abs(p_ref_center[0] - p_ref_final[0]):
                rectangle_width = abs(p_ref_center[0] - p_ref_final[0])*0.9
            else:
                rectangle_width = abs(p_ref_center[0] - p_start[0])*0.9

            print("-----------------------------------------maximum size reached, check scale-----------------------------------------")

        rectangle_height = int(round(rectangle_width * ASPECT_RATIO))

        #-------------------------------------------rectangle points definition-----------------------------------------

        p_ref_start_rectangle =[ p_ref_center[0] - rectangle_width, p_start[1]]   #start of rectangle

        p_ref_corner_1 = [p_ref_center[0] - rectangle_width, p_ref_center[1] + rectangle_height] #first corner of rectangle
        p_ref_corner_2 = [p_ref_center[0] + rectangle_width, p_ref_center[1] - rectangle_height] #second corner of rectangle

        p_ref_end_rectangle =[ p_ref_center[0] + rectangle_width, p_start[1]]   #end of rectangle

        match orientation:
            case "N":
                ANGLE = 270
                p_center = self.rotate_point(p_start, p_ref_center, ANGLE)
                p_final = self.rotate_point(p_start, p_ref_final, ANGLE)
                
                p_start_rectangle = self.rotate_point(p_start, p_ref_start_rectangle, ANGLE)
                p_corner_1 = self.rotate_point(p_start, p_ref_corner_1, ANGLE)
                p_corner_2 = self.rotate_point(p_start, p_ref_corner_2, ANGLE)
                p_end_rectangle = self.rotate_point(p_start, p_ref_end_rectangle, ANGLE)        

            case "S":
                ANGLE = 90
                p_center = self.rotate_point(p_start, p_ref_center, ANGLE)
                p_final = self.rotate_point(p_start, p_ref_final, ANGLE)
                
                p_start_rectangle = self.rotate_point(p_start, p_ref_start_rectangle, ANGLE)
                p_corner_1 = self.rotate_point(p_start, p_ref_corner_1, ANGLE)
                p_corner_2 = self.rotate_point(p_start, p_ref_corner_2, ANGLE)
                p_end_rectangle = self.rotate_point(p_start, p_ref_end_rectangle, ANGLE)        

            case "E":
                ANGLE = 0
                p_center = self.rotate_point(p_start, p_ref_center, ANGLE)
                p_final = self.rotate_point(p_start, p_ref_final, ANGLE)
                
                p_start_rectangle = self.rotate_point(p_start, p_ref_start_rectangle, ANGLE)
                p_corner_1 = self.rotate_point(p_start, p_ref_corner_1, ANGLE)
                p_corner_2 = self.rotate_point(p_start, p_ref_corner_2, ANGLE)
                p_end_rectangle = self.rotate_point(p_start, p_ref_end_rectangle, ANGLE)        

            case "W":
                ANGLE = 180
                p_center = self.rotate_point(p_start, p_ref_center, ANGLE)
                p_final = self.rotate_point(p_start, p_ref_final, ANGLE)
                
                p_start_rectangle = self.rotate_point(p_start, p_ref_start_rectangle, ANGLE)
                p_corner_1 = self.rotate_point(p_start, p_ref_corner_1, ANGLE)
                p_corner_2 = self.rotate_point(p_start, p_ref_corner_2, ANGLE)
                p_end_rectangle = self.rotate_point(p_start, p_ref_end_rectangle, ANGLE)        
                


        x1, y1 = p_start
        x2, y2 = p_start_rectangle
        x3, y3 = p_corner_1
        x4, y4 = p_center
        x5, y5 = p_corner_2
        x6, y6 = p_end_rectangle
        x7, y7 = p_final

        self.created_dots.append(p_final)


        line1 = canvas.create_line(x1, y1, x2, y2, fill="black", width=LINE_WIDTH)

        rect = canvas.create_rectangle(x3, y3, x5, y5,outline="black", width=LINE_WIDTH)

        line2 = canvas.create_line(x6, y6, x7, y7, fill="black", width=LINE_WIDTH)

        canvas.elements.extend([line1, rect, line2])

    def rotate_point(self, p1, p2, rotation):
        
        x1, y1 = p1
        x2, y2 = p2

        # Convert rotation angle to radians
        theta = math.radians(rotation)

        # Translate point p2 to origin
        translated_x = x2 - x1
        translated_y = y2 - y1

        # Rotate point
        rotated_x = translated_x * math.cos(theta) - translated_y * math.sin(theta)
        rotated_y = translated_x * math.sin(theta) + translated_y * math.cos(theta)

        # Translate point back
        new_x2 = rotated_x + x1
        new_y2 = rotated_y + y1

        return [new_x2, new_y2]
    
    def draw_inductor(self, canvas, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        line1 = canvas.create_line(x1, y1, x1 + 5, y1, fill="black", width=LINE_WIDTH)
        arc1 = canvas.create_arc(x1 + 5, y1 - 5, x1 + 15, y1 + 5, start=0, extent=180, style='arc', outline="black", width=LINE_WIDTH)
        arc2 = canvas.create_arc(x1 + 15, y1 - 5, x1 + 25, y1 + 5, start=0, extent=180, style='arc', outline="black", width=LINE_WIDTH)
        arc3 = canvas.create_arc(x1 + 25, y1 - 5, x1 + 35, y1 + 5, start=0, extent=180, style='arc', outline="black", width=LINE_WIDTH)
        line2 = canvas.create_line(x1 + 35, y1, x2, y2, fill="black", width=LINE_WIDTH)
        canvas.elements.extend([line1, arc1, arc2, arc3, line2])

    def draw_capacitor(self, canvas, p1, p2):
        x1, y1 = p1
        x2, y2 = p2
        line1 = canvas.create_line(x1, y1, x1 + 15, y1, fill="black", width=LINE_WIDTH)
        line2 = canvas.create_line(x1 + 15, y1 - 10, x1 + 15, y1 + 10, fill="black", width=LINE_WIDTH)
        line3 = canvas.create_line(x1 + 25, y1 - 10, x1 + 25, y1 + 10, fill="black", width=LINE_WIDTH)
        line4 = canvas.create_line(x1 + 25, y1, x2, y1, fill="black", width=LINE_WIDTH)
        canvas.elements.extend([line1, line2, line3, line4])

if __name__ == "__main__":
    root = ctk.CTk()
    app = CanvasApp(root)
    root.mainloop()
