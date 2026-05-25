import tkinter as tk
import json

from logica_juego import (
    Guerrero, Mago, Arquero, Asesino,
    Enemigo, Arma,
    guardar_ranking
)

FONDO  = "#1a1a2e"
PANEL  = "#16213e"
ROJO   = "#e94560"
TEXTO  = "#eaeaea"
DORADO = "#f5a623"
VERDE  = "#4caf50"
BOTON  = "#0f3460"

F_GRANDE = ("Arial", 22, "bold")
F_MEDIA  = ("Arial", 13, "bold")
F_NORMAL = ("Arial", 11)
F_CHICA  = ("Arial", 9)

# =====================================================
# VARIABLES GLOBALES
# =====================================================
jugador = None   # el personaje del jugador
enemigo = None   # el enemigo actual en combate
puntos_enemigo = 0  # puntos que da el enemigo al morir

# =====================================================
# CREAMOS LA VENTANA Y TODOS LOS FRAMES (pantallas)
# =====================================================

# La ventana principal del juego
ventana = tk.Tk()
ventana.title("Juego RPG")
ventana.resizable(False, False)
ventana.configure(bg=FONDO)
ventana.geometry("680x520")

# Cada "pantalla" es un Frame que ocupa toda la ventana.
# Con .tkraise() traemos una al frente para "cambiar de pantalla".
frame_inicio    = tk.Frame(ventana, bg=FONDO)
frame_personaje = tk.Frame(ventana, bg=FONDO)
frame_combate   = tk.Frame(ventana, bg=FONDO)
frame_fin       = tk.Frame(ventana, bg=FONDO)

# Colocamos todos los frames en la misma posicion
for frame in [frame_inicio, frame_personaje, frame_combate, frame_fin]:
    frame.place(x=0, y=0, relwidth=1, relheight=1)


# =====================================================
# FUNCIONES PARA CAMBIAR DE PANTALLA
# =====================================================

def mostrar_inicio():
    frame_inicio.tkraise()

def mostrar_seleccion():
    frame_personaje.tkraise()

def mostrar_combate():
    actualizar_stats()
    frame_combate.tkraise()

def mostrar_fin():
    frame_fin.tkraise()


# =====================================================
# PANTALLA 1: INICIO
# =====================================================
tk.Label(frame_inicio,
         text="Hecho Por:\nJose Manuel Hernandez Sepulveda\nEmanuel Isaza Castro",
         bg=FONDO,
         fg=TEXTO,
         font=F_NORMAL).pack(pady=(20, 0))

tk.Label(frame_inicio,
         text="Mata al Goblin, al Orco y al Dragon",
         bg=FONDO, 
         fg=ROJO,
         font=F_GRANDE).pack(pady=(70, 4))

tk.Label(frame_inicio,
         text="Proximamente en Steam",
         bg=FONDO, 
         fg=DORADO,
         font=F_MEDIA).pack(pady=(0, 40))

tk.Button(frame_inicio,
          text="Jugar",
          command=mostrar_seleccion,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=18, 
          relief="flat",
          cursor="hand2").pack(pady=7)

# Label donde aparece el ranking (empieza vacio)
lbl_ranking = tk.Label(frame_inicio,
                        text="",
                        bg=FONDO, 
                        fg=DORADO,
                        font=F_NORMAL,
                        justify="center")

lbl_ranking.pack(pady=(20, 0))

def ver_ranking():
    # Leemos el archivo ranking.json y mostramos el top 5
    try:
        with open("ranking.json") as f:
            datos = json.load(f)
    except Exception:
        lbl_ranking.config(text="Aun no hay puntuaciones guardadas")
        return

    lineas = ["--- TOP 5 ---"]
    for i, entrada in enumerate(datos):
        lineas.append(f"{i+1}. {entrada['nombre']}  -  {entrada['puntos']} pts")

    # "\n".join() une las lineas con saltos de linea
    lbl_ranking.config(text="\n".join(lineas))

tk.Button(frame_inicio,
          text="Ver Ranking",
          command=ver_ranking,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=18, 
          relief="flat",
          cursor="hand2").pack(pady=7)

tk.Button(frame_inicio,
          text="Salir",
          command=ventana.quit,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=18, 
          relief="flat",
          cursor="hand2").pack(pady=7)
