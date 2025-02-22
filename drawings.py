import customtkinter as ctk
from tkinter import messagebox
import math
import csv
from tkinter import filedialog


# Constants for padding
LABEL_PADY = 10
PADDING = 5
LINE_WIDTH = 2  # Constant for line width
FONT_FAMILY = "Arial"

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
        self.canvas_memory_asignation = []  #to store and erase elements
        self.id_elements_deleted = []

        self.component_options = ["Select Component", "Resistor", "Inductor", "Capacitor", "Rectangle", "Text"]
        self.len_component_options = len(self.component_options)

        self.parameters_labels = ["start x","start y","offset point 2"," offset point 3","orientation","scale", "text", "offset x", "offset y"]
        
        self.coord_label = ctk.CTkLabel(self.root, text="")
        self.coord_label.pack()

    def on_mouse_move(self, event):
        
        if hasattr(event, '_generated'):
            return     

        for dot in self.created_dots:
            dot_x, dot_y = dot
            distance = ((event.x - dot_x)**2 + (event.y - dot_y)**2)**0.5
            
            if distance < 10:
                self.coord_label.configure(text=f"X: {dot_x}, Y: {dot_y}")
                
                self.x_pos = dot_x
                self.y_pos = dot_y
                closest = self.canvas.find_closest(self.x_pos, self.y_pos)
                self.selected_element = closest[0] if closest else None
                #self.canvas.create_rectangle(dot_x - 10, dot_y - 10, dot_x + 10, dot_y + 10, outline="red", tag="cursor_marker")
                #print(f"canvas.elements: {self.canvas.elements}")
                #print(f"self.selected_element: {self.selected_element}")
                 
                break
        else:
            self.coord_label.configure(text=f"X: {event.x}, Y: {event.y}")
            #self.canvas.delete("cursor_marker")
            self.x_pos = event.x
            self.y_pos = event.y
            closest = self.canvas.find_closest(self.x_pos, self.y_pos)
            self.selected_element = closest[0] if closest else None
            #print(f"self.selected_element: {self.selected_element}")

    def find_closest_excluding(self, ids_to_ignore):
        # Obtener todos los elementos
        all_items = self.canvas.find_all()
        
        # Filtrar los elementos, excluyendo los IDs a ignorar
        filtered_items = [item for item in all_items if item not in ids_to_ignore]
        
        if filtered_items:
            # Encontrar el más cercano entre los elementos filtrados
            closest_filtered = min(filtered_items, key=lambda x: ((self.canvas.coords(x)[0] - self.x_pos)**2 + (self.canvas.coords(x)[1] - self.y_pos)**2)**0.5)
            return (closest_filtered,)  # Retorna como tupla para mantener formato de find_closest
        else:
            return ()  # Retorna tupla vacía si no hay elementos
        
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

        parameters_data[0][2].insert(0, self.coord_x)
        parameters_data[1][2].insert(0, self.coord_y)
  
        component_dropdown = ctk.CTkComboBox(popup, values=self.component_options)
        component_dropdown.set(self.component_options[-1])
        self.item_selected = component_dropdown.get()
        component_dropdown.configure(command=lambda value: self.set_item_selected(value))

        select_button = ctk.CTkButton(popup, text="Insert", command=lambda: self.draw_component(self.item_selected, parameters_data))
        delete_button = ctk.CTkButton(popup, text="Delete", command=lambda: self.delete_group_selected(self.selected_element))
        print_log_button = ctk.CTkButton(popup, text="Print Log", command=lambda: self.print_log())
        offset_button = ctk.CTkButton(popup, text="Offset", command=lambda: self.offset_component(self.selected_element, parameters_data))
        
        label.grid(row=0, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        component_dropdown.grid(row=1, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        select_button.grid(row=2, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        frame_paremeters.grid(row=3, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        delete_button.grid(row=4, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        print_log_button.grid(row=5, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
        offset_button.grid(row=6, column=0, pady=PADDING, padx=PADDING, sticky='nsew')
 
        popup.grid_columnconfigure(0, weight=1)  # Make the column expandable
        frame_paremeters.grid_rowconfigure(0, weight=1)  # Make frame1 occupy all the space of its container
        frame_paremeters.grid_columnconfigure(0, weight=1)  # Make frame1 occupy all the space of its container

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
            if i == 4:
                
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

    def draw_component(self, component_type, parameters_data):
        #x1, y1 = x, y
        #x2, y2 = x + 50, y

        x1= int(parameters_data[0][2].get())
        y1 = int(parameters_data[1][2].get())
        offset_point_2 = parameters_data[2][2].get()
        offset_point_3 = parameters_data[3][2].get()
        orientation = parameters_data[4][2].get()
        scale = parameters_data[5][2].get()
        text = parameters_data[6][2].get()
        offset_x = parameters_data[7][2].get()
        offset_y = parameters_data[8][2].get()

        if component_type == "Resistor":
            message = f"self.draw_resistor(self.canvas, [{x1}, {y1}], {offset_point_2}, {offset_point_3}, {orientation}, {scale})"
            print(message)
            parameters = [self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale]
            self.draw_resistor(self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale)
            self.log_message(message, self.id_element_created, parameters, "Resistor")
        elif component_type == "Inductor":
            message = f"self.draw_inductor(self.canvas, [{x1}, {y1}], {offset_point_2}, {offset_point_3}, {orientation}, {scale})"
            print(message)
            parameters = [self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale]
            self.draw_inductor(self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale)
            self.log_message(message, self.id_element_created, parameters, "Inductor")
        elif component_type == "Capacitor":
            message = f"self.draw_capacitor(self.canvas, [{x1}, {y1}], {offset_point_2}, {offset_point_3}, {orientation}, {scale})"
            print(message)
            parameters = [self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale]
            self.draw_capacitor(self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale)
            self.log_message(message, self.id_element_created, parameters, "Capacitor")
        elif component_type == "Rectangle":
            message = f"self.draw_rectangle(self.canvas, [{x1}, {y1}], {offset_point_2}, {offset_point_3}, {orientation}, {scale})"
            print(message)
            parameters = [self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale]
            self.draw_rectangle(self.canvas, [x1, y1], offset_point_2, offset_point_3, orientation, scale)
            self.log_message(message, self.id_element_created, parameters, "Rectangle")
        elif component_type == "Text":
            message = f"self.draw_text(self.canvas, [{x1}, {y1}], {text}, {scale})"
            print(message)
            parameters = [self.canvas, [x1, y1], text, scale]
            self.draw_text(self.canvas, [x1, y1], text, scale)
            self.log_message(message, self.id_element_created, parameters, "Text")

        self.created_dots.append([self.coord_x, self.coord_y])

    def offset_component(self, id_element, parameters_data):
        
        id_info = None
        offset_x = int(parameters_data[7][2].get())
        offset_y = int(parameters_data[8][2].get())

        id_group = self.get_id_group(id_element)

        for i in range(len(self.log)):
            if self.log[i][1] == id_group:
                id_info = self.log[i]

        if id_info is None:
            print("No hay elemento seleccionado")
            return
        
        print(f"id_info: {id_info}")

        if offset_x != "" or offset_y != "":

            

            x1 = id_info[2][1][0] + offset_x
            y1 = id_info[2][1][1] + offset_y

            

            if id_info[3] == "Resistor":
                message = f"self.draw_resistor({id_info[2][0]}, [{x1}, {y1}], {id_info[2][2]}, {id_info[2][3]}, {id_info[2][4]}, {id_info[2][5]})"
                parameters = [id_info[2][0], [x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5]]
                self.draw_resistor(id_info[2][0],[x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5])
                self.log_message(message, self.id_element_created, parameters, "Resistor")
            elif id_info[3] == "Inductor":
                message = f"self.draw_inductor({id_info[2][0]}, [{x1}, {y1}], {id_info[2][2]}, {id_info[2][3]}, {id_info[2][4]}, {id_info[2][5]})"
                parameters = [id_info[2][0], [x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5]]
                self.draw_inductor(id_info[2][0],[x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5])
                self.log_message(message, self.id_element_created, parameters, "Inductor")
            elif id_info[3] == "Capacitor":
                message = f"self.draw_capacitor({id_info[2][0]}, [{x1}, {y1}], {id_info[2][2]}, {id_info[2][3]}, {id_info[2][4]}, {id_info[2][5]})"
                parameters = [id_info[2][0], [x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5]]
                self.draw_capacitor(id_info[2][0],[x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5])
                self.log_message(message, self.id_element_created, parameters, "Capacitor")
            elif id_info[3] == "Rectangle":
                message = f"self.draw_rectangle({id_info[2][0]}, [{x1}, {y1}], {id_info[2][2]}, {id_info[2][3]}, {id_info[2][4]}, {id_info[2][5]})"
                parameters = [id_info[2][0], [x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5]]
                self.draw_rectangle(id_info[2][0],[x1, y1], id_info[2][2], id_info[2][3], id_info[2][4], id_info[2][5])
                self.log_message(message, self.id_element_created, parameters, "Rectangle")
            elif id_info[3] == "Text":
                message = f"self.draw_text({id_info[2][0]}, [{x1}, {y1}], {id_info[2][2]}, {id_info[2][3]})"
                parameters = [id_info[2][0], [x1, y1], id_info[2][2], id_info[2][3]]
                self.draw_text(id_info[2][0],[x1, y1], id_info[2][2], id_info[2][3])
                self.log_message(message, self.id_element_created, parameters, "Text")

            self.delete_group_selected(id_element)
        
    def print_all_data_entries(self, frames_parameters):
        for frame_items in frames_parameters:
            entry = frame_items[2]  # Assuming the entry widget is the third item in the list
            print(entry.get())

    def log_message(self, message, id_element, parameters, component_type):
        if not hasattr(self, 'log'):
            self.log = []
        
        self.log.append([message, id_element, parameters, component_type])

    def print_log2(self):
        if len(self.log) >= 1:

            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file, delimiter='|', quoting=csv.QUOTE_NONE, escapechar='|')
                    for item in self.log:
                        writer.writerow(item[0])

    def print_log(self):
        if len(self.log) >= 1:
            file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
            if file_path:
                with open(file_path, mode='w', newline='') as file:
                    writer = csv.writer(file, delimiter='|')
                    for item in self.log:
                        writer.writerow([item[0]])  # Envolver item[0] en una lista

    def draw_resistor(self, canvas, pmain, offset_center, offset_final, orientation, scale):
        
        FINAL_OFFSET_RESISTOR_DEFAULT = 100
        SCALE_RESISTOR_DEFAULT = 10

        if offset_final =="":
            offset_final = FINAL_OFFSET_RESISTOR_DEFAULT
        if scale == "":
            scale = SCALE_RESISTOR_DEFAULT

        #-----------------------------------------offset center feature-----------------------------------------

        if offset_center == "" or int(offset_center) == 0:
            offset_center_var = int(offset_final) * 0.5
            offset_final_var = int(offset_final) * 0.5
        else:
            offset_center_var = int(offset_center)
            offset_final_var = int(offset_final)

        #-------------------------------------------points definition-----------------------------------------


        p_start = pmain
        p_ref_center = [p_start[0] + offset_center_var, p_start[1]]  # center of rectangle
        p_ref_end = [p_start[0] + offset_final_var + offset_center_var, p_start[1]]

        zigzag_size = int(scale)

        if zigzag_size * 1.5 >= 0.9 *abs(p_ref_center[0] - p_start[0]) or zigzag_size * 1.5 >= 0.9 * abs(p_ref_center[0] - p_ref_end[0]):
            if abs(p_ref_center[0] - p_start[0]) > abs(p_ref_center[0] - p_ref_end[0]):
                zigzag_size = abs(p_ref_center[0] - p_ref_end[0]) * 0.9 * (2/3)   
            else:
                zigzag_size = abs(p_ref_center[0] - p_start[0]) * 0.9 * (2/3)

            print("-----------------------------------------maximum size reached, check scale-----------------------------------------")

        p_ref_start_zig_1 = [p_ref_center[0] - zigzag_size * 1.5, p_start[1]]
        p_ref_top_zig_1 = [p_ref_center[0] - zigzag_size * 1, p_ref_center[1] - zigzag_size]

        p_ref_start_zig_2 = [p_ref_center[0] - zigzag_size * 0.5, p_ref_center[1]]
        p_ref_top_zig_2 = [p_ref_center[0], p_ref_center[1] - zigzag_size]

        p_ref_start_zig_3 = [p_ref_center[0] + zigzag_size * 0.5, p_ref_center[1]]
        p_ref_top_zig_3 = [p_ref_center[0] + zigzag_size * 1, p_ref_center[1] - zigzag_size]
        p_ref_end_zig_3 = [p_ref_center[0] + zigzag_size * 1.5, p_start[1]]

        match orientation:
            case "N":
                ANGLE = 270
                p_start_zig_1 = self.rotate_point(p_start, p_ref_start_zig_1, ANGLE)
                p_top_zig_1 = self.rotate_point(p_start, p_ref_top_zig_1, ANGLE)
                p_start_zig_2 = self.rotate_point(p_start, p_ref_start_zig_2, ANGLE)
                p_top_zig_2 = self.rotate_point(p_start, p_ref_top_zig_2, ANGLE)
                p_start_zig_3 = self.rotate_point(p_start, p_ref_start_zig_3, ANGLE)
                p_top_zig_3 = self.rotate_point(p_start, p_ref_top_zig_3, ANGLE)
                p_end_zig_3 = self.rotate_point(p_start, p_ref_end_zig_3, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)
                
            case "S":
                ANGLE = 90
                p_start_zig_1 = self.rotate_point(p_start, p_ref_start_zig_1, ANGLE)
                p_top_zig_1 = self.rotate_point(p_start, p_ref_top_zig_1, ANGLE)
                p_start_zig_2 = self.rotate_point(p_start, p_ref_start_zig_2, ANGLE)
                p_top_zig_2 = self.rotate_point(p_start, p_ref_top_zig_2, ANGLE)
                p_start_zig_3 = self.rotate_point(p_start, p_ref_start_zig_3, ANGLE)
                p_top_zig_3 = self.rotate_point(p_start, p_ref_top_zig_3, ANGLE)
                p_end_zig_3 = self.rotate_point(p_start, p_ref_end_zig_3, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

            case "E":
                ANGLE = 0
                p_start_zig_1 = self.rotate_point(p_start, p_ref_start_zig_1, ANGLE)
                p_top_zig_1 = self.rotate_point(p_start, p_ref_top_zig_1, ANGLE)
                p_start_zig_2 = self.rotate_point(p_start, p_ref_start_zig_2, ANGLE)
                p_top_zig_2 = self.rotate_point(p_start, p_ref_top_zig_2, ANGLE)
                p_start_zig_3 = self.rotate_point(p_start, p_ref_start_zig_3, ANGLE)
                p_top_zig_3 = self.rotate_point(p_start, p_ref_top_zig_3, ANGLE)
                p_end_zig_3 = self.rotate_point(p_start, p_ref_end_zig_3, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

            case "W":
                ANGLE = 180
                p_start_zig_1 = self.rotate_point(p_start, p_ref_start_zig_1, ANGLE)
                p_top_zig_1 = self.rotate_point(p_start, p_ref_top_zig_1, ANGLE)
                p_start_zig_2 = self.rotate_point(p_start, p_ref_start_zig_2, ANGLE)
                p_top_zig_2 = self.rotate_point(p_start, p_ref_top_zig_2, ANGLE)
                p_start_zig_3 = self.rotate_point(p_start, p_ref_start_zig_3, ANGLE)
                p_top_zig_3 = self.rotate_point(p_start, p_ref_top_zig_3, ANGLE)
                p_end_zig_3 = self.rotate_point(p_start, p_ref_end_zig_3, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)
                
        x1, y1 = p_start #start
        x2, y2 = p_start_zig_1 #start zigzag 1
        x3, y3 = p_top_zig_1 #top zigzag 1
        x4, y4 = p_start_zig_2 #start zigzag 2
        x5, y5 = p_top_zig_2 #top zigzag 2
        x6, y6 = p_start_zig_3 #start zigzag 3
        x7, y7 = p_top_zig_3 #top zigzag 3
        x8, y8 = p_end_zig_3 #end zigzag 3
        x9, y9 = p_end #end
        
        self.created_dots.append(p_end)
        

        lines = [
            canvas.create_line(x1, y1, x2, y2, fill="black", width=LINE_WIDTH),
            canvas.create_line(x2, y2, x3, y3, fill="black", width=LINE_WIDTH),
            canvas.create_line(x3, y3, x4, y4, fill="black", width=LINE_WIDTH),
            canvas.create_line(x4, y4, x5, y5, fill="black", width=LINE_WIDTH),
            canvas.create_line(x5, y5, x6, y6, fill="black", width=LINE_WIDTH),
            canvas.create_line(x6, y6, x7, y7, fill="black", width=LINE_WIDTH),
            canvas.create_line(x7, y7, x8, y8, fill="black", width=LINE_WIDTH),
            canvas.create_line(x8, y8, x9, y9, fill="black", width=LINE_WIDTH)
        ]

        self.canvas_elements_memory(lines)

    def draw_rectangle(self, canvas, pmain, offset_center, offset_final, orientation, scale):

        FINAL_OFFSET_RECTANGLE_DEFAULT = 100
        SCALE_RECTANGLE_DEFAULT = 10

        if offset_final =="":
            offset_final = FINAL_OFFSET_RECTANGLE_DEFAULT
        if scale == "":
            scale = SCALE_RECTANGLE_DEFAULT

        #-----------------------------------------offset center feature-----------------------------------------

        if offset_center == "" or int(offset_center) == 0:
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
            rectangle_width = int(scale)

        if rectangle_width * 0.5>= 0.9 *abs(p_ref_center[0] - p_start[0]) or rectangle_width * 0.5 >= 0.9 * abs(p_ref_center[0] - p_ref_final[0]):
            if abs(p_ref_center[0] - p_start[0]) > abs(p_ref_center[0] - p_ref_final[0]):
                rectangle_width = abs(p_ref_center[0] - p_ref_final[0])* 0.9 * 2
            else:
                rectangle_width = abs(p_ref_center[0] - p_start[0]) * 0.9 * 2

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

        lines = [
            canvas.create_line(x1, y1, x2, y2, fill="black", width=LINE_WIDTH),
            canvas.create_rectangle(x3, y3, x5, y5,outline="black", width=LINE_WIDTH),
            canvas.create_line(x6, y6, x7, y7, fill="black", width=LINE_WIDTH)
        ]

        self.canvas_elements_memory(lines)

    def draw_inductor(self, canvas, pmain, offset_center, offset_final, orientation, scale):
        
        FINAL_OFFSET_INDCUTOR_DEFAULT = 100
        SCALE_INDCUTOR_DEFAULT = 10

        if offset_final =="":
            offset_final = FINAL_OFFSET_INDCUTOR_DEFAULT
        if scale == "":
            scale = SCALE_INDCUTOR_DEFAULT

        #-----------------------------------------offset center feature-----------------------------------------

        if offset_center == "" or int(offset_center) == 0:
            offset_center_var = int(offset_final) * 0.5
            offset_final_var = int(offset_final) * 0.5
        else:
            offset_center_var = int(offset_center)
            offset_final_var = int(offset_final)

        #-------------------------------------------points definition-----------------------------------------


        p_start = pmain
        p_ref_center = [p_start[0] + offset_center_var, p_start[1]]  # center of rectangle
        p_ref_end = [p_start[0] + offset_final_var + offset_center_var, p_start[1]]

        width_arc = int(scale)

        if width_arc * 1.5 >= 0.9 *abs(p_ref_center[0] - p_start[0]) or width_arc * 1.5 >= 0.9 * abs(p_ref_center[0] - p_ref_end[0]):
            if abs(p_ref_center[0] - p_start[0]) > abs(p_ref_center[0] - p_ref_end[0]):
                width_arc = abs(p_ref_center[0] - p_ref_end[0]) * 0.9 * (2/3)   
            else:
                width_arc = abs(p_ref_center[0] - p_start[0]) * 0.9 * (2/3)

            print("-----------------------------------------maximum size reached, check scale-----------------------------------------")

        p_ref_start_fig = [p_ref_center[0] - width_arc * 1.5, p_start[1]]

        p_ref_init_arc_1 = [p_ref_center[0] - width_arc * 1.5, p_ref_center[1] + width_arc * 0.5]
        p_ref_end_arc_1 = [p_ref_center[0] - width_arc * 0.5, p_ref_center[1] - width_arc * 0.5]

        p_ref_init_arc_2 = [p_ref_center[0] - width_arc * 0.5, p_ref_center[1] + width_arc * 0.5]
        p_ref_end_arc_2 = [p_ref_center[0] + width_arc * 0.5, p_ref_center[1] - width_arc * 0.5]
        
        p_ref_init_arc_3 = [p_ref_center[0] + width_arc * 0.5, p_ref_center[1] + width_arc * 0.5]
        p_ref_end_arc_3 = [p_ref_center[0] + width_arc * 1.5, p_ref_center[1] - width_arc * 0.5]
        
        p_ref_end_fig = [p_ref_center[0] + width_arc * 1.5, p_ref_end[1]]

        match orientation:
            case "N":
                ANGLE = 270
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_init_arc_1 = self.rotate_point(p_start, p_ref_init_arc_1, ANGLE)
                p_end_arc_1 = self.rotate_point(p_start, p_ref_end_arc_1, ANGLE)
                p_init_arc_2 = self.rotate_point(p_start, p_ref_init_arc_2, ANGLE)
                p_end_arc_2 = self.rotate_point(p_start, p_ref_end_arc_2, ANGLE)
                p_init_arc_3 = self.rotate_point(p_start, p_ref_init_arc_3, ANGLE)
                p_end_arc_3 = self.rotate_point(p_start, p_ref_end_arc_3, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

                arc_angle = 270
            case "S":
                ANGLE = 90
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_init_arc_1 = self.rotate_point(p_start, p_ref_init_arc_1, ANGLE)
                p_end_arc_1 = self.rotate_point(p_start, p_ref_end_arc_1, ANGLE)
                p_init_arc_2 = self.rotate_point(p_start, p_ref_init_arc_2, ANGLE)
                p_end_arc_2 = self.rotate_point(p_start, p_ref_end_arc_2, ANGLE)
                p_init_arc_3 = self.rotate_point(p_start, p_ref_init_arc_3, ANGLE)
                p_end_arc_3 = self.rotate_point(p_start, p_ref_end_arc_3, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

                arc_angle = 270
            case "E":
                ANGLE = 0
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_init_arc_1 = self.rotate_point(p_start, p_ref_init_arc_1, ANGLE)
                p_end_arc_1 = self.rotate_point(p_start, p_ref_end_arc_1, ANGLE)
                p_init_arc_2 = self.rotate_point(p_start, p_ref_init_arc_2, ANGLE)
                p_end_arc_2 = self.rotate_point(p_start, p_ref_end_arc_2, ANGLE)
                p_init_arc_3 = self.rotate_point(p_start, p_ref_init_arc_3, ANGLE)
                p_end_arc_3 = self.rotate_point(p_start, p_ref_end_arc_3, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

                arc_angle = 0
            case "W":
                ANGLE = 180
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_init_arc_1 = self.rotate_point(p_start, p_ref_init_arc_1, ANGLE)
                p_end_arc_1 = self.rotate_point(p_start, p_ref_end_arc_1, ANGLE)
                p_init_arc_2 = self.rotate_point(p_start, p_ref_init_arc_2, ANGLE)
                p_end_arc_2 = self.rotate_point(p_start, p_ref_end_arc_2, ANGLE)
                p_init_arc_3 = self.rotate_point(p_start, p_ref_init_arc_3, ANGLE)
                p_end_arc_3 = self.rotate_point(p_start, p_ref_end_arc_3, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

                arc_angle = 0

        x1, y1 = p_start
        x2, y2 = p_start_fig
        x3, y3 = p_init_arc_1
        x4, y4 = p_end_arc_1
        x5, y5 = p_init_arc_2
        x6, y6 = p_end_arc_2
        x7, y7 = p_init_arc_3
        x8, y8 = p_end_arc_3
        x9, y9 = p_end_fig
        x10, y10 = p_end

        self.created_dots.append(p_end)

        lines = [
            canvas.create_line(x1, y1, x2, y2, fill="black", width=LINE_WIDTH),
            canvas.create_arc(x3, y3, x4, y4, start=arc_angle, extent=180, style='arc', outline="black", width=LINE_WIDTH),
            canvas.create_arc(x5, y5, x6, y6, start=arc_angle, extent=180, style='arc', outline="black", width=LINE_WIDTH),
            canvas.create_arc(x7, y7, x8, y8, start=arc_angle, extent=180, style='arc', outline="black", width=LINE_WIDTH),
            canvas.create_line(x9, y9, x10, y10, fill="black", width=LINE_WIDTH)
        ]

        self.canvas_elements_memory(lines)

    def draw_capacitor(self, canvas, pmain, offset_center, offset_final, orientation, scale):
        

        #-----------------------------------------offset center feature-----------------------------------------
        FINAL_OFFSET_CAPACITOR_DEFAULT = 100
        SCALE_CAPACITOR_DEFAULT = 10

        if offset_final =="":
            offset_final = FINAL_OFFSET_CAPACITOR_DEFAULT
        if scale == "":
            scale = SCALE_CAPACITOR_DEFAULT

        if offset_center == "" or int(offset_center) == 0:
            offset_center_var = int(offset_final) * 0.5
            offset_final_var = int(offset_final) * 0.5
        else:
            offset_center_var = int(offset_center)
            offset_final_var = int(offset_final)

        #-------------------------------------------points definition-----------------------------------------


        p_start = pmain
        p_ref_center = [p_start[0] + offset_center_var, p_start[1]]  # center of rectangle
        p_ref_end = [p_start[0] + offset_final_var + offset_center_var, p_start[1]]

        MIN_WIDTH_CAPACITOR = 10

        if scale == "":
            width_capacitor = MIN_WIDTH_CAPACITOR
        else:
            width_capacitor = int(scale)

        if width_capacitor * 1.5 >= 0.9 *abs(p_ref_center[0] - p_start[0]) or width_capacitor * 1.5 >= 0.9 * abs(p_ref_center[0] - p_ref_end[0]):
            if abs(p_ref_center[0] - p_start[0]) > abs(p_ref_center[0] - p_ref_end[0]):
                width_capacitor = abs(p_ref_center[0] - p_ref_end[0]) * 0.9 * (2/3)   
            else:
                width_capacitor = abs(p_ref_center[0] - p_start[0]) * 0.9 * (2/3)

            print("-----------------------------------------maximum size reached, check scale-----------------------------------------")

        height_capacitor = width_capacitor * 4
        #-------------------------------------------points definition-----------------------------------------

        p_ref_start_fig = [p_ref_center[0] - width_capacitor * 0.5, p_start[1]]
        p_ref_line_1_start = [p_ref_center[0] - width_capacitor * 0.5, p_ref_center[1] - height_capacitor * 0.5]
        p_ref_line_1_end = [p_ref_center[0] - width_capacitor * 0.5, p_ref_center[1] + height_capacitor * 0.5]
        p_ref_line_2_start = [p_ref_center[0] + width_capacitor * 0.5, p_ref_center[1] - height_capacitor * 0.5]
        p_ref_line_2_end = [p_ref_center[0] + width_capacitor * 0.5, p_ref_center[1] + height_capacitor * 0.5]
        p_ref_end_fig = [p_ref_center[0] + width_capacitor * 0.5, p_ref_end[1]]


        match orientation:
            case "N":
                ANGLE = 270
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_line_1_start = self.rotate_point(p_start, p_ref_line_1_start, ANGLE)
                p_line_1_end = self.rotate_point(p_start, p_ref_line_1_end, ANGLE)
                p_line_2_start = self.rotate_point(p_start, p_ref_line_2_start, ANGLE)
                p_line_2_end = self.rotate_point(p_start, p_ref_line_2_end, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)
            case "S":
                ANGLE = 90
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_line_1_start = self.rotate_point(p_start, p_ref_line_1_start, ANGLE)
                p_line_1_end = self.rotate_point(p_start, p_ref_line_1_end, ANGLE)
                p_line_2_start = self.rotate_point(p_start, p_ref_line_2_start, ANGLE)
                p_line_2_end = self.rotate_point(p_start, p_ref_line_2_end, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)
            case "E":
                ANGLE = 0
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_line_1_start = self.rotate_point(p_start, p_ref_line_1_start, ANGLE)
                p_line_1_end = self.rotate_point(p_start, p_ref_line_1_end, ANGLE)
                p_line_2_start = self.rotate_point(p_start, p_ref_line_2_start, ANGLE)
                p_line_2_end = self.rotate_point(p_start, p_ref_line_2_end, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)
            case "W":
                ANGLE = 180
                p_start_fig = self.rotate_point(p_start, p_ref_start_fig, ANGLE)
                p_line_1_start = self.rotate_point(p_start, p_ref_line_1_start, ANGLE)
                p_line_1_end = self.rotate_point(p_start, p_ref_line_1_end, ANGLE)
                p_line_2_start = self.rotate_point(p_start, p_ref_line_2_start, ANGLE)
                p_line_2_end = self.rotate_point(p_start, p_ref_line_2_end, ANGLE)
                p_end_fig = self.rotate_point(p_start, p_ref_end_fig, ANGLE)
                p_end = self.rotate_point(p_start, p_ref_end, ANGLE)

        self.created_dots.append(p_end)

        x1, y1 = p_start
        x2, y2 = p_start_fig
        x3, y3 = p_line_1_start
        x4, y4 = p_line_1_end
        x5, y5 = p_line_2_start
        x6, y6 = p_line_2_end
        x7, y7 = p_end_fig
        x8, y8 = p_end

        lines = [
            canvas.create_line(x1, y1, x2, y2, fill="black", width=LINE_WIDTH),
            canvas.create_line(x3, y3, x4, y4, fill="black", width=LINE_WIDTH),
            canvas.create_line(x5, y5, x6, y6, fill="black", width=LINE_WIDTH),
            canvas.create_line(x7, y7, x8, y8, fill="black", width=LINE_WIDTH)
        ]

        self.canvas_elements_memory(lines)

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
    
    def delete_selected(self, id):
        if id:
            self.canvas.delete(id)

    def delete_group_selected(self, id):
        print("self.id_elements_deleted: ", self.id_elements_deleted)
        print(f"id: {id}")
        print(f"canvas.elements: {self.canvas.elements}")
        print(f"self.canvas_memory_asignation: {self.canvas_memory_asignation}")
        id_group=None
        if id:

            id_group = self.get_id_group(id)
                
            print(f"id_group: {id_group}")
            
            #self.id_elements_deleted.append(id_group)

            for i in range(len(self.canvas_memory_asignation)):
                
                if id_group == self.canvas_memory_asignation[i][0]:
                        print(f"self.canvas_memory_asignation[i][1]: {self.canvas_memory_asignation[i][1]}")
                        self.delete_selected(self.canvas_memory_asignation[i][1])

        print(f"self.canvas_memory_asignation: {self.canvas_memory_asignation}")
        print(f"canvas.elements: {self.canvas.elements}")

        print("self.id_elements_deleted: ", self.id_elements_deleted)

        
        print("------------------self.id_elements_deleted: ---------------------", self.id_elements_deleted)

        self.delete_log_entry(id_group)

    def get_id_group(self, id):
        for i in range(len(self.canvas_memory_asignation)):
            if id == self.canvas_memory_asignation[i][1]:
                return self.canvas_memory_asignation[i][0]

    def delete_log_entry(self, id_group):
        if self.log:
            for i in range(len(self.log)):
                print(f"self.log[{i}][1]: ", self.log[i])
                if self.log[i][1] == id_group:
                    self.id_elements_deleted.append(self.log[i][1])
                    # del self.log[i]
            i_aux = 0
            for i in range(len(self.id_elements_deleted)):
                for i2 in range(len(self.log)):
                    if self.id_elements_deleted[i] == self.log[i2 - i_aux][1]:
                        del self.log[i2 - i_aux]
                        i_aux += 1

    def canvas_elements_memory(self, drawing_elements):

        if self.canvas.elements:
            id_start = self.canvas.elements[-1]+1
        else:
            id_start = 1

        print(f"canvas.elements: {self.canvas.elements}")
        print(f"id_start: {id_start}")

        self.canvas.elements.extend(drawing_elements)

        self.id_element_created = id_start
        
        for i in range(len(drawing_elements)):
            self.canvas_memory_asignation.append([id_start,id_start+i])
        
        print(f"self.canvas_memory_asignation: {self.canvas_memory_asignation}")

    def remove_id(self, id):
        self.canvas.delete(id) 
        if id in self.canvas.elements:
            self.canvas.elements.remove(id)
    
    def draw_text(self, canvas, p1, text, scale):
        
        if text == "":
            text_var = "text"
        else:
            text_var = text

        if scale == "":
            scale_var = 12
        else:
            scale_var = int(scale)
        
        x1, y1 = p1
        text_id = canvas.create_text(x1, y1, text=text_var, font=(FONT_FAMILY, scale_var), fill="black")
        self.canvas_elements_memory([text_id])

if __name__ == "__main__":
    root = ctk.CTk()
    app = CanvasApp(root)
    root.mainloop()
