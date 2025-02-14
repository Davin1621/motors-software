from customtkinter import CTkLabel, CTkButton, CTkCanvas, CTkToplevel, CTkFrame, CTkComboBox, CTkCheckBox, CTkScrollbar
from numpy import max as max_np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import sin
from customtkinter import filedialog, CTkInputDialog
from itertools import zip_longest
import math

import matplotlib.pyplot as plt
import random
import csv

from numba import njit

#from styles import a*

# -----------------------------------------------------------------Graphs colors---------------------------------------------------------------

PLOT_LINE_COLORS = ['deepskyblue', 'lime', 'magenta']
CURSOR_TEXT_COLOR = 'white'
CURSOR_TEXT_BACKGROUND_COLOR = 'black'
BACKGROUND_STYLE = 'dark_background'
GRID_COLOR = 'blue'
FIGURE_BACKGROUND_COLOR = "#333333"
AXES_BACKGROUND_COLOR = 'black'
SPINES_COLOR = 'deepskyblue'

# -----------------------------------------------------------------Varius vars---------------------------------------------------------------

FONT_FAMILY = "font"
FONT_SIZE_TITLE = 15
FONT_SIZE_LABEL = 12
PADDING = 4

#-----------------------------------------------------FRAME INFO----------------------------------------------

def frame_info1( frames_array):
        frame_visible=True
        frame_memory=frames_array.grid_info()
        frame_row=frame_memory['row']
       
        frame_info=[]
        frame_info.append(frame_visible)  #[0]
        frame_info.append(frame_row)     #[1]

        return frame_info

def frame_info_batch( frames_array):

        all_frames_info=[]

        for i in range(len(frames_array)):

            frame_info=frame_info1(frames_array[i])

            all_frames_info.append(frame_info)

        return all_frames_info

def frame_info_main( frame_main):

        frame_main_total_rows=frame_main.grid_size()[1]

        frame_main_rows_visible=[]

        for i in range(frame_main_total_rows):
            frame_main_rows_visible.append(True)

        return frame_main_rows_visible

#---------------------------------------------SCROLLVAR MENU--------------------------------------------

def items_creation_location( container,i,label):
    frame = CTkFrame(container) 
    frame.grid(row=i, column=0, sticky="nsew", padx=PADDING, pady=PADDING)

    checkbox = CTkCheckBox(frame, text=label)
    checkbox.grid(row=i, column=0, sticky="nw", padx=PADDING, pady=PADDING)

    return frame,checkbox

def logic_filter_and( output_array, condition_1, array_2, condition_2):

    for i in range(len(output_array)):
        if output_array[i]==condition_1 and array_2[i]==condition_2:
            output_array[i]=True #filter_output[i] is already true because of the condition
        else:
            output_array[i]=False

def list_unique_values_dropdowns(array_values,id):

    array_options_filter1=[]
  
    array_options_filter1.append("(no selection)")
 
    for i in range(len(array_values)):

        array_options_filter1.append(array_values[i][id])

    array_uniques= sorted(list(set(array_options_filter1)))

    return array_uniques

def checkbox_toggle( frame_info, containers_twins_array, main_container, datos_main_rows):
        
    visible = not frame_info[0]
    frame_sub_row=frame_info[1]
    frame_main_total_rows=main_container.grid_size()[1]
    main_frame=main_container
    frames_siblings=containers_twins_array

    if visible:

        frames_siblings[frame_sub_row].grid_remove()

        for i in range(frame_main_total_rows):

            if i==frame_sub_row:
                main_frame.grid_rowconfigure(i, weight=0)
                datos_main_rows[i]=False
            else:
                if datos_main_rows[i]==True:
                    main_frame.grid_rowconfigure(i, weight=1)
                else:
                    main_frame.grid_rowconfigure(i, weight=0)                                              
    else:
            
        datos_main_rows[frame_sub_row] = True

        frames_siblings[frame_sub_row].grid(row=frame_sub_row, column=0, sticky="nsew", padx=PADDING, pady=PADDING)

        main_frame.grid_rowconfigure(frame_sub_row, weight=1)
                        
    frame_info[0] = visible

def create_array( length):

        array_to_filter=[]
        for i in range(length):

            array_to_filter.append(False)
        
        return array_to_filter

def arrays_options_filters(array_to_filter, array_checkboxes_selected, value1, value2, value_checkboxes_selected):
        
    filter_output=create_array(len(array_to_filter))

    filtered_values_dropdowns=[]

    filtered_values_dropdowns.append(value1)
    filtered_values_dropdowns.append(value2)

    Aux_arrays=[]   

    Aux_arrays_id_excluded=[]
    Aux_arrays_id_selected=[]   

    #---------------------------------------------------------creation of aux arrays-----------------------------------------------------

    for ivalues in range(len(filtered_values_dropdowns)):

        Aux_arrays.append(create_array(len(array_to_filter)))  #creates arrays the size of the items arrays for each filter

        if filtered_values_dropdowns[ivalues]=="(no selection)":    #adds a term to the array if it is equal to "(no selection)"

            Aux_arrays_id_excluded.append(ivalues)
        else:

            Aux_arrays_id_selected.append(ivalues)

    #---------------------------------------------------------load values to aux arrays-----------------------------------------------------      

    if len(Aux_arrays_id_excluded)==len(Aux_arrays):    #if none is selected, show all

        for i in range(len(array_to_filter)):   #loop of items to set all to TRUE

            filter_output[i]=True
    else:
        for i in range(len(array_to_filter)):   #LOOP OF ITEMS
                
            for ivalues in range(len(filtered_values_dropdowns)):   #LOOP OF FILTERS

                if ivalues not in Aux_arrays_id_excluded:   #if it is not one the excluded

                    if array_to_filter[i][ivalues]==filtered_values_dropdowns[ivalues]:   #if the values are equal to the filter TRUE

                        Aux_arrays[ivalues][i]=True

                    else:   #if it is not equal then FALSE

                        Aux_arrays[ivalues][i]=False

    #---------------------------------------------------------filters output-----------------------------------------------------

    if len(Aux_arrays_id_selected)==1:      #if there is only one filter selected

        filter_output=Aux_arrays[Aux_arrays_id_selected[0]]

    if len(Aux_arrays_id_selected)>1:       #if there are at least 2 filters selected

        for i_array in range(len(Aux_arrays)):  #loop for each filter   
        
            if i_array==0:

                filter_output=Aux_arrays[Aux_arrays_id_selected[0]] #only for the first cicly does not matter filter_output state

            else:
                logic_filter_and(filter_output, True, Aux_arrays[i_array], True)

    #---------------------------------------------------------selected boxes logic last filter-----------------------------------------------------

    if value_checkboxes_selected!="(no selection)":
        match value_checkboxes_selected:
            case "Selected":
                logic_filter_and(filter_output, True, array_checkboxes_selected, True)
            
            case "Not Selected":

                logic_filter_and(filter_output, True, array_checkboxes_selected, False)

    return filter_output  

def filter_options(array_to_filters, array_checkboxes_selected, VALUE_1_selected, VALUE_2_selected, VALUE_checkboxes_selected):
        
    #Returns an array of the id items to hide according to the filters

    filter1_selected= VALUE_1_selected
    filter1_id_selected=0

    filter2_selected= VALUE_2_selected
    filter2_id_selected=0

    unique_values_filter_1= list_unique_values_dropdowns(array_to_filters,0)
    unique_values_filter_2= list_unique_values_dropdowns(array_to_filters,1)

    for i in range(len(unique_values_filter_1)):

        if unique_values_filter_1[i]==filter1_selected:
                
            filter1_id_selected=i

    for i in range(len(unique_values_filter_2)):

        if unique_values_filter_2[i]==filter2_selected:
                
            filter2_id_selected=i

    filter_final=arrays_options_filters(array_to_filters, array_checkboxes_selected,unique_values_filter_1[filter1_id_selected],unique_values_filter_2[filter2_id_selected], VALUE_checkboxes_selected)

    return filter_final

def round_down_to_nearest_power_of_ten(number):
    if number == 0:
        return 0
    exponent = int(math.log10(number))
    factor = 10 ** exponent
    return (number // factor) * factor

#------------------------------------------------------------graph-----------------------------------------------

def canvas_plot(fig, frame_container):
        
        canvas = FigureCanvasTkAgg(fig, master=frame_container)
        canvas.draw()   

        canvas_widget = canvas.get_tk_widget()
        canvas_widget.grid(row=0, column=0, sticky="nsew")
        canvas_widget.configure(highlightthickness=0)  # Set highlight thickness to 0

        frame_container.grid_rowconfigure(0, weight=1)
        frame_container.grid_columnconfigure(0, weight=1)

def graphs_ax(ax, fig, x_label, y_label):

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        ax.grid(True)
        ax.grid(True, color=GRID_COLOR, linestyle='--')  # Líneas discontinuas azules

        fig.patch.set_facecolor(FIGURE_BACKGROUND_COLOR)  # Fondo negro para la figura
        ax.set_facecolor(AXES_BACKGROUND_COLOR)  # Fondo negro para los ejes

        ax.spines['top'].set_color(SPINES_COLOR)  # Bordes superiores en azul brillante
        ax.spines['right'].set_color(SPINES_COLOR)  # Bordes derechos en azul brillante
        ax.spines['left'].set_color(SPINES_COLOR)  # Bordes izquierdos en azul brillante
        ax.spines['bottom'].set_color(SPINES_COLOR)  # Bordes inferiores en azul brillante
        
def graphs_fig(Graph_frame):

    frame_width = Graph_frame.winfo_width() or 400  # Usa un valor por defecto si no está inicializado
    frame_height = Graph_frame.winfo_height() or 300

    fig = Figure(figsize=(frame_width / 100, frame_height / 100))  # Ajusta el divisor para un tamaño apropiado
    fig.subplots_adjust(bottom=0.25)

    return fig

def space_x_values(limit_min, limit_max, length):

        x_values=[limit_min + i*((limit_max - limit_min) / (length - 1)) for i in range(length)]

        return x_values

@njit
def space_x_values_log(limit_min, f_main, length):

        x_values=[limit_min + f_main * i for i in range(length)]

        return x_values

def labels_x_axis(ax, values_selected, array_values):
        
        x_values_1=[]
        x_values_2=[]
        decimal_places=0

        for i in range(len(values_selected)):
            x_values_1.append(array_values[values_selected[i]-1])

        for i in range(len(values_selected)):
            x_values_2.append(f'{array_values[values_selected[i]-1]:.{decimal_places}f}')

        ax.set_xticks(x_values_1)
        ax.set_xticklabels(x_values_2)

def check_reorder_xy_data(array):
        x_values = [item[0] for item in array]
        y_values = [item[1] for item in array]
        return [x_values, y_values]
    
def max_value_lim(serie,option_value):
    if option_value == "max":
        # Si el primer elemento es una lista o tupla, es una lista de listas
        if isinstance(serie[0], (list, tuple)):
            var_lim_max_result = round(max(max(sublist) for sublist in serie), 2)

        # Si no, es una lista simple
        else:
            var_lim_max_result = round(max(serie), 2)
    else:
        var_lim_max_result = float(option_value)
    
    return var_lim_max_result

def min_value_lim(serie, option_value):
    if option_value == "min":
        # Si el primer elemento es una lista o tupla, es una lista de listas
        if isinstance(serie[0], (list, tuple)):
            var_lim_min_result = round(min(min(sublist) for sublist in serie), 2)
        # Si no, es una lista simple
        else:
            var_lim_min_result = round(min(serie), 2)
    else:
        var_lim_min_result = float(option_value)
    
    return var_lim_min_result

#------------------------------------------------- dataset ----------------------------------------------

def bar_function(values, pick):
        array=[]

        if pick==0:
            aux_pick=0.5
        else:
            aux_pick=pick

        serie_x_data = [i for i in range(values)]  # valores enteros de 0 a 'values'
        serie_y_data = [aux_pick+i for i in serie_x_data]  # valores y como múltiplos de 'aux_pick'

        array.append(serie_x_data)
        array.append(serie_y_data)

        return serie_y_data
    
def inital_plot_function(values):
    array=[]

    serie_x_data = [i for i in range(values)]
    serie_y_data = [0 for i in serie_x_data]

    array.append(serie_x_data)
    array.append(serie_y_data)

    return serie_y_data

#------------------------------------------------- Create Components ----------------------------------------------

def Create_components_left( frame, label, button):

    #Array_frame1=CTkFrame(frame)
    #Array_label1=CTkLabel(Array_frame1, text=label, font=(FONT_FAMILY, FONT_SIZE_LABEL))
    Array_but1=CTkButton(frame, text=button, width=200)

    Array1 = []
    #Array1.append((Array_frame1, Array_label1, Array_but1))
    Array1.append(Array_but1)
    return Array1
        
def Create_components_left_dropdown(frame, label, button, options):

    Array_frame1=CTkFrame(frame)
    Array_label1=CTkLabel(Array_frame1, text=label, font=(FONT_FAMILY, FONT_SIZE_LABEL))
    Array_drop1=CTkComboBox(Array_frame1, values=options)

    Array1 = []
    Array1.append((Array_frame1, Array_label1, Array_drop1))
    return Array1
    
def Create_components_left_2(frame_main):

    frame_sub1=CTkFrame(frame_main)
    frame_sub2=CTkFrame(frame_main, height=200)
    frame_sub3=CTkFrame(frame_main)

    #frame_sub1.configure(fg_color="#ffa500")  # Orange color
    #frame_sub2.configure(fg_color="#ffa500")  # Orange color
    #frame_sub3.configure(fg_color="#ffa500")  # Orange color

    #frame_sub2.pack_propagate(False)  # Add propagate false to frame_sub2

    Array1 = []
    Array1.append((frame_sub1, frame_sub2, frame_sub3))
    return Array1

def Create_components_right(frame, buttons_quantity, buttons_caption, labels_quantity, labels_captions):

    #Array_frame1=CTkFrame(frame, width=frame.winfo_width())
    Array_frame1=CTkFrame(frame)
    Array_frame2=CTkFrame(Array_frame1)
    Array_frame3=CTkFrame(Array_frame1)

    width_items=300

    labels_number=labels_quantity
    labels=[]

    for i in range(labels_number):
        labels.append(CTkLabel(Array_frame3, width=width_items, height=width_items, text=labels_captions[i]))

    buttons1=buttons_quantity
    buttons=[]

    for i in range(buttons1):
        buttons.append(CTkButton(Array_frame3, width=width_items, height=width_items, text=buttons_caption[i]))

    #Array_frame2.configure(fg_color="#00ff00")  # Green color

    Array1 = []
    Array1.append((Array_frame1, Array_frame2, Array_frame3, buttons, labels))
    return Array1
    
def Create_components_main(frame):

    #Array_frame1=CTkFrame(frame, width=frame.winfo_width())
    Array_frame1=CTkFrame(frame)
    Array_frame2=CTkFrame(Array_frame1)
    Array_frame3=CTkFrame(Array_frame1)

    #Array_frame2.configure(fg_color="#00ff00")  # Green color

    Array1 = []
    Array1.append((Array_frame1, Array_frame2, Array_frame3))
    return Array1

#------------------------------------------------- Screen location frames ----------------------------------------------

def Locate_frames_left(Datos):

    Datos[0].pack(side="top", fill="both", expand=True, padx=PADDING, pady=PADDING) 
    Datos[1].pack(side="left", fill="x", expand=True, padx=PADDING, pady=PADDING)
    Datos[2].pack(side="left", fill="x", expand=True, padx=PADDING, pady=PADDING)

def Locate_frames_left_2(Datos):

    Datos[0].grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
    Datos[1].grid(row=1, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
    Datos[2].grid(row=2, column=0, sticky="nsew", padx=PADDING, pady=PADDING)

    Datos[0].grid_rowconfigure(0, weight=1)
    Datos[0].grid_rowconfigure(1, weight=1)
    Datos[0].grid_rowconfigure(2, weight=1)
    Datos[0].grid_columnconfigure(0, weight=0)

    Datos[1].grid_rowconfigure(0, weight=1)
    Datos[1].grid_columnconfigure(0, weight=1, minsize=0)
    Datos[1].grid_columnconfigure(1, weight=0)

    Datos[2].grid_rowconfigure(0, weight=1)
    Datos[2].grid_rowconfigure(1, weight=1)
    Datos[2].grid_rowconfigure(2, weight=1)
    Datos[2].grid_columnconfigure(0, weight=1)

def Locate_frames_left_3(Datos):

    Datos.pack(side="top", fill="both", expand=True, padx=PADDING, pady=PADDING) 

def Locate_frames_main(Datos):
        
    Datos[0].grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
    Datos[1].grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
    Datos[2].grid(row=0, column=1, sticky="nsew", padx=PADDING, pady=PADDING)

    Datos[0].grid_rowconfigure(0, weight=1)
    Datos[0].grid_columnconfigure(0, weight=0)
    Datos[0].grid_columnconfigure(1, weight=1)

    Datos[1].grid_rowconfigure(0, weight=1)
    Datos[1].grid_rowconfigure(1, weight=8)
    Datos[1].grid_rowconfigure(2, weight=1)
    Datos[1].grid_columnconfigure(0, weight=0)


    Datos[2].grid_rowconfigure(0, weight=1)
    Datos[2].grid_rowconfigure(1, weight=1)
    Datos[2].grid_rowconfigure(2, weight=1)
    Datos[2].grid_rowconfigure(3, weight=1)
    Datos[2].grid_columnconfigure(0, weight=1)
    #Datos[2].grid_columnconfigure(1, weight=1)

class graphics_window():

    def __init__(self, model_tab1):

        self.plot_containers = {}  # Diccionario para guardar los contenedores de gráficos
        self.figures = {}         # Diccionario para guardar las figuras
        #---------------------------- Frames principales -------------------------------------------------------

        model_tab1.grid_rowconfigure(0, weight=1)
        model_tab1.grid_columnconfigure(0, weight=1)

        main_components=Create_components_main(model_tab1)

        self.main_components=main_components

        self.right_frame_freeze = main_components[0][2]
        self.left_frame_freeze = main_components[0][1]

        Locate_frames_main(main_components[0])

        ltabs=Create_components_left_2(main_components[0][1])

        #---------------------------- DATASETS -------------------------------------------------------

        self.f_main = 300
        
        self.datasets = self.datasets_definition()

        #---------------------------- Dropdowns lists options -------------------------------------------------------

        dropdown_options_1 = list_unique_values_dropdowns(self.datasets[1],0)   #dropdown options 1
        dropdown_options_2 = list_unique_values_dropdowns(self.datasets[1],1)   #dropdown options 2

        #---------------------------- Title items -------------------------------------------------------
        top_frame = CTkFrame(ltabs[0][0])
        top_frame.pack(side="top", fill="both", expand=True, padx=PADDING, pady=PADDING)
        Litemstab = CTkLabel(top_frame, text="Filters", font=(FONT_FAMILY, FONT_SIZE_TITLE, "bold", "underline"))
        Litemstab.pack(side="left", fill="both", expand=True, padx=PADDING, pady=PADDING)
        clear_items_button = CTkButton(top_frame, text="Clear Filters")
        clear_items_button.pack(side="right", fill="both", expand=True, padx=PADDING, pady=PADDING)

        #---------------------------- components left-right -------------------------------------------------------

        Litems1 = Create_components_left_dropdown(ltabs[0][0], "Type:", "Time Domain: fundamental cycle", dropdown_options_1)
        Litems2 = Create_components_left_dropdown(ltabs[0][0], "Domain:", "Time Domain: 1 switching cycle", dropdown_options_2)
        Litems3 = Create_components_left_dropdown(ltabs[0][0], "Selection:", "Frecuency Domain", ["(no selection)","Selected","Not Selected"])
        Litems4 = Create_components_left(ltabs[0][2], "", "Program aciton")
        Litems5 = Create_components_left(ltabs[0][2], "", "Export all to CSV")
        Litems6 = Create_components_left(ltabs[0][2], "", "Export all to python")

        Litems=[]
        Litems.append(Litems1[0])
        Litems.append(Litems2[0])
        Litems.append(Litems3[0])
        Litems.append(Litems4[0])
        Litems.append(Litems5[0])
        Litems.append(Litems6[0])

        Ritems1 = Create_components_right(main_components[0][2],3,["Go Up","Go down","domain"],3,["A","B","C"])
        Ritems2 = Create_components_right(main_components[0][2],3,["Go Up","Go down","domain"],3,["A","B","C"])
        Ritems3 = Create_components_right(main_components[0][2],3,["Go Up","Go down","domain"],3,["A","B","C"])
        Ritems4 = Create_components_right(main_components[0][2],3,["Go Up","Go down","domain"],3,["A","B","C"])

        Ritems=[]
        Ritems.append(Ritems1[0])
        Ritems.append(Ritems2[0])
        Ritems.append(Ritems3[0])
        Ritems.append(Ritems4[0])

        #---------------------------- Location for tabs -------------------------------------------------------

        Locate_frames_left_2(ltabs[0])
        
        Locate_frames_left(Litems[0])
        Locate_frames_left(Litems[1])
        Locate_frames_left(Litems[2])
        #Locate_frames_left_3(Litems[3])
        Locate_frames_left_3(Litems[4])
        Locate_frames_left_3(Litems[5])

        self.Locate_frames_right(Ritems[0], 0, 1, [self.datasets[2][0]])
        self.Locate_frames_right(Ritems[1], 1, 1, "none")
        self.Locate_frames_right(Ritems[2], 2, 1, "none")
        self.Locate_frames_right(Ritems[3], 3, 1, "none")
        
        #---------------------------- scrollbar menu -------------------------------------------------------

        canvas_scroll_frame = self.scrollbar_function(ltabs[0][1])  #canvas for scrollbar menu
        items_frames=self.scrollbar_items(canvas_scroll_frame[0], self.datasets, Ritems) #all items in scrollbar menu
        canvas_scroll_frame[1].configure(width=items_frames[0]+2*PADDING)   #size of canvas for scrollbar menu
        item_main_info=frame_info_main(canvas_scroll_frame[0]) #info function for main container         
        all_frames_info=frame_info_batch(items_frames[2])  #info for all frames

        #------------------------------Actions dropdowns---------------------------------------------------

        
        Dropdowns_memory_values=["","",""]
 
        clear_items_button.configure(command=lambda:  self.checkbox_filter_all_clear(Litems, Dropdowns_memory_values,all_frames_info,items_frames[2],canvas_scroll_frame[0],item_main_info,self.datasets[1]))

        Litems1[0][2].configure(command=lambda value1: self.checkbox_filter_all(value1,0, Dropdowns_memory_values,items_frames[1],all_frames_info,items_frames[2],canvas_scroll_frame[0],item_main_info,self.datasets[1]))
        Litems2[0][2].configure(command=lambda value1: self.checkbox_filter_all(value1,1, Dropdowns_memory_values,items_frames[1],all_frames_info,items_frames[2],canvas_scroll_frame[0],item_main_info,self.datasets[1]))
        Litems3[0][2].configure(command=lambda value1: self.checkbox_filter_all(value1,2, Dropdowns_memory_values,items_frames[1],all_frames_info,items_frames[2],canvas_scroll_frame[0],item_main_info,self.datasets[1]))



        #---------------------------- buttons -------------------------------------------------------
        
        self.order_frames_datasets=["none","none","none","none"]
        
        Litems[3].configure(command=lambda: self.switch_frame(self.datasets,Ritems,0,1))
        Litems[4].configure(command=lambda: self.export_to_csv(self.datasets[0],self.datasets[2]))
        Litems[5].configure(command=lambda: self.export_to_py(self.datasets[0],self.datasets[2]))

        #-------------------------------------------------buttons right frame-----------------------
        vars_domains=[1,1,1,1]
        
        #Ritems[0][3][0].configure(state="disable", fg_color="grey", text_color="black")
        Ritems[0][3][1].configure(command=lambda: self.switch_frame(self.datasets,Ritems,0,1))  #go down
        Ritems[0][3][2].configure(command=lambda: self.toggle_domain(vars_domains,Ritems[0][1],self.datasets[0][self.order_frames_datasets[0]],self.datasets[3][self.order_frames_datasets[0]]))
        
        Ritems[1][3][0].configure(command=lambda: self.switch_frame(self.datasets,Ritems,0,1))  #go up
        Ritems[1][3][1].configure(command=lambda: self.switch_frame(self.datasets,Ritems,1,2))  #go down
        Ritems[1][3][2].configure(command=lambda: self.toggle_domain(vars_domains,Ritems[1][1],self.datasets[0][self.order_frames_datasets[1]],self.datasets[3][self.order_frames_datasets[1]]))
        
        
        Ritems[2][3][0].configure(command=lambda: self.switch_frame(self.datasets,Ritems,1,2))  #go up
        Ritems[2][3][1].configure(command=lambda: self.switch_frame(self.datasets,Ritems,2,3))  #go down
        Ritems[2][3][2].configure(command=lambda: self.toggle_domain(vars_domains,Ritems[2][1],self.datasets[0][self.order_frames_datasets[2]],self.datasets[3][self.order_frames_datasets[2]]))
        
        
        Ritems[3][3][0].configure(command=lambda: self.switch_frame(self.datasets,Ritems,2,3))  #go up
        #Ritems[3][3][1].configure(state="disable", fg_color="grey", text_color="black")
        Ritems[3][3][2].configure(command=lambda: self.toggle_domain(vars_domains,Ritems[3][1],self.datasets[0][self.order_frames_datasets[3]],self.datasets[3][self.order_frames_datasets[3]]))
        

        #---------------------------- memories for buttons -------------------------------------------------------

        right2_info=frame_info1(Ritems[1][0])
        right3_info=frame_info1(Ritems[2][0])
        right4_info=frame_info1(Ritems[3][0])

        self.main_rows_info=frame_info_main(main_components[0][2])

        self.right2_info=right2_info
        self.right3_info=right3_info
        self.right4_info=right4_info

        self.toggle_frame_2(right2_info,Ritems,main_components[0][2],self.main_rows_info,["none"],"")
        self.toggle_frame_2(right3_info,Ritems,main_components[0][2],self.main_rows_info,["none"],"")
        self.toggle_frame_2(right4_info,Ritems,main_components[0][2],self.main_rows_info,["none"],"")

        #----------------------------------------------Initial checkbox---------------------------------------------------
        checkbox_initial=0
        items_frames[3][checkbox_initial].select() #select checkbox
        self.order_frames_datasets[0]=checkbox_initial #update checkbox order
        items_frames[1][checkbox_initial]=items_frames[3][checkbox_initial].get() #update checkbox states
        self.create_plot(Ritems[0][1],self.datasets[0][checkbox_initial],self.datasets[3][checkbox_initial]) #creates plot checkbox
        self.Locate_frames_right_sub(Ritems[0], len(self.datasets[2][checkbox_initial]), self.datasets[2][checkbox_initial], "unique") #update right frames

    def switch_frame(self, datasets,Ritems, first_item_index, second_item_index):
        
        self.freeze_screen_right()

        self.order_frames_datasets[first_item_index], self.order_frames_datasets[second_item_index] = self.order_frames_datasets[second_item_index], self.order_frames_datasets[first_item_index]
 
        frame_up=self.order_frames_datasets[second_item_index]
        frame_down=self.order_frames_datasets[first_item_index]

        self.create_plot(Ritems[second_item_index][1],datasets[0][frame_up],datasets[3][frame_up])
        self.create_plot(Ritems[first_item_index][1],datasets[0][frame_down],datasets[3][frame_down])

        if first_item_index==0:
            self.Locate_frames_right_sub(Ritems[first_item_index], len(datasets[2][frame_down]), datasets[2][frame_down],"first")
        else:
            self.Locate_frames_right_sub(Ritems[first_item_index], len(datasets[2][frame_down]), datasets[2][frame_down],"")

        if (self.checkbox_states_sum-1)==second_item_index:
            self.Locate_frames_right_sub(Ritems[second_item_index], len(datasets[2][frame_up]), datasets[2][frame_up],"last")
        else:
            self.Locate_frames_right_sub(Ritems[second_item_index], len(datasets[2][frame_up]), datasets[2][frame_up],"")

        self.unfreeze_screen_right()

    def toggle_frame(self, frame_sub, frame_info, all_frames, main_rows_info):
        self.freeze_screen_right()
        visible = frame_info[0]
        frame_main_row=frame_info[1] #CHECK

        if main_rows_info[frame_main_row]==True:

            if visible:

                frame_sub.grid_remove()

            else:
            
                self.Locate_frames_right(all_frames,frame_main_row)

            frame_info[0]= not visible

        self.unfreeze_screen_right()

    def toggle_frame_2(self, frame_info, containers_twins_array, main_container, datos_main_rows, dataset_info, optional_position):
        
        visible = frame_info[0]
        frame_sub_row=frame_info[1]
        frame_main_total_rows=main_container.grid_size()[1]

        if visible:
            containers_twins_array[frame_sub_row][0].grid_remove()
            for i in range(frame_main_total_rows):
                if i==frame_sub_row:
                    main_container.grid_rowconfigure(i, weight=0)
                    datos_main_rows[i]=False
                else:
                    if datos_main_rows[i]==True:
                        main_container.grid_rowconfigure(i, weight=1)
                    else:
                        main_container.grid_rowconfigure(i, weight=0)   
        else:
            datos_main_rows[frame_sub_row] = True

            containers_twins_array[frame_sub_row][0].grid(row=frame_sub_row, column=0,sticky="nsew", padx=PADDING, pady=PADDING)

            self.Locate_frames_right_sub(containers_twins_array[frame_sub_row], len(dataset_info), dataset_info, optional_position)
            
            main_container.grid_rowconfigure(frame_sub_row, weight=1)   #returns weight to 1 for the main container
                        
        frame_info[0] = not visible

        self.unfreeze_screen_right()
       
    def checkbox_filter_all(self,value, dropdown_id_value, dropdowns_values_memory, items_frames_states, all_frames_info, frames_datos, datos_main, datos_main_rows, datasets_labels):

        match dropdown_id_value:
            case 0:
                dropdowns_values_memory[0]=value #filter 1- type
            case 1:
                dropdowns_values_memory[1]=value #filter 2- Domain
            case 2:
                dropdowns_values_memory[2]=value #filter 3- selected

        self.array_to_filter= filter_options(datasets_labels, items_frames_states,dropdowns_values_memory[0], dropdowns_values_memory[1], dropdowns_values_memory[2])

        for i in range(len(self.array_to_filter)):

            all_frames_info[i][0]=self.array_to_filter[i]    #LOAD THE ARRAY TO FILER, TO THE PROPERTY OF VISIBILITY

            checkbox_toggle(all_frames_info[i],frames_datos,datos_main,datos_main_rows)

        self.scrollbar_item.yview_moveto(0)
        true_count = sum(self.array_to_filter)

        if true_count<14:
            self.toggle_scrollbar(True)
        else:
            self.toggle_scrollbar(False)


        print(true_count)
        
    def toggle_scrollbar(self, disable):
        if disable:
            self.scrollbar_item.unbind_all("<MouseWheel>")
            self.scrollbar_bar.configure(state="disabled")
        else:
            self.scrollbar_item.bind_all("<MouseWheel>", 
                lambda e: self.scrollbar_item.yview_scroll(int(-1*(e.delta/30)), "units"))
            self.scrollbar_bar.configure(state="normal")

    def checkbox_filter_all_clear(self,Litems, dropdowns_values_memory, all_frames_info, frames_datos, datos_main, datos_main_rows, datasets_labels):

        Litems[0][2].set("(no selection)")
        Litems[1][2].set("(no selection)")
        Litems[2][2].set("(no selection)")

        for i in range (len(dropdowns_values_memory)):
            dropdowns_values_memory[i]=("no selection")

        self.array_to_filter = [True] * len(datasets_labels)

        for i in range(len(self.array_to_filter)):

            all_frames_info[i][0]=self.array_to_filter[i]    #LOAD THE ARRAY TO FILER, TO THE PROPERTY OF VISIBILITY

            checkbox_toggle(all_frames_info[i],frames_datos,datos_main,datos_main_rows)
        
    #------------------------------------------------- scrollbar functions ----------------------------------------------

    def scrollbar_items(self, container, datasets, right_items):

        max_frame_width = 0
        checkbox_states = []
        checkboxes = []
        self.checkboxes_box = []
        checkbox_states_sum = []
        checkbox_visible = []

        checkbox_states_sum.append(0)
        
        for i in range(len(datasets[2])):

            checkbox = items_creation_location(container,i,datasets[4][i])

            checkbox[1].configure(command=lambda chk=checkbox[1], idx=i: self.click_checkbox(chk, idx, checkbox_states, checkbox_states_sum, datasets, right_items))
            
            checkbox_states.append(checkbox[1].get())
            checkboxes.append(checkbox[0])
            self.checkboxes_box.append(checkbox[1])
            checkbox_visible.append(True)

            checkbox[0].update_idletasks()  # Ensure the frame is updated to get the correct width
            total_width = checkbox[0].winfo_width()
            if total_width > max_frame_width:
                max_frame_width = total_width

        return max_frame_width, checkbox_states, checkboxes, self.checkboxes_box, checkbox_states_sum

    def enable_disable_checkbox(self,length, state_var):

        for i in range(length):
                if i not in self.order_frames_datasets:
                    self.checkboxes_box[i].configure(state=state_var)

    def click_checkbox(self, checkbox, index, checkbox_states, checkbox_states_sum, datasets, right_items):


        if checkbox.get():
            if sum(checkbox_states) >= 4:
                checkbox.deselect()                
                return
        else:
            if checkbox_states_sum[0] == 1:
                checkbox.select()
                return
        checkbox_states[index] = checkbox.get()
        checkbox_states_sum[0] = sum(checkbox_states)

        self.checkbox_states_sum=checkbox_states_sum[0]

        #------------------------------------array of displayed graphs--------------------------------------------------------

        if checkbox_states[index]==1:
            self.order_frames_datasets[checkbox_states_sum[0]-1]=index
        else:
            for i in range(len(self.order_frames_datasets)):
                if self.order_frames_datasets[i]==index:
                    self.order_frames_datasets[i]="none"

            if any(item == "none" for item in self.order_frames_datasets) and not all(item == "none" for item in self.order_frames_datasets):
                non_none_items = [item for item in self.order_frames_datasets if item != "none"]
                self.order_frames_datasets = non_none_items + ["none"] * (4 - len(non_none_items))

        plot_frame_1=self.order_frames_datasets[0]

        plot_frame_2=self.order_frames_datasets[1]

        plot_frame_3=self.order_frames_datasets[2]

        plot_frame_4=self.order_frames_datasets[3]

        self.freeze_screen_right()


        #------------------------------------hide show frames--------------------------------------------------------

        match checkbox_states_sum[0],checkbox_states[index]:
            case 1,1:   #show 1th plot

                self.create_plot(right_items[0][1],datasets[0][index],datasets[3][index])

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "unique")

            case 1,0:   #hide 2th 
                
                self.toggle_frame_2(self.right2_info,right_items,self.main_components[0][2],self.main_rows_info,["none"],"")

                self.create_plot(right_items[0][1],datasets[0][plot_frame_1],datasets[3][plot_frame_1])

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "unique")

            case 2,1:#show 2th frame

                self.toggle_frame_2(self.right2_info,right_items,self.main_components[0][2],self.main_rows_info,datasets[2][plot_frame_2], "last")

                self.create_plot(right_items[1][1],datasets[0][index],datasets[3][index])

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "first")

            case 2,0:   #hide 3th frame

                self.toggle_frame_2(self.right3_info,right_items,self.main_components[0][2],self.main_rows_info,["none"],"")

                self.create_plot(right_items[0][1],datasets[0][plot_frame_1],datasets[3][plot_frame_1])
                self.create_plot(right_items[1][1],datasets[0][plot_frame_2],datasets[3][plot_frame_2])

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "first")
                self.Locate_frames_right_sub(right_items[1], len(datasets[2][plot_frame_2]), datasets[2][plot_frame_2], "last")

            case 3,1:   #show 3th frame

                self.toggle_frame_2(self.right3_info,right_items,self.main_components[0][2],self.main_rows_info,datasets[2][plot_frame_3], "last")

                self.create_plot(right_items[2][1],datasets[0][index],datasets[3][index])

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "first")
                self.Locate_frames_right_sub(right_items[1], len(datasets[2][plot_frame_2]), datasets[2][plot_frame_2], "")

            case 3,0:   #hide 4th frame

                self.toggle_frame_2(self.right4_info,right_items,self.main_components[0][2],self.main_rows_info,["none"], "")

                self.create_plot(right_items[0][1],datasets[0][plot_frame_1],datasets[3][plot_frame_1])
                self.create_plot(right_items[1][1],datasets[0][plot_frame_2],datasets[3][plot_frame_2])
                self.create_plot(right_items[2][1],datasets[0][plot_frame_3],datasets[3][plot_frame_3])

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "first")
                self.Locate_frames_right_sub(right_items[1], len(datasets[2][plot_frame_2]), datasets[2][plot_frame_2], "")
                self.Locate_frames_right_sub(right_items[2], len(datasets[2][plot_frame_3]), datasets[2][plot_frame_3], "last")

                self.enable_disable_checkbox(len(checkbox_states),"normal")

            case 4,1:   #show 4th frame

                self.toggle_frame_2(self.right4_info,right_items,self.main_components[0][2],self.main_rows_info,datasets[2][plot_frame_4], "last")

                self.create_plot(right_items[3][1],datasets[0][index],datasets[3][index])

                self.enable_disable_checkbox(len(checkbox_states),"disabled")

                self.Locate_frames_right_sub(right_items[0], len(datasets[2][plot_frame_1]), datasets[2][plot_frame_1], "first")
                self.Locate_frames_right_sub(right_items[1], len(datasets[2][plot_frame_2]), datasets[2][plot_frame_2], "")
                self.Locate_frames_right_sub(right_items[2], len(datasets[2][plot_frame_3]), datasets[2][plot_frame_3], "")

    #------------------------------------------------- Locate frames ---------------------------------------

    def Locate_frames_right(self, Datos, id, labels_quantity, labels_captions):
        
        Datos[0].grid(row=id, column=0,sticky="nsew", padx=PADDING, pady=PADDING)
        Datos[1].grid(row=0, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
        Datos[2].grid(row=0, column=1, sticky="ns", padx=PADDING, pady=PADDING)

        Datos[0].grid_rowconfigure(0, weight=1)
        Datos[0].grid_columnconfigure(0, weight=1)
        Datos[0].grid_columnconfigure(1, weight=0)

        Datos[1].grid_rowconfigure(0, weight=1)
        Datos[1].grid_columnconfigure(0, weight=1)

        #Datos[2].grid_rowconfigure(0, weight=0)
        Datos[2].grid_columnconfigure(0, weight=0)

        Datos[0].grid_propagate(False)

        if labels_captions!="none":

            self.Locate_frames_right_sub(Datos, labels_quantity, labels_captions, "")

    def Locate_frames_right_sub(self, Datos, labels_quantity, labels_captions, position_optional):

        #-----------------buttons and labels------------------------

        labels_quantity_var=labels_quantity

        for i in range(len(Datos[3])+len(Datos[4])):

            Datos[2].grid_rowconfigure(i, weight=1)

            if i<len(Datos[4]): #labels

                if labels_quantity_var>=i+1:
                    Datos[4][i].grid(row=i, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
                    Datos[4][i].configure(text=labels_captions[i], fg_color="black", corner_radius=5, text_color=PLOT_LINE_COLORS[i])
                    
            else: #buttons

                Datos[3][i-len(Datos[4])].grid(row=i, column=0, sticky="nsew", padx=PADDING, pady=PADDING)
                match i - len(Datos[4]):
                    case 0: #go up
                        if position_optional=="first" or position_optional=="unique":
                            Datos[2].grid_rowconfigure(i, weight=0)
                            Datos[3][i-len(Datos[4])].grid_remove()
                    case 1: #go down
                        if position_optional=="last" or position_optional=="unique":
                            Datos[2].grid_rowconfigure(i, weight=0)
                            Datos[3][i-len(Datos[4])].grid_remove()
                    case 2: #domain
                        Datos[3][i-len(Datos[4])].configure(state="normal")
                    case _:
                        Datos[3][i-len(Datos[4])].configure(state="normal")
        #---------------------------erase the rest of labels if it is not the maximum----------------------

        if len(Datos[4])>labels_quantity:

            for i in range(len(Datos[4])):
                if i>(labels_quantity-1):
                    
                    Datos[2].grid_rowconfigure(i, weight=0)
                    Datos[4][i].grid_remove()

        #self.unfreeze_screen_right()
        
    #------------------------------------------------- Screen freeze functions ---------------------------------------

    def freeze_screen_right(self):
        """Congelar la pantalla temporalmente."""
        self.right_frame_freeze.grid_remove()  # Ocultar el contenedor principal
        self.right_frame_freeze.update_idletasks()  # Procesar tareas pendientes
      
    def unfreeze_screen_right(self):
        self.right_frame_freeze.grid() 
        self.right_frame_freeze.update_idletasks()  

    def freeze_screen_left(self):
        """Congelar la pantalla temporalmente."""
        self.left_frame_freeze.grid_remove()  # Ocultar el contenedor principal
        self.left_frame_freeze.update_idletasks()  # Procesar tareas pendientes

    def unfreeze_screen_left(self):
        """Reactivar la pantalla después de los comandos."""
        self.left_frame_freeze.grid()  # Volver a mostrar el contenedor
        self.left_frame_freeze.update_idletasks()  # Actualizar la interfaz gráfica
    
    #------------------------------------------------- Datasets functions --------------------------------------------

    def datasets_definition(self):
        datasets_graphs_settings=[]
        datasets_filters=[]
        datasets_captions=[]
        datasets_values=[]
        datasets_names=[]

        datasets_captions.append(["Current Phase Load U"])
        datasets_captions.append(["Current Phase Load V"])
        datasets_captions.append(["Current Phase Load W"])
        datasets_captions.append(["Current Line U"])                  #1
        datasets_captions.append(["Current Line V"])                  #2
        datasets_captions.append(["Current Line W"])                  #3
        datasets_captions.append(["Current DC Bus"])                  #4
        datasets_captions.append(["Current DC Capacitor"])                  #5
        datasets_captions.append(["Current DC Load"])                  #6
        datasets_captions.append(["Current Switch U"])                  #7
        datasets_captions.append(["Current Diode MOSFET U"])                  #5
        datasets_captions.append(["Current MOSFET Channel U"])                  #6
        datasets_captions.append(["Current Switch UN"])                  #7
        datasets_captions.append(["Current Diode MOSFET UN"])                  #8
        datasets_captions.append(["Current MOSFET Channel UN"])                  #9
        datasets_captions.append(["Current Gate U"])                  #10
        datasets_captions.append(["Current Gate UN"])                  #11
        datasets_captions.append(["Current Filter Capacitor"])                  #12
        datasets_captions.append(["Current Snubber Capacitor U"])                  #13
        datasets_captions.append(["Current Snubber Capacitor UN"])                  #14
        datasets_captions.append(["Current DC Ceramic Capacitor"])                  #15

        datasets_captions.append(["Voltage DC Input"])                  #15
        datasets_captions.append(["Voltage DC Capacitor"])                  #16
        datasets_captions.append(["Voltage Line UV"])                  #17
        datasets_captions.append(["Voltage Line VW"])                  #18
        datasets_captions.append(["Voltage Line WU"])                  #19
        datasets_captions.append(["Voltage Phase Load U"])                  #20
        datasets_captions.append(["Voltage Phase Load V"])                  #21
        datasets_captions.append(["Voltage Phase Load W"])                  #22
        datasets_captions.append(["Voltage Line Load UV"])                  #23
        datasets_captions.append(["Voltage Line Load VW"])                  #24
        datasets_captions.append(["Voltage Line Load WU"])                  #25
        datasets_captions.append(["Voltage Switch U"])                  #26
        datasets_captions.append(["Voltage Switch UN"])                  #27
        datasets_captions.append(["Voltage Gate U"])                  #28
        datasets_captions.append(["Voltage Gate UN"])                  #29
        datasets_captions.append(["Voltage Gate Source U"])                  #30
        datasets_captions.append(["Voltage Gate Source UN"])                  #31
        datasets_captions.append(["Voltage Filter Capacitor"])                  #32

        datasets_captions.append(["Power Battery Output"])                  #33
        datasets_captions.append(["Power DC Capacitor"])                  #32
        datasets_captions.append(["Power Switch U"])                  #37
        datasets_captions.append(["Power Switch UN"])                  #38
        datasets_captions.append(["Power Switch Diode U"])                  #39
        datasets_captions.append(["Power Switch Diode UN"])                  #40
        datasets_captions.append(["Power Load"])                  #41

        datasets_captions.append(["Current Phase Load U Harmonic Magnitudes"])                  #42
        datasets_captions.append(["Current Phase Load U Harmonic Phase Angles"])                  #43
        datasets_captions.append(["Current Line U Harmonic Magnitudes"])                  #44
        datasets_captions.append(["Current Line U Harmonic Phase Angles"])                  #45
        datasets_captions.append(["Current DC Bus Harmonic Magnitudes"])                  #46
        datasets_captions.append(["Current DC Bus Harmonic Phase Angles"])                  #47
        datasets_captions.append(["Current DC Capacitor Harmonic Magnitudes"])                  #48
        datasets_captions.append(["Current DC Capacitor Harmonic Phase Angles"])                  #49
        datasets_captions.append(["Voltage Phase Load U Harmonic Magnitudes"])                  #50
        datasets_captions.append(["Voltage Phase Load U Harmonic Phase Angles"])                  #51
        datasets_captions.append(["Voltage Line Load UV Harmonic Magnitudes"])                  #48
        datasets_captions.append(["Voltage Line Load UV Harmonic Phase Angles"])                  #49
        datasets_captions.append(["Voltage Line UV Harmonic Magnitudes"])                  #48
        datasets_captions.append(["Voltage Line UV Harmonic Phase Angles"])                  #49
        datasets_captions.append(["Active Power Harmonic Magnitudes"])                  #52
        datasets_captions.append(["Reactive Power Harmonic Magnitudes"])                  #53

        datasets_filters.append(["Current - AC","Time domain"])                  #0
        datasets_filters.append(["Current - AC","Time domain"])                  #1
        datasets_filters.append(["Current - AC","Time domain"])                  #2
        datasets_filters.append(["Current - AC","Time domain"])                  #3
        datasets_filters.append(["Current - AC","Time domain"])                  #4
        datasets_filters.append(["Current - AC","Time domain"])                  #5
        datasets_filters.append(["Current - DC","Time domain"])                  #6
        datasets_filters.append(["Current - DC","Time domain"])                  #7
        datasets_filters.append(["Current - DC","Time domain"])                  #8
        datasets_filters.append(["Current - Inverter","Time domain"])                  #9
        datasets_filters.append(["Current - Inverter","Time domain"])                  #10
        datasets_filters.append(["Current - Inverter","Time domain"])                  #11
        datasets_filters.append(["Current - Inverter","Time domain"])                  #12
        datasets_filters.append(["Current - Inverter","Time domain"])                  #13
        datasets_filters.append(["Current - Inverter","Time domain"])                  #14
        datasets_filters.append(["Current - Inverter","Time domain"])                  #15
        datasets_filters.append(["Current - AC","Time domain"])                  #16
        datasets_filters.append(["Current - Inverter","Time domain"])                  #17
        datasets_filters.append(["Current - Inverter","Time domain"])                  #18
        datasets_filters.append(["Current - AC","Time domain"])                  #19
        datasets_filters.append(["Current - DC","Time domain"])                  #20

        datasets_filters.append(["Voltage - DC","Time domain"])                  #21
        datasets_filters.append(["Voltage - DC","Time domain"])                  #22
        datasets_filters.append(["Voltage - AC","Time domain"])                  #23
        datasets_filters.append(["Voltage - AC","Time domain"])                  #24
        datasets_filters.append(["Voltage - AC","Time domain"])                  #25
        datasets_filters.append(["Voltage - AC","Time domain"])                  #20
        datasets_filters.append(["Voltage - AC","Time domain"])                  #21
        datasets_filters.append(["Voltage - AC","Time domain"])                  #22
        datasets_filters.append(["Voltage - AC","Time domain"])                  #23
        datasets_filters.append(["Voltage - AC","Time domain"])                  #24
        datasets_filters.append(["Voltage - AC","Time domain"])                  #25
        datasets_filters.append(["Voltage - Inverter","Time domain"])                  #26
        datasets_filters.append(["Voltage - Inverter","Time domain"])                  #27
        datasets_filters.append(["Voltage - Inverter","Time domain"])                  #28
        datasets_filters.append(["Voltage - Inverter","Time domain"])                  #29
        datasets_filters.append(["Voltage - Inverter","Time domain"])                  #30
        datasets_filters.append(["Voltage - Inverter","Time domain"])                  #31
        datasets_filters.append(["Voltage - AC","Time domain"])                  #31

        datasets_filters.append(["Power - DC","Time domain"])                  #31
        datasets_filters.append(["Power - DC","Time domain"])                  #32
        datasets_filters.append(["Power - Inverter","Time domain"])                  #33
        datasets_filters.append(["Power - Inverter","Time domain"])                  #34
        datasets_filters.append(["Power - Inverter","Time domain"])                  #35
        datasets_filters.append(["Power - Inverter","Time domain"])                  #36
        datasets_filters.append(["Power - AC","Time domain"])                  #37

        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #42
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #43
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #44
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #45
        datasets_filters.append(["Harmonics - DC","Frequency domain"])                  #46
        datasets_filters.append(["Harmonics - DC","Frequency domain"])                  #47
        datasets_filters.append(["Harmonics - DC","Frequency domain"])                  #48
        datasets_filters.append(["Harmonics - DC","Frequency domain"])                  #49
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #50
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #51
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #50
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #51
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #52
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #5
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #52
        datasets_filters.append(["Harmonics - AC","Frequency domain"])                  #5

        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #1
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #2
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #3
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #4
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #5
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #6
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #7
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #8
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #9
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #10
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #11
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #12
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #13
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #14
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #15
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #16
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #17
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #18
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #19
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #20
        datasets_graphs_settings.append(["xy","ms","A","min","max","min","max"])                  #21
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #22
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #23
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #24
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #25
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #26
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #27
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #28
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #29
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #30
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #31
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #32
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #33
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #34
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #35
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #36
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #37
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #38
        datasets_graphs_settings.append(["xy","ms","V","min","max","min","max"])                  #39
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])                  #40
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])                  #41
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])              
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])              
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])     
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])              
        datasets_graphs_settings.append(["xy","ms","kW","min","max","min","max"])     
        datasets_graphs_settings.append(["bars","Hz","A","min","max","min","max"])                  #42
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #43
        datasets_graphs_settings.append(["bars","Hz","A","min","max","min","max"])                  #44
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #45
        datasets_graphs_settings.append(["bars","Hz","A","min","max","min","max"])                  #46
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #47
        datasets_graphs_settings.append(["bars","Hz","A","min","max","min","max"])                  #48
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #49
        datasets_graphs_settings.append(["bars","Hz","V","min","max","min","max"])                  #48
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #49
        datasets_graphs_settings.append(["bars","Hz","V","min","max","min","max"])                  #50
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #51
        datasets_graphs_settings.append(["bars","Hz","V","min","max","min","max"])                  #52
        datasets_graphs_settings.append(["bars","Hz","deg","min","max","min","max"])                  #53
        datasets_graphs_settings.append(["bars","Hz","kW","min","max","min","max"])                  #53
        datasets_graphs_settings.append(["bars","Hz","kVAr","min","max","min","max"])                  #53

        datasets_names.append(["Current Phase Load U"])
        datasets_names.append(["Current Phase Load V"])
        datasets_names.append(["Current Phase Load W"])
        datasets_names.append(["Current Line U"])                  #1
        datasets_names.append(["Current Line V"])                  #2
        datasets_names.append(["Current Line W"])                  #3
        datasets_names.append(["Current DC Bus"])                  #4
        datasets_names.append(["Current DC Capacitor"])                  #5
        datasets_names.append(["Current DC Load"])                  #6
        datasets_names.append(["Current Switch U"])                  #7
        datasets_names.append(["Current Diode MOSFET U"])                  #5
        datasets_names.append(["Current MOSFET Channel U"])                  #6
        datasets_names.append(["Current Switch UN"])                  #7
        datasets_names.append(["Current Diode MOSFET UN"])                  #8
        datasets_names.append(["Current MOSFET Channel UN"])                  #9
        datasets_names.append(["Current Gate U"])                  #10
        datasets_names.append(["Current Gate UN"])                  #11
        datasets_names.append(["Current Filter Capacitor"])                  #12
        datasets_names.append(["Current Snubber Capacitor U"])                  #13
        datasets_names.append(["Current Snubber Capacitor UN"])                  #14
        datasets_names.append(["Current DC Ceramic Capacitor"])                  #15

        datasets_names.append(["Voltage DC Input"])                  #15
        datasets_names.append(["Voltage DC Capacitor"])                  #16
        datasets_names.append(["Voltage Line UV"])                  #17
        datasets_names.append(["Voltage Line VW"])                  #18
        datasets_names.append(["Voltage Line WU"])                  #19
        datasets_names.append(["Voltage Phase Load U"])                  #20
        datasets_names.append(["Voltage Phase Load V"])                  #21
        datasets_names.append(["Voltage Phase Load W"])                  #22
        datasets_names.append(["Voltage Line Load UV"])                  #23
        datasets_names.append(["Voltage Line Load VW"])                  #24
        datasets_names.append(["Voltage Line Load WU"])                  #25
        datasets_names.append(["Voltage Switch U"])                  #26
        datasets_names.append(["Voltage Switch UN"])                  #27
        datasets_names.append(["Voltage Gate U"])                  #28
        datasets_names.append(["Voltage Gate UN"])                  #29
        datasets_names.append(["Voltage Gate Source U"])                  #30
        datasets_names.append(["Voltage Gate Source UN"])                  #31
        datasets_names.append(["Voltage Filter Capacitor"])                  #32

        datasets_names.append(["Power Battery Output"])                  #33
        datasets_names.append(["Power DC Capacitor"])                  #32
        datasets_names.append(["Power Switch U"])                  #37
        datasets_names.append(["Power Switch UN"])                  #38
        datasets_names.append(["Power Switch Diode U"])                  #39
        datasets_names.append(["Power Switch Diode UN"])                  #40
        datasets_names.append(["Power Load"])                  #41

        datasets_names.append(["Current Phase Load U Harmonic Magnitudes"])                  #42
        datasets_names.append(["Current Phase Load U Harmonic Phase Angles"])                  #43
        datasets_names.append(["Current Line U Harmonic Magnitudes"])                  #44
        datasets_names.append(["Current Line U Harmonic Phase Angles"])                  #45
        datasets_names.append(["Current DC Bus Harmonic Magnitudes"])                  #46
        datasets_names.append(["Current DC Bus Harmonic Phase Angles"])                  #47
        datasets_names.append(["Current DC Capacitor Harmonic Magnitudes"])                  #48
        datasets_names.append(["Current DC Capacitor Harmonic Phase Angles"])                  #49
        datasets_names.append(["Voltage Phase Load U Harmonic Magnitudes"])                  #50
        datasets_names.append(["Voltage Phase Load U Harmonic Phase Angles"])                  #49
        datasets_names.append(["Voltage Line Load UV Harmonic Magnitudes"])                  #50
        datasets_names.append(["Voltage Line Load UV Harmonic Phase Angles"])                  #49
        datasets_names.append(["Voltage Line UV Harmonic Magnitudes"])                  #50
        datasets_names.append(["Voltage Line UV Harmonic Phase Angles"])                  #51
        datasets_names.append(["Active Power Harmonic Magnitudes"])                  #52
        datasets_names.append(["Reactive Power Harmonic Magnitudes"])                  #53       

        for i in range(len(datasets_captions)):
            datasets_values.append(inital_plot_function(361))
        
        return datasets_values, datasets_filters, datasets_captions, datasets_graphs_settings, datasets_names
            
    def export_to_csv(self, data_values,data_names):

        #-------------------------------------------list separator window----------------------------------------------
        default_separator = ','

        if len(data_values) > 1:    # Ask the user for the list separator only if data has more than one element
            separator_dialog = CTkInputDialog(text="Enter the list separator for series\n(default is   ','  ):", title="List Separator")
            separator_dialog.grab_set()
            list_separator = separator_dialog.get_input() or default_separator
        else:
            list_separator = default_separator
        
        #-------------------------------------------saving path----------------------------------------------

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]) # Ask the user where to save the file

        #-------------------------------------------print data----------------------------------------------

        if file_path:
            with open(file_path, mode='w', newline='') as file: # Write the data to a CSV file
                writer = csv.writer(file, delimiter=list_separator)

                data_names_flat= self.flatten_array(data_names)
                data_values_flat= self.flatten_array(data_values)

                writer.writerow(data_names_flat) # Write the data_names as the first row
                               
                for row in zip_longest(*data_values_flat, fillvalue=''):
                    writer.writerow(row)
                            
    def export_to_py(self, data_values,data_names):

        default_option = 'individual'

        # Ask the user for the writing option only if data has more than one element
        if len(data_values) > 1:
            write_option = default_option
            option_window = CTkToplevel()
            option_window.title("Writing Option")
            option_window.geometry("300x150")
            option_window.lift()  # Bring the window to the front
            option_window.attributes('-topmost', True)  # Keep it on top
            option_window.grab_set()  # Prevent clicking outside the popup

            def set_option(option):
                nonlocal write_option
                write_option = option
                option_window.destroy()

            label = CTkLabel(option_window, text="Choose how to write the series arrays:")
            label.pack(pady=PADDING)

            individual_button = CTkButton(option_window, text="Individual", command=lambda: set_option("individual"))
            individual_button.pack(pady=PADDING)

            combined_button = CTkButton(option_window, text="Combined", command=lambda: set_option("combined"))
            combined_button.pack(pady=PADDING)

            option_window.wait_window()
        else:
            write_option = default_option

        # Ask the user where to save the file
        file_path = filedialog.asksaveasfilename(defaultextension=".py", filetypes=[("Python files", "*.py"), ("All files", "*.*")])

        line_jump_var=15
        data_names_flat= self.flatten_array(data_names)
        data_values_flat= self.flatten_array(data_values)

        if file_path:
            # Write the data to a Python file
            with open(file_path, mode='w') as file:
                if write_option == 'combined':
                    file.write("Data = [\n")
                    for array in data_values_flat:
                        file.write("    [\n")
                        for i in range(0, len(array), line_jump_var):
                            line = "        " + ", ".join(map(str, array[i:i+line_jump_var]))
                            if i + line_jump_var < len(array):
                                line += ","
                            file.write(line + "\n")
                        file.write("    ]")
                        if array != data_values_flat[-1]:
                            file.write(",")
                        file.write("\n")
                    file.write("]\n")
                else:
                    for idx, array in enumerate(data_values_flat):
                        file.write(f"{data_names_flat[idx]} = [\n")
                        for i in range(0, len(array), line_jump_var):
                            line = "    " + ", ".join(map(str, array[i:i+line_jump_var]))
                            if i + line_jump_var < len(array):
                                line += ","
                            file.write(line + "\n")
                        file.write("]\n")
    
    def progress_bar_popup(self, current, total, bar_length):
        """
        Function to display a progress bar in a popup window.

        Parameters:
        current (int): The current progress count.
        total (int): The total count for completion.
        bar_length (int): The length of the progress bar. Default is 50.
        """
        # Create a new popup window
        progress_window = CTkToplevel()
        progress_window.title("Progress")
        progress_window.geometry("300x100")

        # Calculate the progress in percentage
        progress = float(current) / total
        # Calculate the number of filled positions in the bar
        block = int(round(bar_length * progress))
        # Create the progress bar string
        bar = "#" * block + "-" * (bar_length - block)

        # Create a label to display the progress bar
        progress_label = CTkLabel(progress_window, text=f"[{bar}] {round(progress * 100, 2)}%")
        progress_label.pack(pady=20)

        # Update the label when the progress is complete
        if current == total:
            progress_label.config(text="Completed!")
            progress_window.after(2000, progress_window.destroy)  # Close the window after 2 seconds
    
    def flatten_array(self, array):

        flattened = []
        for item in array:
            if isinstance(item, list) and any(isinstance(subitem, list) for subitem in item):
                flattened.extend(self.flatten_array(item))
            else:
                flattened.append(item)
        return flattened

    def create_bar_plot(self, Graph_frame, serie_data_y, x_label, y_label, x_lim_min, x_lim_max, y_lim_min, y_lim_max):


        #plt.style.use(BACKGROUND_STYLE)
        fig = graphs_fig(Graph_frame)
        ax = fig.add_subplot(111)

        x_values = space_x_values_log(self.f_main,self.f_main, len(serie_data_y))  # values for x axis
        ax.bar(x_values, serie_data_y, color=PLOT_LINE_COLORS[0])  
        ax.set_xscale('log') 

        graphs_ax(ax, fig, x_label, y_label)  

        canvas_plot(fig, Graph_frame) 

        #---------------------------------------------------------------------update cursor----------------------------------------------------------------

        cursor_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, color=CURSOR_TEXT_COLOR, bbox=dict(facecolor=CURSOR_TEXT_BACKGROUND_COLOR, alpha=0.7))

        def update_cursor(event):
            if event.inaxes:
                cursor_text.set_text(f'x: {event.xdata:.2f}\ny: {event.ydata:.2f}')
                fig.canvas.draw_idle()
            else:
                cursor_text.set_text('')
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', update_cursor)
    
    #MODIFIED
    def create_xy_plot(self, Graph_frame, series_data_y, x_label, y_label, var_domain, y_lim_min, y_lim_max):

        y_lim_max_result=max_value_lim(series_data_y,y_lim_max)

        y_lim_min_result=min_value_lim(series_data_y,y_lim_min)

        fig = graphs_fig(Graph_frame)
        ax = fig.add_subplot(111)

        match var_domain:
            case 1:
                limit_label_x=360
                x_label_result = "deg"

                ax.set_xticks([0, 90, 180, 270, 360])
                ax.set_xticklabels(['0', '90', '180', '270', '360'])
            case 2:
                limit_label_x=1000/self.f_main
                x_label_result=x_label

                ax.set_xticks([0, limit_label_x/4, 2*limit_label_x/4, 3*limit_label_x/4, limit_label_x])
                ax.set_xticklabels(['0', limit_label_x/4, 2*limit_label_x/4, 3*limit_label_x/4, limit_label_x])
                
        if isinstance(series_data_y[0], (list, tuple)):

            x_list_values = []

            series_data_y_np = np.array(series_data_y, dtype=np.float64)
            x_list_values = create_x_list_values(series_data_y_np, limit_label_x)

            for i, (x_data, y_data) in enumerate(zip(x_list_values, series_data_y)):
                
                ax.plot(x_data, y_data, color=PLOT_LINE_COLORS[i % len(PLOT_LINE_COLORS)], linestyle='-')

        else:   
                
            x_values=space_x_values(0,limit_label_x,len(series_data_y))
              
            ax.plot(x_values, series_data_y, color=PLOT_LINE_COLORS[0], linestyle='-')    

        graphs_ax(ax, fig, x_label_result, y_label) 

        ax.set_xlim(0, limit_label_x)  
        ax.set_ylim(y_lim_min_result, y_lim_max_result)
                
        canvas_plot(fig, Graph_frame) 

        #---------------------------------------------------------------------update cursor----------------------------------------------------------------

        cursor_text = ax.text(0.02, 0.98, '', transform=ax.transAxes, color=CURSOR_TEXT_COLOR, bbox=dict(facecolor=CURSOR_TEXT_BACKGROUND_COLOR, alpha=0.7))

        def update_cursor(event):
            if event.inaxes:
                cursor_text.set_text(f'x: {event.xdata:.2f}\ny: {event.ydata:.2f}')
                fig.canvas.draw_idle()
            else:
                cursor_text.set_text('')
                fig.canvas.draw_idle()

        fig.canvas.mpl_connect('motion_notify_event', update_cursor)

    def create_plot(self, frame, datasets_y ,graph_info):
        match graph_info[0]:
            case "xy":
                self.create_xy_plot(frame, datasets_y, graph_info[1], graph_info[2], 1, graph_info[5], graph_info[6])   
            case "bars":
                self.create_bar_plot(frame, datasets_y, graph_info[1], graph_info[2], graph_info[3], graph_info[4], graph_info[5], graph_info[6])

    def toggle_domain(self, var_domain, graph_frame, datasets_y, graph_info):



        grid_info = graph_frame.grid_info()
        row = grid_info['row']

        if var_domain[row]==2:
            var_domain[row]=1
        else:
            var_domain[row]=2

        if graph_info[0]=="xy":
            self.create_xy_plot(graph_frame, datasets_y, graph_info[1], graph_info[2], var_domain[row], graph_info[5], graph_info[6])

    def scrollbar_function(self, main_frame):

        height_value=250

        #canvas = CTkCanvas(main_frame, bg="#2b2b2b", highlightthickness=0)
        #canvas = CTkCanvas(main_frame, bg=BACKGROUND_STYLE)

        
        canvas = CTkCanvas(main_frame, bg=FIGURE_BACKGROUND_COLOR, highlightthickness=0)  # (light mode, dark mode)

        canvas.grid(row=0, column=0, sticky="ns", padx=PADDING, pady=PADDING)

        second_frame = CTkFrame(canvas)

        scrollbar = CTkScrollbar(main_frame, orientation="vertical", command=canvas.yview)

        self.scrollbar_item=canvas
        self.scrollbar_bar=scrollbar
        
        scrollbar.grid(row=0, column=1, sticky="ns", padx=PADDING, pady=PADDING)

        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0,0), window=second_frame, anchor="nw")

        # Enable mouse wheel scrolling when hovering over the canvas
        def on_mouse_wheel(event):
            canvas.yview_scroll(int(-1*(event.delta/30)), "units")

        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", on_mouse_wheel))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        canvas.grid_rowconfigure(0, weight=1)
        canvas.grid_columnconfigure(0, weight=1)

        scrollbar.grid_rowconfigure(0, weight=1)
        scrollbar.grid_columnconfigure(0, weight=0)

        return second_frame,canvas



import numpy as np

@njit
def space_x_values(limit_min, limit_max, length):
    K = (limit_max - limit_min) / (length - 1)
    x_values = np.empty(length, dtype=np.float64)  
    for i in range(length):
        x_values[i] = limit_min + i * K
    return x_values

@njit
def create_x_list_values(series_data_y, limit_label_x):
    num_series = series_data_y.shape[0]
    length = series_data_y.shape[1]
    
    x_list_values = np.empty((num_series, length), dtype=np.float64)
    
    for i in range(num_series):
        x_list_values[i, :] = space_x_values(0, limit_label_x, length)
    return x_list_values