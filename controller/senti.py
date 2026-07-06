#!/usr/bin/env python3
# senti.py

"""
Python ttkbootstrap GUi for Sentinella scripts

pip install fabric ttkbootstrap

python3 senti.py

Install on teacher computer.
Edit hosts file.
Edit settings.yaml file and change user.
Requires SSH server on pupils conputers, accessible with SSK keys


"""

import PIL._tkinter_finder #  important pyinstaller
from fabric import Connection
import os, ctypes
from concurrent.futures import ThreadPoolExecutor, as_completed

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk  
# from tkinter import messagebox
from settings import settings
from hosts import  load_hosts_from_file

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

SSH_USER = settings.settings["ssh_user"]
SSH_TIMEOUT =  settings.settings["ssh_timeout"]
MAX_THREADS = settings.settings["max_threads"]
DISABLE_TIME = settings.settings["disable_time"]
COLUMN_GRID = 4

def  is_admin():
    try:
        admin = os.getuid() == 0
        return admin 
    except AttributeError:
        admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        return admin
    

# ---------------------------------------------------------------------
# SSH EXECUTION
# ---------------------------------------------------------------------

def execute_notification(host: str, title: str):

    command = (
        f'notify-send "Sentinella" '
        f'"Executant: {title}"'
    )

    execute_command(host, command)

# ---------------------------------------------------------------------

def execute_command(host: str, command: str):

    try:
        conn = Connection(
            host=host,
            user=SSH_USER,
            connect_timeout=SSH_TIMEOUT,
        )

        result = conn.run(
            command,
            hide=True,
            warn=True,
            timeout=SSH_TIMEOUT   # <-- TIMEOUT PER COMANDA
        )
        
        conn.close()

        return {
            "host": host,
            "success": result.ok,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
        }

    except Exception as e:

        return {
            "host": host,
            "success": False,
            "stdout": "",
            "stderr": str(e),
        }

# ---------------------------------------------------------------------
    # EXECUTION THREAD
# ---------------------------------------------------------------------


def run_commands(hosts, title: str, command: str):

    results = []

    with ThreadPoolExecutor(max_workers=MAX_THREADS * 2) as executor:

        # Llança notificacions
        for host in hosts:
            executor.submit(
                execute_notification,
                host,
                title
            )

        # Llança comandes
        command_futures = [
            executor.submit(
                execute_command,
                host,
                command
            )
            for host in hosts
        ]

        for future in as_completed(command_futures):
            results.append(future.result())
         

    return results

# ---------------------------------------------------------------------
#  Sentinella Window
# ---------------------------------------------------------------------

class SentinellaApp(ttk.Window):


    def __init__(self):
        super().__init__(themename="superhero")
        self.buttons_config = []

        self.buttons_config = settings.buttons

        self.title("Sentinella GUI")
        self.geometry("1200x800")

        self.host_vars = {}
        self.create_widgets()
        self.create_host_checkbuttons()
        self.create_dynamic_buttons()

    def create_dynamic_buttons(self):

        if not self.buttons_config:
            return

        for btn in self.buttons_config:

            title = btn.get("title", "Button")
            command = btn.get("command", "")
            style= btn.get("style","PRIMARY")

            button = ttk.Button(
                self.button_high_frame,
                text=title,
                bootstyle=style,
            )

            button.config(
                command=lambda b=button, c=command, t=title:
                    self.run_dynamic_command(b, t, c)
            )

            button.pack(side=LEFT, padx=5)

    def run_dynamic_command(self, button, title, command):

        selected_hosts = [
            host
            for host, var in self.host_vars.items()
            if var.get()
        ]

        if not selected_hosts:
            self.append_result(
                f"[{title}] No hi ha hosts seleccionats."
            )
            return

        button.config(state="disabled")
        self.update_idletasks()


        self.results = run_commands(selected_hosts, title, command)


        self.after(
            DISABLE_TIME,
            lambda b=button: b.config(state="normal")
        )

        self.show()
            
        output = f"\n=== {title.upper()} ===\n\n"
    
        if not self.results:
            output += ">>> No hi ha resultats\n"

        for r in self.results:
            if r.get('success'):
                output += f"{r['host']}: Ok  {r.get('stdout', '')} \n"
            else:
                output += f"{r['host']}: {r.get('stderr', '')}\n"
    
        self.append_result(output)
        

    def create_widgets(self):

        title = ttk.Label(
            self,
            text="Sentinella",
            font=("Helvetica", 16, "bold")
        )
        title.pack(anchor="w", fill=X, padx=10, pady=10)

        self.button_high_frame = ttk.Frame(self)
        self.button_high_frame.pack(fill=X, padx=10, pady=10)

        # =========================================================
        # CONTENIDOR PRINCIPAL (GRID 3 COLUMNES)
        # =========================================================
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=BOTH, expand=True, padx=10, pady=10)

        self.main_frame.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1, minsize=400)  # Hosts
        self.main_frame.columnconfigure(1, weight=2, minsize=400)  # Graella
        self.main_frame.columnconfigure(2, weight=0, minsize=400)  # Resultats

        # =========================================================
        # COL 0 → HOSTS
        # =========================================================
        self.frame_hosts = ttk.LabelFrame(self.main_frame, text="Hosts")
        self.frame_hosts.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Canvas scroll dins hosts
        self.canvas = tk.Canvas(self.frame_hosts)
        self.scrollbar = ttk.Scrollbar(
            self.frame_hosts,
            orient=VERTICAL,
            command=self.canvas.yview
        )
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self._canvas_window_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(
                self._canvas_window_id,
                width=e.width
            )
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # =========================================================
        # COL 1 → GRAELLA
        # =========================================================
        self.frame_grid = ttk.LabelFrame(self.main_frame, text="Graella")
        self.frame_grid.grid(row=0, column=1, sticky="nsew", padx=5)

        # IMPORTANT: fer-la responsive
        for i in range(COLUMN_GRID):
            self.frame_grid.columnconfigure(i, weight=1)

        # =========================================================
        # COL 2 → RESULTATS
        # =========================================================
        self.frame_results = ttk.LabelFrame(self.main_frame, text="Resultats")
        self.frame_results.grid(row=0, column=2, sticky="nsew", padx=(5, 0))

        self.result_text = tk.Text(self.frame_results, wrap="word")
        self.result_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.frame_results.rowconfigure(0, weight=1)
        self.frame_results.columnconfigure(0, weight=1)

        self.result_text.configure(state="disabled")

        # =========================================================
        # COMANDES ADMIN (fora del grid principal)
        # =========================================================
        if is_admin():
            command_frame = ttk.Frame(self)
            command_frame.pack(fill=X, padx=10, pady=5)

            ttk.Label(
                command_frame,
                text="Comanda Bash:",
                font=("Helvetica", 10, "bold")
            ).pack(anchor="w")

            self.command_entry = ttk.Entry(command_frame)
            self.command_entry.insert(0, "pwd")
            self.command_entry.pack(fill=X, pady=5)

            
            ttk.Button(
                command_frame,
                text="Executar",
                bootstyle=DANGER,
                command=self.execute_selected_command
            ).pack(side=LEFT, padx=5)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=X, padx=10, pady=10)

        ttk.Button(
            self.button_frame,
            text="Seleccionar tots",
            bootstyle=SUCCESS,
            command=self.select_all
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            self.button_frame,
            text="Deseleccionar tots",
            bootstyle=WARNING,
            command=self.unselect_all
        ).pack(side=LEFT, padx=5)

        ttk.Button(
            self.button_frame,
            text="Mostrar selecció",
            bootstyle=PRIMARY,
            command=self.show_selected
        ).pack(side=LEFT, padx=5)

    def execute_selected_command(self):
        if not is_admin():
            return
 
        command = self.command_entry.get().strip()

        if not command:
            self.append_result(
                "[WARNING] Has d'introduir una comanda Bash."
            )
            return

        selected_hosts = [
            host
            for host, var in self.host_vars.items()
            if var.get()
        ]

        if not selected_hosts:
            self.append_result(
               "[WARNING] Selecciona almenys un host."
            )
            return

        try:

            # problema
            results = run_commands(selected_hosts, "Comanda BASH", command)

        except Exception as e:
            self.append_result(
                f"[ERROR] {e}"
            )

    def create_host_checkbuttons(self):

        try:
            self.hosts = load_hosts_from_file()
            

            for host in self.hosts:

                var = ttk.BooleanVar(value=False)
                self.host_vars[host.ip] = var

                chk = ttk.Checkbutton(
                    self.scrollable_frame,
                    text= host.label + " - " + host.ip,
                    variable=var,
                    bootstyle="round-toggle"
                )

                chk.pack(
                    anchor="w",
                    padx=10,
                    pady=3
                )

        except FileNotFoundError:
            self.append_result(
                "[ERROR] No s'ha trobat el fitxer hosts"
            )

    def select_all(self):

        for var in self.host_vars.values():
            var.set(True)

    def unselect_all(self):

        for var in self.host_vars.values():
            var.set(False)

    def show_selected(self):

        selected = [
            host
            for host, var in self.host_vars.items()
            if var.get()
        ]

        if selected:
            self.append_result(
                "Hosts seleccionats \n" .join(selected)
            )
        else:
            self.append_result(
                "Sense selecció. No hi ha cap host seleccionat."
            )

    def append_result(self, text):

        self.result_text.configure(state="normal")
        self.result_text.insert("end", text + "\n")
        self.result_text.see("end")
        self.result_text.configure(state="disabled")

    def get_host_label(self, ip_str):
        ip_to_label = {h.ip: h.label for h in self.hosts}
        return ip_to_label.get(ip_str)

    def show(self):

        # netejar graella anterior
        for widget in self.frame_grid.winfo_children():
            widget.destroy()

        cols = COLUMN_GRID
        if self.results:
            for i, result in enumerate(self.results):
                if result['success']:
                    style = 'success'
                else:
                    style= 'secondary'

                label = self.get_host_label( result['host'])

                btn = ttk.Button(
                    self.frame_grid,
                    text= label ,
                    bootstyle= style
                )

                row = i // cols
                col = i % cols
                btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3)

        # opcional: fer responsive
        for c in range(cols):
            self.frame_grid.columnconfigure(c, weight=1)


if __name__ == "__main__":
    app = SentinellaApp()
    app.mainloop()
