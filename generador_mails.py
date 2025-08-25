import random
import string
import tkinter as tk
from tkinter import messagebox
from faker import Faker

fake = Faker('es_ES')

# Lista inicial de dominios válidos (sin example.com)
dominios_validos = ["gmail.com", "hotmail.com", "yahoo.com", "outlook.com"]

def generar_datos_ficticios(cantidad=10, excluir=None, dominio_extra=None, usar_punto=True):
    datos = []
    dominios = dominios_validos.copy()

    # Excluir dominios marcados
    if excluir:
        dominios = [d for d in dominios if d not in excluir]

    # Agregar dominio extra
    if dominio_extra:
        dominios.append(dominio_extra.strip())

    # Asegurar que haya al menos un dominio disponible
    if not dominios:
        dominios = ["gmail.com"]

    for _ in range(cantidad):
        nombre = fake.first_name().lower()
        apellido = fake.last_name().lower()
        separador = "." if usar_punto else ""
        correo = f"{nombre}{separador}{apellido}{random.randint(1,999)}@{random.choice(dominios)}"
        
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
    # Limpiar lista anterior
    for widget in frame_lista.winfo_children():
        widget.destroy()

    try:
        cantidad = int(entry_cantidad.get() or 10)
    except ValueError:
        cantidad = 10

    # Obtener dominios marcados para excluir
    excluir = [dominio for dominio, var in vars_dominios.items() if var.get()]

    dominio_extra = entry_extra.get().strip() or None
    usar_punto = bool(var_usar_punto.get())

    datos = generar_datos_ficticios(cantidad, excluir, dominio_extra, usar_punto)

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
root.geometry("750x600")

frame_controles = tk.Frame(root)
frame_controles.pack(pady=10)

# Cantidad de filas
tk.Label(frame_controles, text="Cantidad de filas:").grid(row=0, column=0, padx=5, sticky="w")
entry_cantidad = tk.Entry(frame_controles, width=5)
entry_cantidad.grid(row=0, column=1, padx=5, sticky="w")
entry_cantidad.insert(0, "10")

# Checkboxes para excluir dominios
tk.Label(frame_controles, text="Excluir dominios:").grid(row=1, column=0, padx=5, sticky="w")
vars_dominios = {}
frame_checks = tk.Frame(frame_controles)
frame_checks.grid(row=1, column=1, padx=5, sticky="w")
for dom in dominios_validos:
    var = tk.BooleanVar(value=False)
    chk = tk.Checkbutton(frame_checks, text=dom, variable=var)
    chk.pack(anchor="w")
    vars_dominios[dom] = var

# Dominio extra
tk.Label(frame_controles, text="Dominio extra:").grid(row=2, column=0, padx=5, sticky="w")
entry_extra = tk.Entry(frame_controles, width=20)
entry_extra.grid(row=2, column=1, padx=5, sticky="w")
entry_extra.insert(0, "umayor.cl")

# Checkbox separador punto
var_usar_punto = tk.BooleanVar(value=True)
chk_punto = tk.Checkbutton(frame_controles, text="Usar punto entre nombre y apellido", variable=var_usar_punto)
chk_punto.grid(row=3, column=0, columnspan=2, pady=5, sticky="w")

# Botón regenerar
btn_regenerar = tk.Button(frame_controles, text="Reiniciar lista", command=mostrar_datos)
btn_regenerar.grid(row=4, column=0, columnspan=2, pady=10)

frame_lista = tk.Frame(root)
frame_lista.pack(pady=10, fill="both", expand=True)

# Mostrar datos iniciales
mostrar_datos()

root.mainloop()

# pyinstaller --onefile --windowed generador_mails.py