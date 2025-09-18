import tkinter as tk
from tkinter import ttk, messagebox
from subprocess import getoutput, run, CalledProcessError
import os


def get_backlight_devices():
    """Busca dinámicamente los dispositivos de retroiluminación."""
    try:
        devices = os.listdir("/sys/class/backlight/")
        return [d for d in devices if os.path.exists(f"/sys/class/backlight/{d}/brightness")]
    except FileNotFoundError:
        return []


def get_current_brightness(device):
    """Obtiene el brillo actual del archivo del sistema para un dispositivo dado."""
    try:
        return int(getoutput(f"cat /sys/class/backlight/{device}/brightness"))
    except (ValueError, FileNotFoundError):
        return 0


def get_max_brightness(device):
    """Obtiene el brillo máximo para un dispositivo dado."""
    try:
        return int(getoutput(f"cat /sys/class/backlight/{device}/max_brightness"))
    except (ValueError, FileNotFoundError):
        return 255  # Valor por defecto si no se puede encontrar


def set_brightness(device, value):
    """Establece el brillo usando pkexec para permisos de root."""
    try:
        command = ["pkexec", "tee", f"/sys/class/backlight/{device}/brightness"]
        run(command, input=str(int(value)).encode(), check=True)
    except CalledProcessError as e:
        messagebox.showerror("Error", f"Fallo al ejecutar el comando: {e}")
    except FileNotFoundError:
        messagebox.showerror("Error", "Comando 'pkexec' o 'tee' no encontrado.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")


def load_brightness():
    """Carga el valor actual del brillo para el dispositivo seleccionado."""
    selected_device = device_var.get()
    current_value = get_current_brightness(selected_device)
    brightness_slider.set(current_value)


def confirm_brightness():
    """Aplica el valor del slider al dispositivo seleccionado."""
    selected_device = device_var.get()
    selected_value = brightness_slider.get()
    set_brightness(selected_device, selected_value)


def update_slider_range(event):
    """Actualiza el rango del slider cuando cambia la selección del dispositivo."""
    selected_device = device_var.get()
    max_val = get_max_brightness(selected_device)
    brightness_slider.config(to=max_val)
    load_brightness()


def update_value_label(val):
    """Muestra valor numérico y porcentaje."""
    max_val = get_max_brightness(device_var.get())
    percent = (int(float(val)) / max_val) * 100
    value_label.config(text=f"({percent:.0f}%) - {int(float(val))}")


def center_window(win, width, height):
    """Centrar la ventana en pantalla."""
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    win.geometry(f"{width}x{height}+{x}+{y}")


# Ventana principal
root = tk.Tk()
root.title("Control de Brillo")
root.configure(bg="#2E3440")  # Fondo oscuro tipo Nord
center_window(root, 440, 340)

# Estilo ttk
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", font=("Arial", 12), background="#2E3440", foreground="white")
style.configure("TButton", font=("Arial", 11), padding=6, relief="flat")
style.map("TButton",
          background=[("active", "#81A1C1")],
          foreground=[("active", "white")])

# Dispositivos disponibles
backlight_devices = get_backlight_devices()
if not backlight_devices:
    messagebox.showerror("Error", "No se encontraron dispositivos de retroiluminación.")
    root.destroy()

# Frame principal (tarjeta flotante)
main_frame = tk.Frame(root, bg="#3B4252", bd=2, relief="ridge")
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

# Selección de dispositivo
label_device = ttk.Label(main_frame, text="Seleccionar dispositivo:")
label_device.pack(pady=(15, 5))

device_var = tk.StringVar(root)
device_var.set(backlight_devices[0])

device_menu = ttk.Combobox(main_frame, textvariable=device_var, values=backlight_devices, state="readonly")
device_menu.pack(pady=5)
device_menu.bind("<<ComboboxSelected>>", update_slider_range)

# Etiqueta de brillo
label = ttk.Label(main_frame, text="Brillo de la pantalla", font=("Arial", 14))
label.pack(pady=15)

# Slider
brightness_slider = ttk.Scale(
    main_frame,
    from_=0,
    to=get_max_brightness(device_var.get()),
    orient="horizontal",
    length=300,
    command=update_value_label
)
brightness_slider.set(get_current_brightness(device_var.get()))
brightness_slider.pack(pady=5)

# Etiqueta con valor numérico y porcentaje
value_label = ttk.Label(main_frame, text="0 (0%)", font=("Arial", 12))
value_label.pack(pady=(0, 10))

# Botones
button_frame = tk.Frame(main_frame, bg="#3B4252")
button_frame.pack(pady=15)

load_button = ttk.Button(button_frame, text="Cargar", command=load_brightness)
load_button.pack(side=tk.LEFT, padx=10)

confirm_button = ttk.Button(button_frame, text="Confirmar", command=confirm_brightness)
confirm_button.pack(side=tk.LEFT, padx=10)

# Inicializar valor de la etiqueta
update_value_label(brightness_slider.get())

root.mainloop()
