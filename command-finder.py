import tkinter as tk
from tkinter import ttk

class CommandApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Command Finder")
        self.geometry("800x600")
        self.configure(bg="#191c32")

        self.crear_widgets()

    def crear_widgets(self):
        # Etiqueta y menú desplegable para elegir el sistema operativo
        self.os_label = tk.Label(self, text="Elige un sistema operativo:", bg="#191c32", fg="white")
        self.os_label.pack(pady=10)

        self.os_var = tk.StringVar(value="windows")
        self.os_dropdown = ttk.Combobox(self, textvariable=self.os_var, values=["windows", "linux"], state="readonly")
        self.os_dropdown.pack()
        self.os_dropdown.bind("<<ComboboxSelected>>", self.actualizar_lista_comandos)

        # Cuadro de búsqueda de comandos
        self.search_var = tk.StringVar()
        self.search_box = tk.Entry(self, textvariable=self.search_var)
        self.search_box.pack(pady=10)
        self.search_box.bind("<KeyRelease>", self.buscar_comandos)

        # Lista de comandos
        self.command_listbox = tk.Listbox(self, bg="#373b54", fg="#d4d4d4", selectbackground="#5a5f7b", height=20)
        self.command_listbox.pack(pady=10, fill="both", expand=True)
        self.command_listbox.bind("<Motion>", self.mostrar_descripcion)
        self.command_listbox.bind("<<ListboxSelect>>", self.copiar_al_portapapeles)

        # Etiqueta para mostrar la descripción del comando
        self.description_label = tk.Label(self, text="", bg="#1e1e1e", fg="white", wraplength=700)
        self.description_label.pack(pady=10)

        # Cargar los comandos al iniciar
        self.cargar_comandos()

    def cargar_comandos(self):
        self.commands = {
            "windows": {
                "tasklist /v": "Mostrar información detallada de los procesos en ejecución.",
                "ipconfig /all": "Mostrar la configuración de red con información detallada.",
                "ping <direccion_ip>": "Hacer ping a una dirección IP específica.",
                "tracert <direccion_ip>": "Rastrear la ruta a una dirección IP.",
                "netstat -an": "Mostrar todas las conexiones de red y puertos en escucha.",
                "systeminfo": "Mostrar información del sistema.",
                "chkdsk": "Verificar la integridad de los discos duros.",
                "sfc /scannow": "Escanear y reparar archivos de sistema.",
                "diskpart": "Administrar discos, particiones y volúmenes.",
                "getmac": "Mostrar la dirección MAC de las interfaces de red.",
                "shutdown /s": "Apagar el equipo.",
                "shutdown /r": "Reiniciar el equipo.",
                "taskkill /im <nombre_proceso> /f": "Finalizar un proceso por su nombre.",
                "whoami": "Mostrar el nombre del usuario actual.",
                "hostname": "Mostrar el nombre del host del equipo.",
                "clip": "Copiar la salida de un comando al portapapeles.",
                "assoc": "Mostrar o modificar asociaciones de archivos.",
                "attrib": "Mostrar o cambiar atributos de archivos.",
                "color": "Cambiar el color de la consola.",
                "fc": "Comparar dos archivos y mostrar sus diferencias."
            },
            "linux": {
                "fdisk -l": "Mostrar la información de las particiones del disco.",
                "swapon -s": "Mostrar el estado de la memoria virtual.",
                "df -h": "Mostrar el uso del disco en formato legible.",
                "du -sh": "Mostrar el tamaño de un directorio en formato legible.",
                "free -m": "Mostrar el uso de la memoria en megabytes.",
                "top": "Mostrar los procesos en ejecución en tiempo real.",
                "ps aux": "Mostrar todos los procesos en ejecución.",
                "kill <pid>": "Terminar un proceso específico por su PID.",
                "reboot": "Reiniciar el sistema.",
                "shutdown -h now": "Apagar el sistema inmediatamente.",
                "mkdir <directorio>": "Crear un nuevo directorio.",
                "rmdir <directorio>": "Eliminar un directorio vacío.",
                "rm -rf <directorio>": "Eliminar un directorio y su contenido de forma recursiva.",
                "cp <origen> <destino>": "Copiar archivos o directorios.",
                "mv <origen> <destino>": "Mover o renombrar archivos o directorios.",
                "chmod <permisos> <archivo>": "Cambiar los permisos de un archivo.",
                "chown <usuario>:<grupo> <archivo>": "Cambiar el propietario y el grupo de un archivo.",
                "ls -la": "Listar todos los archivos en un directorio con detalles.",
                "grep <cadena> <archivo>": "Buscar una cadena en un archivo.",
                "find <directorio> -name <nombre_archivo>": "Buscar un archivo por su nombre.",
                "tar -czvf <archivo.tar.gz> <directorio>": "Crear un archivo tar comprimido.",
                "scp <origen> <usuario>@<host>:<destino>": "Copiar archivos entre hosts usando SSH.",
                "wget <url>": "Descargar archivos desde la web.",
                "curl <url>": "Transferir datos desde o hacia un servidor."
            }
        }
        self.actualizar_lista_comandos()

    def actualizar_lista_comandos(self, event=None):
        os_type = self.os_var.get()
        self.command_listbox.delete(0, tk.END)
        for cmd in self.commands[os_type]:
            self.command_listbox.insert(tk.END, cmd)

    def buscar_comandos(self, event=None):
        termino = self.search_var.get().lower()
        os_type = self.os_var.get()
        self.command_listbox.delete(0, tk.END)
        for cmd in self.commands[os_type]:
            if termino in cmd.lower():
                self.command_listbox.insert(tk.END, cmd)

    def mostrar_descripcion(self, event):
        widget = event.widget
        index = widget.nearest(event.y)
        comando = widget.get(index)
        os_type = self.os_var.get()
        descripcion = self.commands[os_type].get(comando, "")
        self.description_label.config(text=descripcion)

    def copiar_al_portapapeles(self, event):
        widget = event.widget
        index = widget.curselection()
        if index:
            comando = widget.get(index[0])
            self.clipboard_clear()
            self.clipboard_append(comando)
            self.update()  # Mantener el contenido después de cerrar
            self.description_label.config(text=f'Comando "{comando}" copiado al portapapeles.')

if __name__ == "__main__":
    app = CommandApp()
    app.mainloop()
