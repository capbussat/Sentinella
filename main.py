import flet as ft
import asyncio
from connection import SSHService

# Falta llegir la llista de IPs


# async perquè conté await
async def main(page: ft.Page):

    # hardcoded parameter
    internet = True

    # Theme
    page.theme_mode = ft.ThemeMode.LIGHT
    page.theme = ft.Theme(use_material3=True)
    # Set the title of the application window
    page.title = "Distributed Uncomplicated FireWall"
    page.window.width = 600
    page.window.height = 400

    @ft.control
    class CtrlSwitch(ft.Switch):
        expand: int = 1

    @ft.control
    class NetSwitch(CtrlSwitch):
        value=True,

    class ServicesSwitch(CtrlSwitch):
        expand: int = 2

    # Create a text widget to display a status  message
    status_text = ft.Text("Status OK", bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)

    def display_status(text):
        status_text.value = text
        print(text)

    # Define an event handler for the button click event    
    def change_internet(e):
        value = e.control.value
        if value is False:
            display_status("Internet is OFF")
            
        else:
            display_status("Internet is ON")
            
    def dhcp_status(e):
        value = e.control.value
        if value is False:
            display_status("DHCP is OFF")
        else:
            display_status("DHCP is ON")

    def dns_status(e):
        value = e.control.value
        if value is False:
            display_status("DNS is OFF")
            
        else:
            display_status("DNS is ON")

    def set_browser_policies(e):
        display_status("Run Browser with policies")
        page.update()
        ip = "10.2.197.16"
        new = SSHService(ip)
        new.run("./start-chromium-kiosk.sh")
        print(new)  
        

    def set_firewall_rules(e):
        display_status("Set Firewall rules")

    async def close_app(e):
        # Aquí volem actualitzar la finestra abans del final
        display_status("Closing app in a second...")
        page.update()
        # pausa
        await asyncio.sleep(3)
        await page.window.destroy() # també és coroutine


    async def check_ssh(e):
        display_status("Testing SSH...")
        page.update()
        ip = "10.2.197.16"
        new = SSHService(ip)
        new.run("pwd")
        print(new)  
        display_status("SSH is OK")
        page.update()
        

    # Create a button widget with an associated click event handler
    close_button = ft.Button("Close App",on_click=close_app)
    check_ssh_button = ft.Button("Test SSH",on_click=check_ssh)

    # Add the greeting text and button to the page layout
    page.add(
        ft.Container(
            height = 350,
            width = 600,
            border_radius=ft.BorderRadius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(
                    controls=[
                        NetSwitch(label="Internet", value=True,on_change=change_internet),
                        ]
                    ),
                    ft.Divider(height=12, thickness=3),
                    ft.Row(
                    controls=[
                            ServicesSwitch(label="DHCP",value=True,on_change=dhcp_status),
                            ServicesSwitch(label="DNS",value=True,on_change=dns_status),
                            ServicesSwitch(label="SSH",value=False, disabled=True),
                            ServicesSwitch(label="Veyon",value=True, disabled=True),
                        ]
                    ),
                    ft.Divider(height=24, thickness=3),
                    ft.Row(
                        controls=[
                            ft.Chip(
                                    label="Run Browser with policies",
                                    leading=ft.Icon(ft.Icons.WEB),
                                    autofocus=True,
                                    bgcolor=ft.Colors.WHITE_60,
                                    label_text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                    on_click=set_browser_policies,
                                    ),
                            ft.Chip(
                                    label="Set Firewall rules",
                                    leading=ft.Icon(ft.Icons.WEB),
                                    autofocus=True,
                                    bgcolor=ft.Colors.GREEN_500,
                                    label_text_style=ft.TextStyle(color=ft.Colors.BLACK),
                                    on_click=set_firewall_rules,
                                    )
                            ]
                    ),
                    ft.Divider(height=24, thickness=3),
                    ft.Row(
                        controls=[
                                check_ssh_button, close_button
                            ]
                    ),
                    ft.Row(
                        controls=[
                                status_text
                            ]
                    ),
                     ft.Row(
                        controls=[
                                ft.Text(value="App ports can not be disabled on clients!")
                            ],
                        alignment=ft.Alignment.TOP_RIGHT,
                    ),
                ]
            )
        )
    )

   
   

# Start the Flet application by specifying the main function as the target
# ft.app is deprecated
ft.run(main)