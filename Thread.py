#!/usr/bin/env python3

"""
Flet + Fabric multithreaded SSH executor.

Requirements:
    pip install flet fabric

Run:
    python app.py
"""

import threading
import time

import flet as ft
from fabric import Connection
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------

SSH_USER = "admin"
SSH_TIMEOUT = 5
MAX_THREADS = 10

HOSTS = [
    "192.168.1.10",
    "192.168.1.11",
    "192.168.1.12",
    "192.168.1.13",
    "192.168.1.14",
    "192.168.1.15",
    "192.168.1.16",
    "192.168.1.17",
    "192.168.1.18",
    "192.168.1.19",
    "192.168.1.20",
    "192.168.1.21",
    "192.168.1.22",
    "192.168.1.23",
    "192.168.1.24",
    "192.168.1.25",
    "192.168.1.26",
    "192.168.1.27",
    "192.168.1.28",
    "192.168.1.29",
    "192.168.1.30",
    "192.168.1.31",
    "192.168.1.32",
    "192.168.1.33",
    "192.168.1.34",
    "192.168.1.35",
    "192.168.1.36",
    "192.168.1.37",
    "192.168.1.38",
    "192.168.1.39",
]


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

    page.title = "Fabric SSH Executor"
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
        expand=True,
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

    for host in HOSTS:

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
        border=ft.border.all(1),
        padding=10,
        width=250,
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

    def run_commands():

        selected_hosts = [
            cb.label
            for cb in host_checkboxes
            if cb.value
        ]

        command = txt_command.value.strip()

        if not selected_hosts:
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

    def btn_execute_click(e):

        threading.Thread(
            target=run_commands,
            daemon=True,
        ).start()

    def btn_select_all_click(e):

        for cb in host_checkboxes:
            cb.value = True

        page.update()

    def btn_unselect_all_click(e):

        for cb in host_checkboxes:
            cb.value = False

        page.update()

    # -------------------------------------------------------------
    # BUTTONS
    # -------------------------------------------------------------

    btn_execute = ft.ElevatedButton(
        text="Execute",
        icon=ft.Icons.PLAY_ARROW,
        on_click=btn_execute_click,
    )

    btn_select_all = ft.OutlinedButton(
        text="Select all",
        on_click=btn_select_all_click,
    )

    btn_unselect_all = ft.OutlinedButton(
        text="Unselect all",
        on_click=btn_unselect_all_click,
    )

    # -------------------------------------------------------------
    # LAYOUT
    # -------------------------------------------------------------

    left_panel = ft.Column(
        [
            ft.Text(
                "Hosts",
                size=20,
                weight=ft.FontWeight.BOLD,
            ),
            hosts_container,
        ]
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
            ft.Row(
                [
                    btn_select_all,
                    btn_unselect_all,
                ]
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


# ---------------------------------------------------------------------
# START
# ---------------------------------------------------------------------

ft.app(target=main)