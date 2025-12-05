import json
import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk

from src.compiler.lexer.tokenizer import Tokenizer
from src.compiler.parser.parser import Parser
from src.runtime.run_program import Runtime


class URMExecutorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("URM Ejecutor de Codigo")
        self.root.geometry("1400x800")
        
        # Colores del tema oscuro
        bg_dark = "#000000"
        surface_dark = "#111111"
        border_dark = "#222222"
        text_primary = "#e5e5e5"
        text_secondary = "#a3a3a3"
        primary_color = "#3b82f6"
        red_color = "#dc2626"
        red_hover = "#b91c1c"
        
        # Configurar colores de fondo
        self.root.configure(bg=bg_dark)
        
        # Estilo personalizado
        style = ttk.Style()
        style.theme_use("clam")
        
        # Configurar estilos
        style.configure("Dark.TFrame", background=bg_dark)
        style.configure("Surface.TFrame", background=surface_dark, borderwidth=1, relief="solid")
        style.configure("Dark.TLabel", background=surface_dark, foreground=text_primary, font=("Space Grotesk", 10, "bold"))
        style.configure("Title.TLabel", background=bg_dark, foreground="#ffffff", font=("Space Grotesk", 14, "bold"))
        style.configure("Output.TLabel", background=bg_dark, foreground="#ffffff", font=("Space Grotesk", 12, "bold"))
        style.configure("Info.TLabel", background=surface_dark, foreground=text_secondary, font=("Consolas", 9))
        
        # Frame principal con fondo oscuro
        main_frame = tk.Frame(root, bg=bg_dark)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Header
        header_frame = tk.Frame(main_frame, bg=bg_dark, height=64)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Linea divisoria del header
        tk.Frame(header_frame, bg=border_dark, height=1).pack(side=tk.BOTTOM, fill=tk.X)
        
        title_label = tk.Label(
            header_frame, 
            text="URM Ejecutor de Codigo",
            bg=bg_dark,
            fg="#ffffff",
            font=("Space Grotesk", 14, "bold")
        )
        title_label.pack(side=tk.LEFT, padx=30, pady=20)
        
        # Contenedor principal
        content_frame = tk.Frame(main_frame, bg=bg_dark)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)
        
        # Frame con borde para los editores
        editors_frame = tk.Frame(content_frame, bg=surface_dark, highlightbackground=border_dark, highlightthickness=1)
        editors_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Padding interno
        inner_frame = tk.Frame(editors_frame, bg=surface_dark)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=24, pady=24)
        
        # Grid para los dos editores
        inner_frame.grid_columnconfigure(0, weight=1)
        inner_frame.grid_columnconfigure(1, weight=1)
        inner_frame.grid_rowconfigure(1, weight=1)
        
        # Label: Codigo de entrada URM
        code_label = tk.Label(
            inner_frame,
            text="Codigo de entrada URM",
            bg=surface_dark,
            fg=text_primary,
            font=("Space Grotesk", 10, "bold")
        )
        code_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 12), pady=(0, 8))
        
        # Editor de codigo
        self.code_input = scrolledtext.ScrolledText(
            inner_frame,
            width=40,
            height=15,
            font=("Consolas", 11),
            bg=bg_dark,
            fg=text_primary,
            insertbackground=text_primary,
            selectbackground=primary_color,
            selectforeground="#ffffff",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=border_dark,
            highlightcolor=primary_color
        )
        self.code_input.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 12))
        self.code_input.insert("1.0", "Z(1)\nS(1)\nJ(1,1,3)")
        
        # Label: Traza de Ejecucion
        trace_label = tk.Label(
            inner_frame,
            text="Traza de Ejecucion",
            bg=surface_dark,
            fg=text_primary,
            font=("Space Grotesk", 10, "bold")
        )
        trace_label.grid(row=0, column=1, sticky=tk.W, padx=(12, 0), pady=(0, 8))
        
        # Traza de ejecucion
        self.trace_output = scrolledtext.ScrolledText(
            inner_frame,
            width=40,
            height=15,
            font=("Consolas", 9),
            bg=bg_dark,
            fg=text_secondary,
            state="disabled",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=border_dark,
            highlightcolor=primary_color
        )
        self.trace_output.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(12, 0))
        
        # Controles
        controls_frame = tk.Frame(editors_frame, bg=surface_dark)
        controls_frame.pack(fill=tk.X, padx=24, pady=(0, 24))
        
        # Entrada del Programa
        input_label = tk.Label(
            controls_frame,
            text="Entrada del Programa",
            bg=surface_dark,
            fg=text_primary,
            font=("Space Grotesk", 9, "bold")
        )
        input_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=(0, 8))
        
        self.input_entry = tk.Entry(
            controls_frame,
            width=20,
            font=("Consolas", 10),
            bg=bg_dark,
            fg=text_primary,
            insertbackground=text_primary,
            selectbackground=primary_color,
            selectforeground="#ffffff",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=border_dark,
            highlightcolor=primary_color
        )
        self.input_entry.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        self.input_entry.insert(0, "[5, 2, 0]")
        
        # Max Iteraciones
        max_label = tk.Label(
            controls_frame,
            text="Max Iteraciones",
            bg=surface_dark,
            fg=text_primary,
            font=("Space Grotesk", 9, "bold")
        )
        max_label.grid(row=0, column=1, sticky=tk.W, padx=(10, 10), pady=(0, 8))
        
        self.max_iter_entry = tk.Entry(
            controls_frame,
            width=15,
            font=("Consolas", 10),
            bg=bg_dark,
            fg=text_primary,
            insertbackground=text_primary,
            selectbackground=primary_color,
            selectforeground="#ffffff",
            relief=tk.SOLID,
            borderwidth=1,
            highlightthickness=1,
            highlightbackground=border_dark,
            highlightcolor=primary_color
        )
        self.max_iter_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 10))
        self.max_iter_entry.insert(0, "1000")
        
        # Boton Ejecutar
        self.execute_btn = tk.Button(
            controls_frame,
            text="▶ Ejecutar",
            command=self.execute_program,
            bg=red_color,
            fg="#ffffff",
            activebackground=red_hover,
            activeforeground="#ffffff",
            font=("Space Grotesk", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=20,
            pady=8,
            borderwidth=0
        )
        self.execute_btn.grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        
        controls_frame.grid_columnconfigure(0, weight=1)
        controls_frame.grid_columnconfigure(1, weight=1)
        
        # Salida de Ejecucion
        output_title = tk.Label(
            content_frame,
            text="Salida de Ejecucion",
            bg=bg_dark,
            fg="#ffffff",
            font=("Space Grotesk", 13, "bold")
        )
        output_title.pack(anchor=tk.W, pady=(10, 12))
        
        # Frame de salida
        self.output_frame = tk.Frame(
            content_frame,
            bg=surface_dark,
            highlightbackground=border_dark,
            highlightthickness=1
        )
        self.output_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Contenido de salida
        output_content = tk.Frame(self.output_frame, bg=surface_dark)
        output_content.pack(fill=tk.X, padx=16, pady=16)
        
        info_icon = tk.Label(
            output_content,
            text="ℹ",
            bg=surface_dark,
            fg=text_secondary,
            font=("Arial", 14)
        )
        info_icon.pack(side=tk.LEFT, padx=(0, 12))
        
        self.output_label = tk.Label(
            output_content,
            text="Los resultados se mostraran aqui despues de la ejecucion.",
            bg=surface_dark,
            fg=text_secondary,
            font=("Consolas", 10),
            anchor=tk.W,
            justify=tk.LEFT
        )
        self.output_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

    def execute_program(self):
        try:
            # limpiamos trace
            self.trace_output.config(state="normal")
            self.trace_output.delete("1.0", tk.END)
            self.trace_output.config(state="disabled")

            # obtenemos codigo
            code = self.code_input.get("1.0", tk.END).strip()
            if not code:
                messagebox.showerror("Error", "Por favor ingresa codigo URM")
                return

            # obtenemos entrada
            input_str = self.input_entry.get().strip()
            try:
                program_input = json.loads(input_str)
                if not isinstance(program_input, list):
                    raise ValueError()
            except ValueError:
                messagebox.showerror(
                    "Error", "La entrada debe ser una lista valida, ej: [5, 2, 0]"
                )
                return

            # obtenemos max iteraciones
            try:
                max_iter = int(self.max_iter_entry.get())
                if max_iter <= 0:
                    raise ValueError()
            except ValueError:
                messagebox.showerror(
                    "Error", "Las iteraciones maximas deben ser un numero positivo"
                )
                return

            # tokenizamos el codigo
            tokenizer = Tokenizer()
            tokenizer.load_program(code.split("\n"))
            tokens = tokenizer.tokenize_program()

            if not tokens:
                messagebox.showerror(
                    "Error", "No se pudieron generar tokens del codigo"
                )
                return

            # parseamos el codigo
            parser = Parser(tokens)
            ast = parser.generate_AST()

            if isinstance(ast, str):  # Error
                messagebox.showerror("Error de Sintaxis", ast)
                return

            # ejecutamos codigo
            runtime = Runtime()
            result, trace, steps = runtime.execute_program(ast, program_input, max_iter)

            # Mostrar traza
            self.trace_output.config(state="normal")
            self.trace_output.insert("1.0", "\n".join(trace))
            self.trace_output.config(state="disabled")

            # Mostrar resultado
            if steps and steps >= max_iter:
                output_text = (
                    f"LIMITE ALCANZADO\n"
                    f"Resultado: {result}\n"
                    f"Pasos ejecutados: {steps}\n"
                    f"Estado: Terminado por limite de iteraciones"
                )
                self.output_label.config(foreground="orange")
            else:
                output_text = (
                    f"EJECUCION EXITOSA\n"
                    f"Resultado: {result}\n"
                    f"Pasos ejecutados: {steps or 'N/A'}\n"
                    f"Estado: Completado"
                )
                self.output_label.config(foreground="green")

            self.output_label.config(text=output_text)

        except Exception as e:
            messagebox.showerror("Error", f"Error durante la ejecucion:\n{str(e)}")


if __name__ == "__main__":
    root = tk.Tk()
    app = URMExecutorGUI(root)
    root.mainloop()
