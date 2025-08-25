import random
import string
import tkinter as tk
from tkinter import messagebox
from faker import Faker

fake = Faker('es_ES')

def generar_datos_ficticios(cantidad=10):
    datos = []
    for _ in range(cantidad):
        nombre = fake.first_name()
        apellido = fake.last_name()
        correo = f"{nombre.lower()}.{apellido.lower()}{random.randint(1,999)}@{fake.free_email_domain()}"
        longitud_pwd = random.randint(8, 12)
        caracteres = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(caracteres) for _ in range(longitud_pwd))
        datos.append((correo, password))
    return datos

def copiar_al_portapapeles(texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()
    messagebox.showinfo("Copiado", f"'{texto}' copiado al portapapeles")

def mostrar_datos():
    # Eliminar filas anteriores (excepto encabezados y controles)
    for widget in frame_lista.winfo_children():
        widget.destroy()
    
    datos = generar_datos_ficticios(int(entry_cantidad.get() or 10))
    
    # Encabezados
    tk.Label(frame_lista, text="Sel.", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=5)
    tk.Label(frame_lista, text="Correo", font=("Arial", 10, "bold")).grid(row=0, column=1, padx=10, pady=5)
    tk.Label(frame_lista, text="Contraseña", font=("Arial", 10, "bold")).grid(row=0, column=2, padx=10, pady=5)

    for i, (correo, pwd) in enumerate(datos, start=1):
        var = tk.BooleanVar()
        chk = tk.Checkbutton(frame_lista, variable=var)
        chk.grid(row=i, column=0, padx=5, pady=2)

        btn_correo = tk.Button(frame_lista, text=correo, relief=tk.FLAT, fg="blue", cursor="hand2",
                               command=lambda c=correo: copiar_al_portapapeles(c))
        btn_correo.grid(row=i, column=1, sticky="w", padx=10, pady=2)

        btn_pwd = tk.Button(frame_lista, text=pwd, relief=tk.FLAT, fg="green", cursor="hand2",
                            command=lambda p=pwd: copiar_al_portapapeles(p))
        btn_pwd.grid(row=i, column=2, sticky="w", padx=10, pady=2)

# --- Ventana principal ---
root = tk.Tk()
root.title("Generador de correos ficticios")
root.geometry("650x500")

# Controles superiores: textbox y botón regenerar
frame_controles = tk.Frame(root)
frame_controles.pack(pady=10)

tk.Label(frame_controles, text="Cantidad de filas:").pack(side=tk.LEFT, padx=5)
entry_cantidad = tk.Entry(frame_controles, width=5)
entry_cantidad.pack(side=tk.LEFT)
entry_cantidad.insert(0, "10")  # valor por defecto

btn_regenerar = tk.Button(frame_controles, text="Reiniciar lista", command=mostrar_datos)
btn_regenerar.pack(side=tk.LEFT, padx=10)

# Frame donde se dibuja la lista
frame_lista = tk.Frame(root)
frame_lista.pack(pady=10, fill="both", expand=True)

# Mostrar datos iniciales
mostrar_datos()

root.mainloop()

# pyinstaller --onefile --windowed generador_mails.py