#!/usr/bin/env python3
# senti.py

import PIL._tkinter_finder #  important per pyinstaller
from fabric import Connection
import os
import yaml
from concurrent.futures import ThreadPoolExecutor, as_completed
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
# from tkinter import messagebox
from settings import settings
from hosts import  load_hosts_from_file

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

SSH_USER = settings.settings["ssh_user"]
SSH_TIMEOUT =  settings.settings["ssh_timeout"]
MAX_THREADS = settings.settings["max_threads"]

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
        self.geometry("1200x700")

        self.host_vars = {}

        self.create_widgets()
        self.load_hosts()
        self.create_dynamic_buttons()

    def create_dynamic_buttons(self):

        if not self.buttons_config:
            return

        for btn in self.buttons_config:

            title = btn.get("title", "Button")
            command = btn.get("command", "")
            style= btn.get("style","PRIMARY")

            ttk.Button(
                self.button_high_frame,
                text=title,
                command=lambda c=command, t=title: self.run_dynamic_command(t, c),
                bootstyle=style,
            ).pack(side=LEFT, padx=5)

    def run_dynamic_command(self, title, command):

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

        try:
            results = run_commands(selected_hosts, title, command)

            output = f"\n=== {title.upper()} ===\n\n"

            for r in results:
                output += f"{r['host']}: {r['success']}\n"

            self.append_result(output)

        except Exception as e:
            self.append_result(
                f"[ERROR {title}] {e}"
            )

    # def start_browser(self):

    #     selected_hosts = [
    #         host
    #         for host, var in self.host_vars.items()
    #         if var.get()
    #     ]

    #     if not selected_hosts:
    #         self.append_result(
    #             "[WARNING] Selecciona almenys un host."
    #         )
    #         return

    #     command = "DISPLAY=:0 nohup /usr/local/bin/start-chromium-kiosk.sh  >/dev/null 2>&1 &"
    #     try:

    #         results = run_commands(
    #             selected_hosts,
    #             "Inicia el navegador",
    #             command
    #         )

    #         output = "\n=== INICI NAVEGADOR ===\n\n"

    #         for r in results:

    #             output += (
    #                 f"{r['host']}: "
    #                 f"{r['success']}\n"
    #             )

    #         output += "\n"

    #         self.append_result(output)

    #     except Exception as e:

    #         self.append_result(
    #             f"[ERROR] {e}"
    #         )

    def create_widgets(self):

        title = ttk.Label(
            self,
            text="Llista de Hosts",
            font=("Helvetica", 16, "bold")
        )
        
        title.pack(
            anchor="w",
            fill=X,
            padx=10,
            pady=10
        )

        self.button_high_frame = ttk.Frame(self)
        self.button_high_frame.pack(fill=X, padx=10, pady=10)

        # Frame principal esquerra/dreta
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(
            fill=BOTH,
            expand=True,
            padx=10,
            pady=10
        )

        # Hosts
        self.frame_hosts = ttk.LabelFrame(
            self.main_frame,
            text="Hosts"
        )
        self.frame_hosts.pack(
            side=LEFT,
            fill=BOTH,
            expand=True,
            padx=(0, 5)
        )

        # Resultats
        self.frame_results = ttk.LabelFrame(
            self.main_frame,
            text="Resultats"
        )
        
        self.frame_results.pack(
            side=RIGHT,
            fill=BOTH,
            expand=True,
            padx=(5, 0)
        )
        
        self.result_text = ttk.Text(
            self.frame_results,
            wrap="word"
        )

        self.result_text.pack(
            fill=BOTH,
            expand=True,
            padx=5,
            pady=5
        )

        self.result_text.configure(state="disabled")
        
        self.canvas = ttk.Canvas(self.frame_hosts)
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

        self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set
        )

        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.pack(side=RIGHT, fill=Y)

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

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(fill=X, padx=10, pady=10)

        ttk.Button(
            self.button_frame,
            text="Executar",
            bootstyle=DANGER,
            command=self.execute_selected_command
        ).pack(side=RIGHT, padx=5)

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

        # ttk.Button(
        #     self.button_frame,
        #     text="Inicia navegador",
        #     bootstyle=INFO,
        #     command=self.start_browser
        # ).pack(side=LEFT, padx=5)

    def execute_selected_command(self):

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

            output = ""
            for r in results:
                lines = [
                    f"[{r['host']}]",
                    f"SUCCESS: {r['success']}"
                ]
                
                if r['stdout']:
                    lines.extend([
                        "",
                        "STDOUT:",
                        r['stdout']
                    ])

                if r['stderr']:
                    lines.extend([
                        "",
                        "STDERR:",
                        r['stderr']
                    ])

                lines.append("-" * 40)
            
                output += "\n".join(lines) + "\n\n"
            
            self.result_text.configure(state="normal")
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", output)
            self.result_text.configure(state="disabled")

        except Exception as e:
            self.append_result(
                f"[ERROR] {e}"
            )

    def load_hosts(self):

        try:
            hosts = load_hosts_from_file()

            for host in hosts:

                var = ttk.BooleanVar(value=False)
                self.host_vars[host] = var

                chk = ttk.Checkbutton(
                    self.scrollable_frame,
                    text=host,
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

if __name__ == "__main__":
    app = SentinellaApp()
    app.mainloop()
