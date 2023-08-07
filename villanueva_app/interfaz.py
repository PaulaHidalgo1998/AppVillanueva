# Importa los módulos de Tkinter
import tkinter as tk
from tkinter import ttk
from controlador import Controlador

# Crea la clase de la interfaz gráfica
class InterfazGraficaRaiz(tk.Tk):
    def __init__(self):
        super().__init__()

        # Configura la ventana principal
        self.title("Pagos de las cuotas")
        #self.geometry("400x300")
        self.iconbitmap("festejos.ico")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = FrameInterfazGrafica(self)
        frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

class FrameInterfazGrafica(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        # Configura el redimensionamiento
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(1, weight=1)

        
        # Agregar al constructor de FrameInterfazGrafica para personalizar los botones
        style = ttk.Style(self)
        style.configure("Green.TButton", foreground="black", background="green", font=("Times New Roman", 12))
        style.configure("Red.TButton", foreground="black", background="red", font=("Times New Roman", 12))
        style.configure("Orange.TButton", foreground="black", background="orange", font=("Times New Roman", 12))


        style = ttk.Style(self)
        style.configure("Treeview", padding=(20, 1), rowheight=25)
        style.configure("Label", padding=(20, 1), rowheight=25)
        style.configure("Entry", padding=(20, 1), rowheight=25)

        # Agrega widgets a la ventana
        label_nombre = tk.Label(self, text="Nombre:", font=("Times New Roman", 14))
        label_nombre.grid(row=0, column=0, sticky='w')

        self.nombre = tk.Entry(self)
        self.nombre.grid(row=0, column=1, padx=5, sticky='w')

        label_apellidos = tk.Label(self, text="Apellidos:", font=("Times New Roman", 14))
        label_apellidos.grid(row=1, column=0, sticky='w')

        self.apellidos = tk.Entry(self)
        self.apellidos.grid(row=1, column=1, pady=5, padx=5, sticky='w')

        label_dinero = tk.Label(self, text="Dinero aportado:", font=("Times New Roman", 14))
        label_dinero.grid(row=2, column=0, sticky='w')

        self.dinero = tk.Entry(self)
        self.dinero.grid(row=2, column=1, pady=5, padx=5, sticky='w')

        button_crear = ttk.Button(self, text="Crear persona", command=self.crear_persona, style="Green.TButton")
        # button_crear.grid(row=4, column=0, columnspan=2, pady=10)
        button_crear.grid(row=1, column=2, pady=5, padx=10)

        # Crear el Treeview
        self.tree = ttk.Treeview(self, columns=("numero_socio", "apellidos", "nombre", "tipo_aportacion", "dinero_aportado"), show="headings")
        self.tree.heading("numero_socio", text="Número de Socio")
        self.tree.heading("apellidos", text="Apellidos")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("tipo_aportacion", text="Tipo de Aportación")
        self.tree.heading("dinero_aportado", text="Dinero Aportado")
        self.tree.grid(row=3, column=0, columnspan=4, padx=10, pady=10)

        button_borrar_persona = ttk.Button(self, text="Borrar persona", command=self.borrar_persona, style="Red.TButton")
        button_borrar_persona.grid(row=4, column=0, columnspan=2, sticky='w')

        button_borrar_todo = ttk.Button(self, text="Borrar todo", command=self.borrar_todo, style="Red.TButton")
        button_borrar_todo.grid(row=4, column=1, sticky='e')

        button_pdf = ttk.Button(self, text="Generar PDF", command=self.generar_pdf_personas, style="Orange.TButton")
        button_pdf.grid(row=4, column=1, sticky='e')

        # Obtener datos del modelo Persona
        #personas = controlador

        # Insertar datos en la tabla
        #for persona in personas:
        self.tree.insert("", "end", values=(1, 'Hidalgo', 'Paula', 'Adulto', 40))

        # Asociar el evento de selección de la fila a una función
        self.tree.bind("<<TreeviewSelect>>", self.seleccionar_persona)

    def crear_persona(self):
        nombre_persona = self.nombre.get()
        apellidos_persona = self.apellidos.get()
        dinero_persona = self.dinero.get()
        # controlador.guardar_persona(nombre_persona, apellidos_persona, dinero_persona)

        # Refresh the table
        personas = controlador.obtener_personas()
        self.refresh_table(personas)

    def borrar_persona(self):
        controlador.borrar_persona(self.persona_seleccionada)

        personas = controlador.obtener_personas()
        self.refresh_table(personas)
    
    def borrar_todo(self):
        controlador.borrar_todo()
        # Refresh the table
        personas = controlador.obtener_personas()
        self.refresh_table(personas)

    def generar_pdf_personas(self):
        controlador.generar_pdf_personas_listado()

    def seleccionar_persona(self, event):
        # Obtener el id de la fila seleccionada
        selected_item = self.tree.selection()[0]
        self.persona_seleccionada = self.tree.item(selected_item, "values")[0]  # obtenemos el nº de socio

        # Utiliza el id como desees (por ejemplo, imprimirlo)
        print("ID seleccionado:", self.persona_seleccionada)

    def refresh_table(self, personas):
        # Clear existing data in the table
        self.tree.delete(*self.tree.get_children())

        # Insert updated data into the table
        for persona in personas:
            self.tree.insert("", "end", values=(persona.numero_socio, persona.apellidos, persona.nombre, persona.tipo_aportacion, persona.dinero_aportado))

# Crea una instancia de la interfaz gráfica y entra al bucle principal
if __name__ == "__main__":
    app = InterfazGraficaRaiz()
    controlador = Controlador()
    app.mainloop()
