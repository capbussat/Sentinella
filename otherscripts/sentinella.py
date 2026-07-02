#!/usr/bin/env python3
# Sentinella amb Flet
# És una aplicació que queda aparcada, perquè he seguit en el fitxer senti.py, que és el que s'executa en el arrencada del sistema. Aquesta aplicació és només per a fer proves i per a desenvolupar.

"""
Flet + Fabric multithreaded SSH executor.

Requirements:
    pip install flet fabric

Run:
    python3 sentinella.py
"""
import flet as ft
from fabric import Connection
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from settings import settings

# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

SSH_USER = settings.settings["ssh_user"]
SSH_TIMEOUT =  settings.settings["ssh_timeout"]
MAX_THREADS = settings.settings["max_threads"]

def load_hosts_from_file(filename="hosts") -> list[str]:

    file_path = Path(filename)
    print(Path.cwd())
    print(file_path.resolve())
    
    if not file_path.exists():
        print(f"[ERROR] File not found: {filename}")
        return []

    hosts = []

    with open(file_path, "r", encoding="utf-8") as f:

        for line in f:

            line = line.strip()

            # Ignore empty lines
            if not line:
                continue

            # Ignore comments
            if line.startswith("#"):
                continue

            hosts.append(line)

    return hosts

# ---------------------------------------------------------------------
# SSH EXECUTION
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
# GUI
# ---------------------------------------------------------------------

def main(page: ft.Page):

    try:    

        page.title = "Sentinella SSH GUI"
        page.window_width = 1200
        page.window_height = 800
        page.scroll = ft.ScrollMode.AUTO

        # -------------------------------------------------------------
        # COMMAND FIELD
        # -------------------------------------------------------------

        txt_command = ft.TextField(
            label="Bash command",
            value="hostname",
            multiline=False,
        )

        # -------------------------------------------------------------
        # RESULT AREA
        # -------------------------------------------------------------

        result_column = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        # -------------------------------------------------------------
        # HOST CHECKBOXES
        # -------------------------------------------------------------

        host_checkboxes = []

        try:
            hosts_list= load_hosts_from_file()
        except Exception as e:
            hosts_list = []

        for host in hosts_list:

            cb = ft.Checkbox(
                label=host,
                value=True,
            )

            host_checkboxes.append(cb)
        
        hosts_container = ft.Container(
            content=ft.Column(
                controls=host_checkboxes,
                scroll=ft.ScrollMode.AUTO,
            ),
            border=ft.Border.all(width=1, color=ft.Colors.OUTLINE),
            padding=10,
            width=200,
            height=600,
        )

        # -------------------------------------------------------------
        # UI HELPERS
        # -------------------------------------------------------------

        def add_result(data):

            success = data["success"]

            indicator_color = "green" if success else "red"

            indicator = ft.Container(
                width=16,
                height=16,
                border_radius=100,
                bgcolor=indicator_color,
            )

            output_text = data["stdout"] if success else data["stderr"]

            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    indicator,
                                    ft.Text(
                                        data["host"],
                                        weight=ft.FontWeight.BOLD,
                                        size=16,
                                    ),
                                ]
                            ),
                            ft.Text(
                                output_text,
                                selectable=True,
                                font_family="monospace",
                            ),
                        ]
                    ),
                )
            )

            result_column.controls.append(card)
            page.update()

        # -------------------------------------------------------------
        # EXECUTION THREAD
        # -------------------------------------------------------------


        def run_commands(command: str):

            selected_hosts = [
                cb.label
                for cb in host_checkboxes
                if cb.value
            ]

            # command = txt_command.value.strip()

            if not selected_hosts:
                data = {
                    "host": "---",
                    "success": False,
                    "stdout": "",
                    "stderr": "Warning: Selecciona un host de la llista o falta el fitxer hosts.",
                }
    
                add_result(data)
                return

            if not command:
                return

            result_column.controls.clear()
            page.update()

            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:

                futures = {
                    executor.submit(
                        execute_command,
                        host,
                        command
                    ): host
                    for host in selected_hosts
                }

                for future in as_completed(futures):

                    data = future.result()

                    page.run_thread(
                        lambda d=data: add_result(d)
                    )

        # -------------------------------------------------------------
        # BUTTON EVENTS
        # -------------------------------------------------------------

        def btn_dynamic_click(e):
            
            ### Dynamic button
            
            command = e.control.data
            print(command)
            threading.Thread(
                target=run_commands,
                args=(command),
                daemon=True,
            ).start()


        def btn_start_browser_click(e):
            
            ### Start browser with policies
            threading.Thread(
                target=run_commands,
                args=("DISPLAY=:0 nohup /usr/local/bin/start-chromium-kiosk.sh"),
                daemon=True,
            ).start()

        def btn_execute_click(e):
            threading.Thread(
                target=run_commands,
                args=(txt_command.value.strip()),
                daemon=True,
            ).start()

        def btn_select_all_click(e):
            if checkbox_select_all.value==True:
                for cb in host_checkboxes:
                    cb.value = True
            else:
                for cb in host_checkboxes:
                    cb.value = False
                
            page.update()


        def change_internet_click(e):
            value = e.control.value
            
            try:
                threading.Thread(
                    target=run_commands,
                    args=(command),
                    daemon=True,
                ).start()
            
            except Exception as expection:
                data = {
                    "host": "---",
                    "success": False,
                    "stderr": "Warning: no és possible canviar el valor.",
                }
                add_result(data)
                return

            if value is False:
                command = "./onsentinella.sh"
                data = {
                    "host": "---",
                    "success": True,
                    "stdout": "Info: Desconnectant internet.",
                }
                add_result(data)
            else:
                command = "./offsentinella.sh"
                data = {
                    "host": "---",
                    "success": True,
                    "stdout": "Info: Connectant internet.",
                }
                add_result(data)            

            
        # -------------------------------------------------------------
        # BUTTONS
        # -------------------------------------------------------------

        # load dynamic buttons
        buttons = []

        for button in settings.buttons:
            buttons.append(
                ft.Chip(
                    label=button["title"],
                    leading=ft.Icon(ft.Icons.WEB),
                    autofocus=True,
                    data=button["command"],
                    on_click=btn_dynamic_click,
                )
            )

        checkbox_select_all = ft.Checkbox(
                            label="Select all",
                            value=True,
                            on_change=btn_select_all_click
                        )

        btn_execute = ft.Button(
            content="Execute",
            # icon=ft.Icons.PLAY_ARROW,
            on_click=btn_execute_click,
        )

        btn_start_browser =  ft.Chip(
                                        label="Inicia el navegador",
                                        leading=ft.Icon(ft.Icons.WEB),
                                        autofocus=True,
                                        # bgcolor=ft.Colors.WHITE_60,
                                        # label_text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                        on_click=btn_start_browser_click,
        )
        

        switch_change_internet =  ft.Switch(
            label="Internet", 
            value=True,
            on_change=change_internet_click
        )

        # -------------------------------------------------------------
        # LAYOUT
        # -------------------------------------------------------------

        left_panel = ft.Column(
            [
                ft.Row(
                    [    ft.Text(
                            "Hosts",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                        ),
                        checkbox_select_all,
                    ]
                ),
                hosts_container,
            ],
            expand=True,
        )

        right_panel = ft.Column(
            [
                ft.Text(
                    "Command",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Row(
                    [
                        txt_command,
                        btn_execute,
                    ]
                ),
                ft.GridView(
                    width=480,
                    expand=True,
                    run_spacing=10,
                    runs_count=3,
                    spacing= 10,
                        controls=[ 
                            *buttons  # unpacking
                        ],
                ),
                ft.Divider(),
                ft.Text(
                    "Results",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                ),
                result_column,
            ],
            expand=True,
        )

        page.add(
            ft.Row(
                [
                    left_panel,
                    right_panel,
                ],
                expand=True,
                vertical_alignment=ft.CrossAxisAlignment.START,
            )
        )

        page.update()

    except Exception as e:

        page.add(
            ft.Text(
                f"ERROR: {e}",
                color="red"
            )
        )

        page.update()

        import traceback
        traceback.print_exc()

# ---------------------------------------------------------------------
# START
# ---------------------------------------------------------------------

ft.app(main)
