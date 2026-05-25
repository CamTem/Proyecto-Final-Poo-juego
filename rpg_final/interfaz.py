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
