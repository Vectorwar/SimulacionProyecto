import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import mysql.connector
from datetime import datetime

class VacunacionSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Vacunación")
        self.root.geometry("1200x700")
        self.conn = None
        self.cursor = None
        self.current_user = None
        self.current_role = None
        
        # Configurar estilo
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.show_login()
        
    def connect_db(self, user, password):
        """Conectar a la base de datos con las credenciales del usuario"""
        try:
            self.conn = mysql.connector.connect(
                host="localhost",
                user=user,
                password=password,
                database="vacunacion_db"
            )
            self.cursor = self.conn.cursor(dictionary=True)
            return True
        except mysql.connector.Error as err:
            messagebox.showerror("Error de Conexión", f"Error: {err}")
            return False
    
    def show_login(self):
        """Pantalla de inicio de sesión"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill="both", expand=True)
        
        # Frame del login
        login_frame = tk.Frame(main_frame, bg="white", padx=40, pady=40)
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Título
        title = tk.Label(login_frame, text="Sistema de Vacunación", 
                        font=("Arial", 24, "bold"), bg="white", fg="#2c3e50")
        title.pack(pady=(0, 30))
        
        # Selección de rol
        tk.Label(login_frame, text="Seleccione su rol:", 
                font=("Arial", 12), bg="white").pack(pady=(0, 10))
        
        roles_frame = tk.Frame(login_frame, bg="white")
        roles_frame.pack(pady=10)
        
        roles = [
            ("Administrador", "admin", "admin123", "#e74c3c"),
            ("Médico", "medico", "medico123", "#3498db"),
            ("Enfermero", "enfermero", "enfermero123", "#2ecc71"),
            ("Recepcionista", "recepcionista", "recep123", "#f39c12")
        ]
        
        for i, (role_name, username, password, color) in enumerate(roles):
            btn = tk.Button(roles_frame, text=role_name, 
                          width=15, height=2,
                          font=("Arial", 11, "bold"),
                          bg=color, fg="white",
                          cursor="hand2",
                          command=lambda u=username, p=password, r=role_name: self.login(u, p, r))
            btn.grid(row=i//2, column=i%2, padx=10, pady=10)
    
    def login(self, username, password, role):
        """Procesar el inicio de sesión"""
        if self.connect_db(username, password):
            self.current_user = username
            self.current_role = role
            self.show_main_interface()
    
    def show_main_interface(self):
        """Mostrar la interfaz principal según el rol"""
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg="#ecf0f1")
        main_frame.pack(fill="both", expand=True)
        
        # Header
        header = tk.Frame(main_frame, bg="#34495e", height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tk.Label(header, text=f"Sistema de Vacunación - {self.current_role}", 
                font=("Arial", 16, "bold"), bg="#34495e", fg="white").pack(side="left", padx=20)
        
        tk.Button(header, text="Cerrar Sesión", 
                 command=self.show_login,
                 bg="#e74c3c", fg="white", 
                 font=("Arial", 10, "bold"),
                 cursor="hand2").pack(side="right", padx=20)
        
        # Panel lateral y área de trabajo
        content_frame = tk.Frame(main_frame, bg="#ecf0f1")
        content_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Panel lateral con opciones
        sidebar = tk.Frame(content_frame, bg="white", width=200)
        sidebar.pack(side="left", fill="y", padx=(0, 10))
        sidebar.pack_propagate(False)
        
        # Área de trabajo
        self.work_area = tk.Frame(content_frame, bg="white")
        self.work_area.pack(side="left", fill="both", expand=True)
        
        # Crear menú según el rol
        self.create_menu(sidebar)
        
        # Mostrar pantalla de bienvenida
        self.show_welcome()
    
    def create_menu(self, parent):
        """Crear menú según el rol del usuario"""
        tk.Label(parent, text="Menú", font=("Arial", 14, "bold"), 
                bg="white").pack(pady=20)
        
        if self.current_role == "Administrador":
            self.create_button(parent, "Gestionar Pacientes", lambda: self.show_crud("Pacientes"))
            self.create_button(parent, "Gestionar Vacunas", lambda: self.show_crud("Vacunas"))
            self.create_button(parent, "Gestionar Campañas", lambda: self.show_crud("Campañas"))
            self.create_button(parent, "Gestionar Vacunaciones", lambda: self.show_crud("Vacunaciones"))
            self.create_button(parent, "Consultas Avanzadas", self.show_queries)
            
        elif self.current_role == "Médico":
            self.create_button(parent, "Ver/Actualizar Pacientes", lambda: self.show_read_update("Pacientes"))
            self.create_button(parent, "Ver/Actualizar Vacunaciones", lambda: self.show_read_update("Vacunaciones"))
            self.create_button(parent, "Ver Vacunas", lambda: self.show_read_only("Vacunas"))
            self.create_button(parent, "Ver Campañas", lambda: self.show_read_only("Campañas"))
            self.create_button(parent, "Consultas", self.show_queries)
            
        elif self.current_role == "Enfermero":
            self.create_button(parent, "Ver Pacientes", lambda: self.show_read_only("Pacientes"))
            self.create_button(parent, "Ver Vacunas", lambda: self.show_read_only("Vacunas"))
            self.create_button(parent, "Ver Campañas", lambda: self.show_read_only("Campañas"))
            self.create_button(parent, "Registrar Vacunación", self.show_insert_vaccination)
            self.create_button(parent, "Consultas", self.show_queries)
            
        elif self.current_role == "Recepcionista":
            self.create_button(parent, "Ver Pacientes", lambda: self.show_read_only("Pacientes"))
            self.create_button(parent, "Ver Vacunas", lambda: self.show_read_only("Vacunas"))
            self.create_button(parent, "Ver Campañas", lambda: self.show_read_only("Campañas"))
            self.create_button(parent, "Consultas", self.show_queries)
    
    def create_button(self, parent, text, command):
        """Crear botón del menú"""
        btn = tk.Button(parent, text=text, command=command,
                       bg="#3498db", fg="white",
                       font=("Arial", 10),
                       cursor="hand2",
                       width=20, height=2)
        btn.pack(pady=5, padx=10)
    
    def show_welcome(self):
        """Mostrar pantalla de bienvenida"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.work_area, bg="white")
        welcome_frame.pack(expand=True)
        
        tk.Label(welcome_frame, text=f"Bienvenido, {self.current_role}", 
                font=("Arial", 24, "bold"), bg="white").pack(pady=20)
        
        tk.Label(welcome_frame, text="Seleccione una opción del menú lateral", 
                font=("Arial", 14), bg="white").pack()
    
    def show_crud(self, table):
        """Mostrar interfaz CRUD completa (solo para administrador)"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        # Título
        tk.Label(self.work_area, text=f"Gestión de {table}", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        # Frame para botones
        btn_frame = tk.Frame(self.work_area, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Agregar", command=lambda: self.add_record(table),
                 bg="#2ecc71", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Actualizar", command=lambda: self.update_record(table),
                 bg="#f39c12", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=lambda: self.delete_record(table),
                 bg="#e74c3c", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refrescar", command=lambda: self.show_crud(table),
                 bg="#3498db", fg="white", width=12).pack(side="left", padx=5)
        
        # Tabla de datos
        self.create_table_view(table)
    
    def show_read_update(self, table):
        """Mostrar interfaz de lectura y actualización (para médico)"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text=f"Ver/Actualizar {table}", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        btn_frame = tk.Frame(self.work_area, bg="white")
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="Actualizar", command=lambda: self.update_record(table),
                 bg="#f39c12", fg="white", width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Refrescar", command=lambda: self.show_read_update(table),
                 bg="#3498db", fg="white", width=12).pack(side="left", padx=5)
        
        self.create_table_view(table)
    
    def show_read_only(self, table):
        """Mostrar interfaz de solo lectura"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text=f"Ver {table}", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        tk.Button(self.work_area, text="Refrescar", 
                 command=lambda: self.show_read_only(table),
                 bg="#3498db", fg="white", width=12).pack(pady=10)
        
        self.create_table_view(table)
    
    def create_table_view(self, table):
        """Crear vista de tabla con datos"""
        # Frame para la tabla
        table_frame = tk.Frame(self.work_area, bg="white")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Scrollbars
        scroll_y = tk.Scrollbar(table_frame, orient="vertical")
        scroll_x = tk.Scrollbar(table_frame, orient="horizontal")
        
        # Treeview
        self.tree = ttk.Treeview(table_frame, 
                                 yscrollcommand=scroll_y.set,
                                 xscrollcommand=scroll_x.set,
                                 selectmode="browse")
        
        scroll_y.config(command=self.tree.yview)
        scroll_x.config(command=self.tree.xview)
        scroll_y.pack(side="right", fill="y")
        scroll_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
        
        # Cargar datos
        try:
            self.cursor.execute(f"SELECT * FROM {table}")
            records = self.cursor.fetchall()
            
            if records:
                # Configurar columnas
                columns = list(records[0].keys())
                self.tree["columns"] = columns
                self.tree["show"] = "headings"
                
                for col in columns:
                    self.tree.heading(col, text=col)
                    self.tree.column(col, width=100)
                
                # Insertar datos
                for record in records:
                    values = [record[col] for col in columns]
                    self.tree.insert("", "end", values=values)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error al cargar datos: {err}")
    
    def add_record(self, table):
        """Ventana para agregar registro"""
        add_window = tk.Toplevel(self.root)
        add_window.title(f"Agregar {table}")
        add_window.geometry("400x500")
        
        # Obtener estructura de la tabla
        self.cursor.execute(f"DESCRIBE {table}")
        columns = self.cursor.fetchall()
        
        entries = {}
        row = 0
        
        for col in columns:
            if col['Key'] != 'PRI':  # Skip auto-increment primary key
                tk.Label(add_window, text=col['Field']).grid(row=row, column=0, padx=10, pady=5, sticky="w")
                entry = tk.Entry(add_window, width=30)
                entry.grid(row=row, column=1, padx=10, pady=5)
                entries[col['Field']] = entry
                row += 1
        
        def save():
            values = {field: entry.get() for field, entry in entries.items()}
            fields = ", ".join(values.keys())
            placeholders = ", ".join(["%s"] * len(values))
            
            try:
                query = f"INSERT INTO {table} ({fields}) VALUES ({placeholders})"
                self.cursor.execute(query, list(values.values()))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Registro agregado correctamente")
                add_window.destroy()
                self.show_crud(table)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al insertar: {err}")
        
        tk.Button(add_window, text="Guardar", command=save,
                 bg="#2ecc71", fg="white", width=15).grid(row=row, column=0, columnspan=2, pady=20)
    
    def update_record(self, table):
        """Actualizar registro seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro para actualizar")
            return
        
        # Obtener valores del registro seleccionado
        values = self.tree.item(selected[0])['values']
        columns = self.tree["columns"]
        
        update_window = tk.Toplevel(self.root)
        update_window.title(f"Actualizar {table}")
        update_window.geometry("400x500")
        
        entries = {}
        for i, col in enumerate(columns):
            tk.Label(update_window, text=col).grid(row=i, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(update_window, width=30)
            entry.insert(0, values[i])
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries[col] = entry
            
            # Deshabilitar clave primaria
            if i == 0:
                entry.config(state="disabled")
        
        def save():
            new_values = {field: entry.get() for field, entry in entries.items()}
            pk_field = columns[0]
            pk_value = values[0]
            
            set_clause = ", ".join([f"{field} = %s" for field in columns[1:]])
            
            try:
                query = f"UPDATE {table} SET {set_clause} WHERE {pk_field} = %s"
                self.cursor.execute(query, list(new_values.values())[1:] + [pk_value])
                self.conn.commit()
                messagebox.showinfo("Éxito", "Registro actualizado correctamente")
                update_window.destroy()
                if self.current_role == "Administrador":
                    self.show_crud(table)
                else:
                    self.show_read_update(table)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al actualizar: {err}")
        
        tk.Button(update_window, text="Guardar", command=save,
                 bg="#f39c12", fg="white", width=15).grid(row=len(columns), column=0, columnspan=2, pady=20)
    
    def delete_record(self, table):
        """Eliminar registro seleccionado"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "Seleccione un registro para eliminar")
            return
        
        if messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este registro?"):
            values = self.tree.item(selected[0])['values']
            columns = self.tree["columns"]
            pk_field = columns[0]
            pk_value = values[0]
            
            try:
                query = f"DELETE FROM {table} WHERE {pk_field} = %s"
                self.cursor.execute(query, (pk_value,))
                self.conn.commit()
                messagebox.showinfo("Éxito", "Registro eliminado correctamente")
                self.show_crud(table)
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al eliminar: {err}")
    
    def show_insert_vaccination(self):
        """Interfaz para insertar vacunación (enfermero)"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Registrar Nueva Vacunación", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=20)
        
        form_frame = tk.Frame(self.work_area, bg="white")
        form_frame.pack(pady=20)
        
        # Obtener datos para los combobox
        self.cursor.execute("SELECT ID_Paciente, CONCAT(Nombre, ' ', Apellido) as Nombre_Completo FROM Pacientes")
        pacientes = self.cursor.fetchall()
        
        self.cursor.execute("SELECT ID_Vacuna, Nombre FROM Vacunas")
        vacunas = self.cursor.fetchall()
        
        self.cursor.execute("SELECT ID_Campaña, Nombre FROM Campañas")
        campañas = self.cursor.fetchall()
        
        # Paciente
        tk.Label(form_frame, text="Paciente:", bg="white").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        paciente_var = tk.StringVar()
        paciente_combo = ttk.Combobox(form_frame, textvariable=paciente_var, width=30)
        paciente_combo['values'] = [f"{p['ID_Paciente']} - {p['Nombre_Completo']}" for p in pacientes]
        paciente_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Vacuna
        tk.Label(form_frame, text="Vacuna:", bg="white").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        vacuna_var = tk.StringVar()
        vacuna_combo = ttk.Combobox(form_frame, textvariable=vacuna_var, width=30)
        vacuna_combo['values'] = [f"{v['ID_Vacuna']} - {v['Nombre']}" for v in vacunas]
        vacuna_combo.grid(row=1, column=1, padx=10, pady=10)
        
        # Campaña
        tk.Label(form_frame, text="Campaña:", bg="white").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        campaña_var = tk.StringVar()
        campaña_combo = ttk.Combobox(form_frame, textvariable=campaña_var, width=30)
        campaña_combo['values'] = [f"{c['ID_Campaña']} - {c['Nombre']}" for c in campañas]
        campaña_combo.grid(row=2, column=1, padx=10, pady=10)
        
        # Fecha
        tk.Label(form_frame, text="Fecha (YYYY-MM-DD):", bg="white").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        fecha_entry = tk.Entry(form_frame, width=32)
        fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        fecha_entry.grid(row=3, column=1, padx=10, pady=10)
        
        # Dosis
        tk.Label(form_frame, text="Número de Dosis:", bg="white").grid(row=4, column=0, padx=10, pady=10, sticky="w")
        dosis_entry = tk.Entry(form_frame, width=32)
        dosis_entry.grid(row=4, column=1, padx=10, pady=10)
        
        def guardar_vacunacion():
            try:
                id_paciente = int(paciente_var.get().split(" - ")[0])
                id_vacuna = int(vacuna_var.get().split(" - ")[0])
                id_campaña = int(campaña_var.get().split(" - ")[0])
                fecha = fecha_entry.get()
                dosis = int(dosis_entry.get())
                
                query = """INSERT INTO Vacunaciones 
                          (ID_Paciente, ID_Vacuna, ID_Campaña, Fecha_Vacunacion, Dosis) 
                          VALUES (%s, %s, %s, %s, %s)"""
                
                self.cursor.execute(query, (id_paciente, id_vacuna, id_campaña, fecha, dosis))
                self.conn.commit()
                
                messagebox.showinfo("Éxito", "Vacunación registrada correctamente")
                
                # Limpiar campos
                paciente_combo.set('')
                vacuna_combo.set('')
                campaña_combo.set('')
                fecha_entry.delete(0, tk.END)
                fecha_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
                dosis_entry.delete(0, tk.END)
                
            except ValueError as e:
                messagebox.showerror("Error", "Por favor complete todos los campos correctamente")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error al registrar: {err}")
        
        tk.Button(form_frame, text="Guardar Vacunación", command=guardar_vacunacion,
                 bg="#2ecc71", fg="white", width=20, height=2).grid(row=5, column=0, columnspan=2, pady=20)
    
    def show_queries(self):
        """Mostrar consultas avanzadas"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        tk.Label(self.work_area, text="Consultas Avanzadas", 
                font=("Arial", 18, "bold"), bg="white").pack(pady=10)
        
        # Frame de botones
        queries_frame = tk.Frame(self.work_area, bg="white")
        queries_frame.pack(pady=10)
        
        queries = [
            ("Pacientes por Campaña", self.query_patients_by_campaign),
            ("Vacunaciones por Vacuna", self.query_vaccinations_by_vaccine),
            ("Dosis Incompletas", self.query_incomplete_doses),
            ("Historial de Paciente", self.query_patient_history),
            ("Vacunaciones por Campaña", self.query_vaccinations_by_campaign),
            ("Contactos por Vacuna", self.query_contacts_by_vaccine)
        ]
        
        for i, (text, command) in enumerate(queries):
            tk.Button(queries_frame, text=text, command=command,
                     bg="#3498db", fg="white", width=25, height=2).grid(row=i//2, column=i%2, padx=10, pady=5)
        
        # Área de resultados
        self.results_area = scrolledtext.ScrolledText(self.work_area, width=120, height=25, wrap=tk.WORD)
        self.results_area.pack(pady=10, padx=20, fill="both", expand=True)
    
    def display_query_results(self, results, columns):
        """Mostrar resultados de consulta"""
        self.results_area.delete(1.0, tk.END)
        
        if not results:
            self.results_area.insert(tk.END, "No se encontraron resultados.\n")
            return
        
        # Encabezados
        header = " | ".join([f"{col:20}" for col in columns])
        self.results_area.insert(tk.END, header + "\n")
        self.results_area.insert(tk.END, "-" * len(header) + "\n")
        
        # Datos
        for row in results:
            line = " | ".join([f"{str(row[col]):20}" for col in columns])
            self.results_area.insert(tk.END, line + "\n")
    
    def query_patients_by_campaign(self):
        """Consulta 1: Pacientes vacunados en una campaña específica"""
        query = """
        SELECT p.Nombre, p.Apellido, v.Nombre AS Vacuna, c.Nombre AS Campaña, vac.Fecha_Vacunacion
        FROM Vacunaciones vac
        JOIN Pacientes p ON vac.ID_Paciente = p.ID_Paciente
        JOIN Vacunas v ON vac.ID_Vacuna = v.ID_Vacuna
        JOIN Campañas c ON vac.ID_Campaña = c.ID_Campaña
        WHERE c.Nombre = 'Campaña de Invierno 2024'
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = ['Nombre', 'Apellido', 'Vacuna', 'Campaña', 'Fecha_Vacunacion']
            self.display_query_results(results, columns)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en consulta: {err}")
    
    def query_vaccinations_by_vaccine(self):
        """Consulta 2: Número de vacunaciones por vacuna"""
        query = """
        SELECT v.Nombre AS Vacuna, COUNT(vac.ID_Vacunacion) AS Numero_Vacunaciones
        FROM Vacunaciones vac
        JOIN Vacunas v ON vac.ID_Vacuna = v.ID_Vacuna
        GROUP BY v.Nombre
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = ['Vacuna', 'Numero_Vacunaciones']
            self.display_query_results(results, columns)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en consulta: {err}")
    
    def query_incomplete_doses(self):
        """Consulta 3: Pacientes con dosis incompletas"""
        query = """
        SELECT p.Nombre, p.Apellido, v.Nombre AS Vacuna, 
               COUNT(vac.ID_Vacunacion) AS Dosis_Recibidas, 
               v.Numero_Dosis AS Dosis_Requeridas
        FROM Vacunaciones vac
        JOIN Pacientes p ON vac.ID_Paciente = p.ID_Paciente
        JOIN Vacunas v ON vac.ID_Vacuna = v.ID_Vacuna
        GROUP BY p.ID_Paciente, v.ID_Vacuna
        HAVING COUNT(vac.ID_Vacunacion) < v.Numero_Dosis
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = ['Nombre', 'Apellido', 'Vacuna', 'Dosis_Recibidas', 'Dosis_Requeridas']
            self.display_query_results(results, columns)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en consulta: {err}")
    
    def query_patient_history(self):
        """Consulta 4: Historial de vacunación de un paciente específico"""
        # Ventana para seleccionar paciente
        patient_window = tk.Toplevel(self.root)
        patient_window.title("Seleccionar Paciente")
        patient_window.geometry("400x150")
        
        tk.Label(patient_window, text="Seleccione un paciente:").pack(pady=10)
        
        # Obtener lista de pacientes
        self.cursor.execute("SELECT ID_Paciente, CONCAT(Nombre, ' ', Apellido) as Nombre_Completo FROM Pacientes")
        pacientes = self.cursor.fetchall()
        
        patient_var = tk.StringVar()
        patient_combo = ttk.Combobox(patient_window, textvariable=patient_var, width=40)
        patient_combo['values'] = [f"{p['ID_Paciente']} - {p['Nombre_Completo']}" for p in pacientes]
        patient_combo.pack(pady=10)
        
        def execute_query():
            try:
                id_paciente = int(patient_var.get().split(" - ")[0])
                query = """
                SELECT p.Nombre, p.Apellido, v.Nombre AS Vacuna, c.Nombre AS Campaña,
                       vac.Fecha_Vacunacion, vac.Dosis
                FROM Vacunaciones vac
                JOIN Pacientes p ON vac.ID_Paciente = p.ID_Paciente
                JOIN Vacunas v ON vac.ID_Vacuna = v.ID_Vacuna
                JOIN Campañas c ON vac.ID_Campaña = c.ID_Campaña
                WHERE p.ID_Paciente = %s
                """
                self.cursor.execute(query, (id_paciente,))
                results = self.cursor.fetchall()
                columns = ['Nombre', 'Apellido', 'Vacuna', 'Campaña', 'Fecha_Vacunacion', 'Dosis']
                self.display_query_results(results, columns)
                patient_window.destroy()
            except (ValueError, IndexError):
                messagebox.showwarning("Advertencia", "Seleccione un paciente válido")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error en consulta: {err}")
        
        tk.Button(patient_window, text="Consultar", command=execute_query,
                 bg="#3498db", fg="white", width=15).pack(pady=10)
    
    def query_vaccinations_by_campaign(self):
        """Consulta 5: Vacunaciones por campaña"""
        query = """
        SELECT c.Nombre AS Campaña, COUNT(vac.ID_Vacunacion) AS Numero_Vacunaciones
        FROM Campañas c
        LEFT JOIN Vacunaciones vac ON c.ID_Campaña = vac.ID_Campaña
        GROUP BY c.Nombre
        """
        try:
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            columns = ['Campaña', 'Numero_Vacunaciones']
            self.display_query_results(results, columns)
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error en consulta: {err}")
    
    def query_contacts_by_vaccine(self):
        """Consulta 6: Contactos de pacientes por vacuna"""
        # Ventana para seleccionar vacuna
        vaccine_window = tk.Toplevel(self.root)
        vaccine_window.title("Seleccionar Vacuna")
        vaccine_window.geometry("400x150")
        
        tk.Label(vaccine_window, text="Seleccione una vacuna:").pack(pady=10)
        
        # Obtener lista de vacunas
        self.cursor.execute("SELECT ID_Vacuna, Nombre FROM Vacunas")
        vacunas = self.cursor.fetchall()
        
        vaccine_var = tk.StringVar()
        vaccine_combo = ttk.Combobox(vaccine_window, textvariable=vaccine_var, width=40)
        vaccine_combo['values'] = [f"{v['ID_Vacuna']} - {v['Nombre']}" for v in vacunas]
        vaccine_combo.pack(pady=10)
        
        def execute_query():
            try:
                nombre_vacuna = vaccine_var.get().split(" - ")[1]
                query = """
                SELECT p.Nombre, p.Apellido, p.Telefono, p.Email
                FROM Vacunaciones vac
                JOIN Pacientes p ON vac.ID_Paciente = p.ID_Paciente
                JOIN Vacunas v ON vac.ID_Vacuna = v.ID_Vacuna
                WHERE v.Nombre = %s
                """
                self.cursor.execute(query, (nombre_vacuna,))
                results = self.cursor.fetchall()
                columns = ['Nombre', 'Apellido', 'Telefono', 'Email']
                self.display_query_results(results, columns)
                vaccine_window.destroy()
            except (ValueError, IndexError):
                messagebox.showwarning("Advertencia", "Seleccione una vacuna válida")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error en consulta: {err}")
        
        tk.Button(vaccine_window, text="Consultar", command=execute_query,
                 bg="#3498db", fg="white", width=15).pack(pady=10)
    
    def run(self):
        """Ejecutar la aplicación"""
        self.root.mainloop()

# Ejecutar el sistema
if __name__ == "__main__":
    app = VacunacionSystem()
    app.run()