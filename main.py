import tkinter as tk
from tkinter import ttk, messagebox
import random
import matplotlib.pyplot as plt # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg # type: ignore
import numpy as np # type: ignore

class TrafficSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Tráfico de Ensenada")
        self.root.geometry("1000x700")
        self.root.resizable(True, True)
        
        # Crear el notebook para múltiples pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True)
        
        # Crear las pestañas
        self.start_frame = tk.Frame(self.notebook)
        self.main_frame = tk.Frame(self.notebook)
        self.reports_frame = tk.Frame(self.notebook)
        self.about_frame = tk.Frame(self.notebook)
        
        self.notebook.add(self.start_frame, text="Inicio")
        self.notebook.add(self.main_frame, text="Simulación")
        self.notebook.add(self.reports_frame, text="Reportes")
        self.notebook.add(self.about_frame, text="Acerca de")
        
        # Configurar las pestañas
        self.setup_start_frame()
        self.setup_main_frame()
        self.setup_reports_frame()
        self.setup_about_frame()
        
        # Variables para los resultados de la simulación
        self.simulation_results = None
    
    def setup_start_frame(self):
        # Frame para el logo y título
        logo_frame = tk.Frame(self.start_frame)
        logo_frame.pack(pady=50)
        
        # Logo (placeholder)
        logo_label = tk.Label(logo_frame, text="🚦", font=("Arial", 80))
        logo_label.pack()
        
        # Título del sistema
        title_label = tk.Label(logo_frame, text="Sistema de Simulación de Tráfico\nEnsenada", 
                               font=("Arial", 24, "bold"), justify="center")
        title_label.pack(pady=20)
        
        # Frame para botones
        button_frame = tk.Frame(self.start_frame)
        button_frame.pack(pady=30)
        
        # Botones principales
        btn_width = 20
        btn_height = 2
        font_size = 12
        
        simulation_btn = tk.Button(button_frame, text="Iniciar Simulación", 
                                  width=btn_width, height=btn_height, 
                                  font=("Arial", font_size),
                                  command=lambda: self.notebook.select(self.main_frame))
        simulation_btn.pack(pady=10)
        
        reports_btn = tk.Button(button_frame, text="Ver Reportes", 
                               width=btn_width, height=btn_height, 
                               font=("Arial", font_size),
                               command=lambda: self.notebook.select(self.reports_frame))
        reports_btn.pack(pady=10)
        
        about_btn = tk.Button(button_frame, text="Acerca de...", 
                             width=btn_width, height=btn_height, 
                             font=("Arial", font_size),
                             command=lambda: self.notebook.select(self.about_frame))
        about_btn.pack(pady=10)
    
    def setup_main_frame(self):
        # Dividir en dos partes: mapa y controles
        main_paned = tk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Panel izquierdo: Mapa de Ensenada
        map_frame = tk.Frame(main_paned, bg="white", width=500)
        main_paned.add(map_frame, width=500)
        
        map_title = tk.Label(map_frame, text="Mapa de Intersecciones de Ensenada", 
                            font=("Arial", 14, "bold"), bg="white")
        map_title.pack(pady=10)
        
        # Canvas para el mapa
        self.map_canvas = tk.Canvas(map_frame, bg="white", width=480, height=500)
        self.map_canvas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Dibujar un mapa simple
        self.draw_map()
        
        # Panel derecho: Controles y resultados
        control_frame = tk.Frame(main_paned)
        main_paned.add(control_frame)
        
        # Título de parámetros
        params_label = tk.Label(control_frame, text="Parámetros de Simulación", 
                               font=("Arial", 14, "bold"))
        params_label.pack(pady=(20, 10))
        
        # Frame para los parámetros
        params_frame = tk.LabelFrame(control_frame, text="Configuración")
        params_frame.pack(padx=20, pady=10, fill="x")
        
        # Frecuencia semafórica
        tk.Label(params_frame, text="Frecuencia semafórica (segundos):").grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.traffic_light_var = tk.IntVar(value=30)
        traffic_light_scale = tk.Scale(params_frame, from_=10, to=120, orient="horizontal", 
                                       variable=self.traffic_light_var, length=200)
        traffic_light_scale.grid(row=0, column=1, padx=10, pady=5)
        
        # Cantidad de vehículos por carril
        tk.Label(params_frame, text="Vehículos por carril (por minuto):").grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.vehicles_var = tk.IntVar(value=20)
        vehicles_scale = tk.Scale(params_frame, from_=5, to=60, orient="horizontal", 
                                 variable=self.vehicles_var, length=200)
        vehicles_scale.grid(row=1, column=1, padx=10, pady=5)
        
        # Horario
        tk.Label(params_frame, text="Horario:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.time_var = tk.StringVar(value="Hora pico")
        time_combo = ttk.Combobox(params_frame, textvariable=self.time_var, 
                                  values=["Hora pico", "Hora normal", "Hora baja"])
        time_combo.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
        
        # Botón de ejecutar simulación
        execute_btn = tk.Button(control_frame, text="Ejecutar Simulación", 
                               font=("Arial", 12, "bold"),
                               bg="#4CAF50", fg="white", 
                               command=self.run_simulation,
                               height=2)
        execute_btn.pack(pady=20, padx=20, fill="x")
        
        # Frame para resultados
        self.results_frame = tk.LabelFrame(control_frame, text="Resultados de la Simulación")
        self.results_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        self.results_text = tk.Text(self.results_frame, height=10, width=40, state="disabled")
        self.results_text.pack(padx=10, pady=10, fill="both", expand=True)
    
    def setup_reports_frame(self):
        # Título
        title_label = tk.Label(self.reports_frame, text="Reportes de Simulaciones", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # Frame para gráficos
        charts_frame = tk.Frame(self.reports_frame)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Crear un espacio para los gráficos usando matplotlib
        self.fig, (self.ax1, self.ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.fig.subplots_adjust(wspace=0.3)
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=charts_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Inicializar los gráficos
        self.ax1.set_title('Tiempo de Espera por Intersección')
        self.ax1.set_xlabel('Intersección')
        self.ax1.set_ylabel('Tiempo (segundos)')
        
        self.ax2.set_title('Flujo Vehicular')
        self.ax2.set_xlabel('Hora')
        self.ax2.set_ylabel('Vehículos/minuto')
        
        # Botón para generar nuevo reporte
        gen_report_btn = tk.Button(self.reports_frame, text="Generar Nuevo Reporte", 
                                  command=self.generate_report)
        gen_report_btn.pack(pady=20)
    def setup_about_frame(self):
        # Título
        title_label = tk.Label(self.about_frame, text="Acerca del Simulador", 
                              font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # Información sobre el sistema
        info_text = """
        Sistema de Simulación de Tráfico para Ensenada por Alumnos del instituto Tecnológico de Ensenada.
        Desarrollado por: [Irma Rivera, Annette Zurita, Luis Moneda, Jose Juan Padilla]
        
        Versión 1.0
        
        Este software permite configurar y simular el flujo vehicular
        en las principales intersecciones de la ciudad de Ensenada.
        
        Características principales:
        - Simulación de flujo vehicular
        - Análisis de tiempos de espera
        - Recomendaciones para optimización de semáforos
        - Visualización de zonas críticas de congestión
        
        Desarrollado como proyecto de demostración.
        """
        
        info_label = tk.Label(self.about_frame, text=info_text, justify="left",
                             font=("Arial", 12), padx=30, pady=20)
        info_label.pack()
    
    def draw_map(self):
        # Limpiar el canvas
        self.map_canvas.delete("all")
        
        # Definir dimensiones del canvas
        width = self.map_canvas.winfo_width()
        height = self.map_canvas.winfo_height()
        
        # Si el canvas aún no tiene tamaño definido, usar valores predeterminados
        if width <= 1:
            width = 480
        if height <= 1:
            height = 500
        
        # Dibujar calles principales (líneas negras)
        # Calle horizontal principal
        self.map_canvas.create_line(50, height/2, width-50, height/2, width=8, fill="gray")
        self.map_canvas.create_text(width-40, height/2-10, text="Reforma", font=("Arial", 8))
        
        # Calle vertical principal
        self.map_canvas.create_line(width/2, 50, width/2, height-50, width=8, fill="gray")
        self.map_canvas.create_text(width/2+10, 30, text="Blvd. Costero", font=("Arial", 8))
        
        # Calles secundarias
        self.map_canvas.create_line(width/4, 80, width/4, height-80, width=5, fill="gray")
        self.map_canvas.create_text(width/4+10, 60, text="Ryerson", font=("Arial", 8))
        
        self.map_canvas.create_line(3*width/4, 80, 3*width/4, height-80, width=5, fill="gray")
        self.map_canvas.create_text(3*width/4+10, 60, text="Miramar", font=("Arial", 8))
        
        self.map_canvas.create_line(80, height/4, width-80, height/4, width=5, fill="gray")
        self.map_canvas.create_text(width-60, height/4-10, text="López Mateos", font=("Arial", 8))
        
        self.map_canvas.create_line(80, 3*height/4, width-80, 3*height/4, width=5, fill="gray")
        self.map_canvas.create_text(width-60, 3*height/4-10, text="Juárez", font=("Arial", 8))
        
        # Dibujar intersecciones (círculos rojos)
        radius = 8
        # Intersección principal
        self.map_canvas.create_oval(width/2-radius, height/2-radius, 
                                   width/2+radius, height/2+radius, 
                                   fill="red", tags="intersection")
        
        # Otras intersecciones
        self.map_canvas.create_oval(width/4-radius, height/2-radius, 
                                   width/4+radius, height/2+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(3*width/4-radius, height/2-radius, 
                                   3*width/4+radius, height/2+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(width/2-radius, height/4-radius, 
                                   width/2+radius, height/4+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(width/2-radius, 3*height/4-radius, 
                                   width/2+radius, 3*height/4+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(width/4-radius, height/4-radius, 
                                   width/4+radius, height/4+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(3*width/4-radius, height/4-radius, 
                                   3*width/4+radius, height/4+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(width/4-radius, 3*height/4-radius, 
                                   width/4+radius, 3*height/4+radius, 
                                   fill="red", tags="intersection")
        
        self.map_canvas.create_oval(3*width/4-radius, 3*height/4-radius, 
                                   3*width/4+radius, 3*height/4+radius, 
                                   fill="red", tags="intersection")
    
    def run_simulation(self):
        """Ejecuta la simulación con los parámetros configurados"""
        # Obtener los valores de los parámetros
        traffic_light_frequency = self.traffic_light_var.get()
        vehicles_per_lane = self.vehicles_var.get()
        time_of_day = self.time_var.get()
        
        # Mostrar mensaje de que la simulación está en progreso
        messagebox.showinfo("Simulación", "Ejecutando simulación... Por favor espere.")
        
        # Simular proceso (con valores aleatorios para demostración)
        intersections = ["Reforma-Costero", "Reforma-Ryerson", "Reforma-Miramar", 
                        "López Mateos-Costero", "Juárez-Costero"]
        
        # Calcular tiempos de espera (simulados)
        base_wait_time = traffic_light_frequency / 2
        
        # Modificar según hora del día
        modifier = 1.0
        if time_of_day == "Hora pico":
            modifier = 1.5
        elif time_of_day == "Hora baja":
            modifier = 0.6
        
        # Calcular valores dependiendo de los parámetros
        wait_times = {}
        flow_rates = {}
        congestion_levels = {}
        
        for intersection in intersections:
            # El tiempo de espera depende de la frecuencia semafórica y cantidad de vehículos
            random_factor = random.uniform(0.8, 1.2)
            wait_time = base_wait_time * (1 + (vehicles_per_lane / 60)) * modifier * random_factor
            wait_times[intersection] = round(wait_time, 1)
            
            # Flujo vehicular (vehículos que pasan por minuto)
            flow_capacity = random.randint(40, 60)  # Capacidad base de la intersección
            actual_flow = min(vehicles_per_lane * modifier * random.uniform(0.9, 1.1), flow_capacity)
            flow_rates[intersection] = round(actual_flow, 1)
            
            # Nivel de congestión (0-100%)
            congestion = min(100, (vehicles_per_lane / flow_capacity) * 100 * modifier)
            congestion_levels[intersection] = round(congestion, 1)
        
        # Actualizar los resultados
        self.simulation_results = {
            "wait_times": wait_times,
            "flow_rates": flow_rates,
            "congestion_levels": congestion_levels,
            "parameters": {
                "traffic_light_frequency": traffic_light_frequency,
                "vehicles_per_lane": vehicles_per_lane,
                "time_of_day": time_of_day
            }
        }
        
        # Mostrar resultados
        self.display_results()
        
        # Actualizar gráficos en la pestaña de reportes
        self.update_charts()
        
        # Colorear el mapa según la congestión
        self.update_map_colors()
    
    def display_results(self):
        """Muestra los resultados en el área de texto"""
        if not self.simulation_results:
            return
        
        # Habilitar el widget Text para edición
        self.results_text.config(state="normal")
        
        # Limpiar el contenido anterior
        self.results_text.delete(1.0, tk.END)
        
        # Encontrar la intersección más congestionada
        most_congested = max(self.simulation_results["congestion_levels"], 
                            key=self.simulation_results["congestion_levels"].get)
        
        # Calcular promedios
        avg_wait = sum(self.simulation_results["wait_times"].values()) / len(self.simulation_results["wait_times"])
        avg_flow = sum(self.simulation_results["flow_rates"].values()) / len(self.simulation_results["flow_rates"])
        
        # Generar recomendaciones
        if avg_wait > 30:
            recommendation = "Se recomienda reducir el tiempo de ciclo de semáforos."
        elif max(self.simulation_results["congestion_levels"].values()) > 80:
            recommendation = f"Considere rutas alternativas para {most_congested}."
        else:
            recommendation = "La configuración actual es adecuada para el flujo vehicular."
        
        # Insertar resultados en el widget Text
        self.results_text.insert(tk.END, "RESULTADOS DE LA SIMULACIÓN\n\n")
        self.results_text.insert(tk.END, f"Tiempo promedio de espera: {avg_wait:.1f} segundos\n")
        self.results_text.insert(tk.END, f"Flujo vehicular promedio: {avg_flow:.1f} vehículos/minuto\n\n")
        
        self.results_text.insert(tk.END, "Intersección más congestionada:\n")
        self.results_text.insert(tk.END, f"{most_congested} ({self.simulation_results['congestion_levels'][most_congested]}%)\n\n")
        
        self.results_text.insert(tk.END, "RECOMENDACIÓN:\n")
        self.results_text.insert(tk.END, recommendation)
        
        # Desactivar edición
        self.results_text.config(state="disabled")
    
    def update_charts(self):
        """Actualiza los gráficos en la pestaña de reportes"""
        if not self.simulation_results:
            return
        
        # Limpiar gráficos anteriores
        self.ax1.clear()
        self.ax2.clear()
        
        # Datos para las gráficas
        intersections = list(self.simulation_results["wait_times"].keys())
        wait_times = list(self.simulation_results["wait_times"].values())
        flow_rates = list(self.simulation_results["flow_rates"].values())
        
        # Gráfico de tiempos de espera
        self.ax1.bar(range(len(intersections)), wait_times, color='orange')
        self.ax1.set_title('Tiempo de Espera por Intersección')
        self.ax1.set_ylabel('Tiempo (segundos)')
        self.ax1.set_xticks(range(len(intersections)))
        self.ax1.set_xticklabels([i.split('-')[0] for i in intersections], rotation=45)
        
        # Gráfico de flujo vehicular
        self.ax2.bar(range(len(intersections)), flow_rates, color='blue')
        self.ax2.set_title('Flujo Vehicular por Intersección')
        self.ax2.set_ylabel('Vehículos/minuto')
        self.ax2.set_xticks(range(len(intersections)))
        self.ax2.set_xticklabels([i.split('-')[0] for i in intersections], rotation=45)
        
        # Ajustar diseño y redibujar
        self.fig.tight_layout()
        self.canvas.draw()
    
    def update_map_colors(self):
        """Actualiza los colores en el mapa según el nivel de congestión"""
        if not self.simulation_results:
            return
        
        # Obtener todas las intersecciones del mapa
        intersections = self.map_canvas.find_withtag("intersection")
        
        # Asignar colores según los niveles de congestión
        # (simplificado, en una aplicación real habría que mapear correctamente cada intersección)
        congestion_values = list(self.simulation_results["congestion_levels"].values())
        
        for i, intersection_id in enumerate(intersections):
            if i < len(congestion_values):
                congestion = congestion_values[i]
                
                # Definir color basado en la congestión
                if congestion < 40:
                    color = "green"
                elif congestion < 70:
                    color = "orange"
                else:
                    color = "red"
                
                # Actualizar el color de la intersección
                self.map_canvas.itemconfig(intersection_id, fill=color)
    
    def generate_report(self):
        """Genera un nuevo reporte aleatorio para demostración"""
        if not self.simulation_results:
            messagebox.showinfo("Reporte", "Por favor, ejecute primero una simulación en la pestaña principal.")
            self.notebook.select(self.main_frame)
            return
        
        # Generar datos de simulación para diferentes horas del día
        hours = ["7:00", "8:00", "9:00", "12:00", "14:00", "17:00", "18:00", "19:00"]
        flow_data = []
        
        # Simulamos el flujo a lo largo del día
        peak_hours = ["7:00", "8:00", "17:00", "18:00"]
        
        base_flow = self.simulation_results["parameters"]["vehicles_per_lane"]
        
        for hour in hours:
            if hour in peak_hours:
                flow = base_flow * random.uniform(1.3, 1.7)
            else:
                flow = base_flow * random.uniform(0.6, 1.0)
            flow_data.append(flow)
        
        # Limpiar el segundo gráfico y mostrar los datos por hora
        self.ax2.clear()
        self.ax2.plot(hours, flow_data, 'b-o')
        self.ax2.set_title('Flujo Vehicular a lo Largo del Día')
        self.ax2.set_xlabel('Hora')
        self.ax2.set_ylabel('Vehículos/minuto')
        self.ax2.grid(True)
        
        # Rotar las etiquetas para mejor visualización
        plt.setp(self.ax2.get_xticklabels(), rotation=45)
        
        # Ajustar diseño y redibujar
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Mostrar mensaje de confirmación
        messagebox.showinfo("Reporte", "Reporte generado exitosamente.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficSimulator(root)
    root.mainloop()