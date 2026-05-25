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

# =====================================================
# PANTALLA 2: SELECCION DE PERSONAJE
# =====================================================

tk.Label(frame_personaje,
         text="Crea tu personaje",
         bg=FONDO, 
         fg=ROJO,
         font=F_GRANDE).pack(pady=(50, 20))

# Campo para escribir el nombre
tk.Label(frame_personaje,
         text="Tu nombre:",
         bg=FONDO, 
         fg=TEXTO,
         font=F_NORMAL).pack()

entrada_nombre = tk.Entry(
    frame_personaje,
    font=F_NORMAL,
    bg=PANEL,
    fg=TEXTO,
    insertbackground=TEXTO,
    relief="flat",
    width=22
)

entrada_nombre.pack(pady=6)

# Radiobuttons para elegir clase
# Cuando el usuario selecciona uno, clase_var se actualiza sola.
# Leemos su valor con clase_var.get()
clase_var = tk.StringVar(value="Guerrero")

tk.Label(frame_personaje,
         text="Elige tu clase:",
         bg=FONDO, 
         fg=TEXTO,
         font=F_MEDIA).pack(pady=(14, 4))

# Frame horizontal para poner los 4 botones en fila
fila_clases = tk.Frame(frame_personaje, bg=FONDO)
fila_clases.pack()

def actualizar_desc_clase():
    # Cuando el jugador cambia la clase, actualizamos la descripcion
    clase = clase_var.get()
    lbl_desc_clase.config(text=descripciones[clase])

for clase in ["Guerrero", "Mago", "Arquero", "Asesino"]:
    tk.Radiobutton(fila_clases,
                   text=clase,
                   variable=clase_var,  # todos comparten la misma variable
                   value=clase,         # este boton representa este valor
                   command=actualizar_desc_clase, 
                   bg=FONDO, fg=TEXTO,
                   selectcolor=PANEL,
                   font=F_NORMAL,
                   activebackground=FONDO,
                   activeforeground=ROJO).pack(side="left", padx=25)
    

# Descripciones de cada clase
descripciones = {
    "Guerrero": "Mucha vida y fuerza. Con poca vida golpea 3 veces seguidas.",
    "Mago":     "Ataca con inteligencia. Con poca vida lanza hechizo x4.",
    "Arquero":  "Equilibrado. Con poca vida dispara lluvia de flechas.",
    "Asesino":  "Maximo dano. Con poca vida activa sombra mortal x5.",
}

lbl_desc_clase = tk.Label(
    frame_personaje,
    text=descripciones["Guerrero"],
    bg=PANEL,
    fg=TEXTO,
    font=F_CHICA,
    wraplength=480,
    padx=10,
    pady=8
)

lbl_desc_clase.pack(
    pady=10,
    padx=50,
    fill="x"
)


# Mensaje de error si el nombre esta vacio
lbl_error_nombre = tk.Label(frame_personaje,
                              text="",
                              bg=FONDO, 
                              fg=ROJO,
                              font=F_NORMAL)

lbl_error_nombre.pack(pady=4)

def confirmar_personaje():
    # Lee el nombre y crea el jugador con la clase elegida
    global jugador  # usamos global para modificar la variable de arriba

    nombre = entrada_nombre.get().strip()

    if not nombre:
        lbl_error_nombre.config(text="Escribe tu nombre antes de continuar")
        return

    lbl_error_nombre.config(text="")

    # Diccionario: texto del boton -> clase de Python
    clases = {
        "Guerrero": Guerrero,
        "Mago":     Mago,
        "Arquero":  Arquero,
        "Asesino":  Asesino,
    }

    # Creamos el jugador y le damos un arma inicial
    ClaseElegida = clases[clase_var.get()]
    jugador = ClaseElegida(nombre)
    jugador.inventario.agregar_item(Arma.crear_arma_random("Arma inicial"))

    mostrar_combate()

tk.Button(frame_personaje,
          text="Comenzar aventura",
          command=confirmar_personaje,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=20, 
          relief="flat",
          cursor="hand2").pack(pady=8)

tk.Button(frame_personaje,
          text="Volver",
          command=mostrar_inicio,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=10, 
          relief="flat",
          cursor="hand2").pack()

# =====================================================
# PANTALLA 3: COMBATE
# =====================================================

# --- Zona superior: 3 columnas lado a lado ---
zona_info = tk.Frame(frame_combate, bg=FONDO)
zona_info.pack(fill="x", padx=10, pady=10)

# Columna izquierda: stats del jugador
col_jugador = tk.Frame(zona_info, bg=PANEL, padx=10, pady=10)
col_jugador.pack(side="left", fill="y")

tk.Label(col_jugador, 
         text="TU PERSONAJE",
         bg=PANEL, 
         fg=ROJO, 
         font=F_MEDIA).pack()

lbl_stats_jugador = tk.Label(col_jugador,
                               text="",
                               bg=PANEL, 
                               fg=TEXTO,
                               font=F_CHICA,
                               justify="left")

lbl_stats_jugador.pack(pady=4)

# Columna central: log de combate
col_log = tk.Frame(zona_info, bg=FONDO)
col_log.pack(side="left", 
             padx=10, 
             fill="both", 
             expand=True)

tk.Label(col_log, text="Registro de combate",
         bg=FONDO, 
         fg=TEXTO, 
         font=F_MEDIA).pack()

# tk.Text: cuadro de texto grande de varias lineas
# state="disabled" evita que el usuario escriba en el
log_combate = tk.Text(col_log,
                       width=30, 
                       height=14,
                       bg=PANEL, 
                       fg=TEXTO,
                       font=F_CHICA,
                       state="disabled",
                       relief="flat",
                       wrap="word")
log_combate.pack()

# Columna derecha: stats del enemigo
col_enemigo = tk.Frame(zona_info, bg=PANEL, padx=10, pady=10)
col_enemigo.pack(side="left", fill="y")

tk.Label(col_enemigo, text="ENEMIGO",
         bg=PANEL, fg=ROJO, font=F_MEDIA).pack()

lbl_stats_enemigo = tk.Label(col_enemigo,
                               text="Sin enemigo\n\nElige uno\narriba",
                               bg=PANEL, 
                               fg=TEXTO,
                               font=F_CHICA,
                               justify="left")
lbl_stats_enemigo.pack(pady=4)

# --- Zona media: botones para elegir enemigo ---
tk.Label(frame_combate,
         text="Elige un enemigo:",
         bg=FONDO, 
         fg=DORADO,
         font=F_MEDIA).pack(pady=(2, 4))

zona_enemigos = tk.Frame(frame_combate, bg=FONDO)
zona_enemigos.pack()

# Las funciones de elegir enemigo van abajo (necesitan acceso a log_combate)

# --- Zona inferior: botones de accion ---
zona_acciones = tk.Frame(frame_combate, bg=FONDO)
zona_acciones.pack(pady=6)

# --- Frame para la recompensa (aparece al ganar un combate) ---
frame_recompensa = tk.Frame(frame_combate, bg=FONDO)
frame_recompensa.pack(pady=4)


# ---- Funciones del log ----

def log_escribir(mensaje):
    # Habilitamos el log, escribimos y lo deshabilitamos de nuevo
    log_combate.config(state="normal")
    log_combate.insert("end", f"> {mensaje}\n")
    log_combate.see("end")  # scroll automatico al final
    log_combate.config(state="disabled")

def log_limpiar():
    log_combate.config(state="normal")
    log_combate.delete("1.0", "end")  # borra desde el inicio hasta el final
    log_combate.config(state="disabled")


# ---- Funcion para actualizar los stats en pantalla ----

def actualizar_stats():
    # Actualiza lo que se ve en pantalla con los valores actuales
    if jugador is None:
        return

    # El Mago usa mana, los demas usan stamina
    if isinstance(jugador, Mago):
        recurso = f"Mana:    {jugador.mana}/{jugador.mana_max}"
    else:
        recurso = f"Stamina: {jugador.stamina}/{jugador.stamina_max}"

    lbl_stats_jugador.config(text=(
        f"Nombre: {jugador.nombre}\n"
        f"Clase:  {jugador.__class__.__name__}\n"
        f"Vida:   {jugador.vida}/{jugador.vida_max}\n"
        f"Fuerza: {jugador.fuerza}  Def: {jugador.defensa}\n"
        f"{recurso}\n"
        f"Arma:   {jugador.arma.nombre}\n"
        f"        [{jugador.arma.rareza}]\n"
        f"Puntos: {jugador.puntos}"
    ))

    if enemigo is not None:
        lbl_stats_enemigo.config(text=(
            f"Nombre: {enemigo.nombre}\n"
            f"Vida:   {enemigo.vida}/{enemigo.vida_max}\n"
            f"Fuerza: {enemigo.fuerza}\n"
            f"Def:    {enemigo.defensa}"
        ))
    else:
        lbl_stats_enemigo.config(text="Sin enemigo\n\nElige uno\narriba")


# ---- Funciones de combate ----

def iniciar_combate(nombre_enemigo, multiplicador, puntos):
    # Crea el enemigo y prepara el combate
    global enemigo, puntos_enemigo
    enemigo = Enemigo(nombre_enemigo, multiplicador)
    puntos_enemigo = puntos
    limpiar_recompensa()
    log_limpiar()
    log_escribir(f"Combate contra {nombre_enemigo} iniciado!")
    actualizar_stats()

def turno_enemigo():
    # Despues de que el jugador actua, el enemigo responde
    global enemigo

    if not enemigo.esta_vivo():
        # El enemigo murio: el jugador gano
        en_victoria()
        return

    # El enemigo ataca al jugador
    vida_antes = jugador.vida
    enemigo.atacar(jugador)
    dano_recibido = vida_antes - jugador.vida

    log_escribir(f"{enemigo.nombre} te ataco: -{dano_recibido} de vida")
    actualizar_stats()

    if not jugador.esta_vivo():
        # El jugador murio: derrota
        en_derrota()

def en_victoria():
    global enemigo

    jugador.puntos += puntos_enemigo

    # Loot aleatorio al inventario
    loot = Arma.crear_arma_random("Loot")
    jugador.inventario.agregar_item(loot)

    log_escribir(f"Ganaste! +{puntos_enemigo} pts")
    log_escribir(f"Loot: {loot.nombre} [{loot.rareza}]")

    nombre_enemigo = enemigo.nombre
    enemigo = None
    actualizar_stats()

    if nombre_enemigo == "Dragon":
        # Era el jefe final: fin del juego
        guardar_ranking(jugador)
        configurar_pantalla_fin(victoria=True)
        mostrar_fin()
    else:
        # Era un enemigo normal: mostrar recompensa
        mostrar_recompensa()

def en_derrota():
    guardar_ranking(jugador)
    configurar_pantalla_fin(victoria=False)
    mostrar_fin()


# ---- Acciones del jugador ----

def accion_atacar():
    if enemigo is None:
        log_escribir("Primero elige un enemigo")
        return

    vida_antes = enemigo.vida
    jugador.atacar(enemigo)  # metodo del Taller 1
    dano = vida_antes - enemigo.vida

    log_escribir(f"Atacaste a {enemigo.nombre}: -{dano} de vida")
    turno_enemigo()

def accion_descansar():
    if enemigo is None:
        log_escribir("Primero elige un enemigo")
        return

    # El Mago recupera mana, los demas recuperan stamina
    if isinstance(jugador, Mago):
        jugador.mana = min(jugador.mana + 3, jugador.mana_max)
        log_escribir("Descansaste: +3 mana")
    else:
        jugador.stamina = min(jugador.stamina + 3, jugador.stamina_max)
        log_escribir("Descansaste: +3 stamina")

    turno_enemigo()

def accion_huir():
    global enemigo
    enemigo = None
    log_escribir("Huiste del combate. Elige otro enemigo.")
    actualizar_stats()

def accion_inventario():
    # Abre una ventana emergente para equipar armas
    # tk.Toplevel: ventana flotante encima de la principal
    if not jugador.inventario.items:
        log_escribir("No tienes armas en el inventario")
        return

    ventana_inv = tk.Toplevel(ventana)
    ventana_inv.title("Inventario")
    ventana_inv.configure(bg=FONDO)
    ventana_inv.resizable(False, False)
    ventana_inv.geometry("360x280")

    tk.Label(ventana_inv,
             text="Elige un arma para equipar",
             bg=FONDO, fg=ROJO,
             font=F_MEDIA).pack(pady=10)

    for arma in jugador.inventario.items:
        # a=arma: cada boton guarda su propia arma en la variable 'a'
        # Sin esto, todos los botones usarian la ultima arma del loop
        def al_equipar(a=arma):
            jugador.arma = a
            log_escribir(f"Equipaste: {a.nombre} [{a.rareza}]")
            actualizar_stats()
            ventana_inv.destroy()

        tk.Button(ventana_inv,
                  text=f"{arma.nombre}  [{arma.rareza}]  dano:{arma.daño}",
                  command=al_equipar,
                  bg=BOTON, 
                  fg=TEXTO,
                  font=F_CHICA,
                  width=38, 
                  relief="flat",
                  cursor="hand2").pack(pady=4)

    tk.Button(ventana_inv,
              text="Cerrar",
              command=ventana_inv.destroy,
              bg=BOTON, 
              fg=TEXTO,
              font=F_NORMAL,
              width=12, relief="flat").pack(pady=8)


# ---- Recompensa ----

def mostrar_recompensa():
    # Muestra botones para elegir recompensa tras ganar un combate
    limpiar_recompensa()

    tk.Label(frame_recompensa,
             text="Victoria! Elige tu recompensa:",
             bg=FONDO, 
             fg=VERDE,
             font=F_MEDIA).pack(pady=(4, 6))

    fila = tk.Frame(frame_recompensa, bg=FONDO)
    fila.pack()

    tk.Button(fila,
              text="Recuperar 30 de vida",
              command=recompensa_vida,
              bg=BOTON, 
              fg=TEXTO,
              font=F_NORMAL,
              width=20, relief="flat",
              cursor="hand2").pack(side="left", padx=8)

    tk.Button(fila,
              text="Mejorar Fuerza y Defensa",
              command=recompensa_stats,
              bg=BOTON, 
              fg=TEXTO,
              font=F_NORMAL,
              width=22, relief="flat",
              cursor="hand2").pack(side="left", padx=8)

def recompensa_vida():
    jugador.vida += 30
    log_escribir("Recuperaste 30 de vida")
    limpiar_recompensa()
    actualizar_stats()

def recompensa_stats():
    jugador.fuerza  += 2
    jugador.defensa += 2
    if isinstance(jugador, Mago):
        jugador.inteligencia += 2
    log_escribir("Mejoraste Fuerza y Defensa (+2)")
    limpiar_recompensa()
    actualizar_stats()

def limpiar_recompensa():
    # Borra los botones de recompensa de la pantalla
    for widget in frame_recompensa.winfo_children():
        widget.destroy()


# ---- Creamos los botones de enemigos y acciones ----

tk.Button(zona_enemigos,
          text="Goblin (facil)",
          command=lambda: iniciar_combate("Goblin", 2, 1),
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=14, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=6)

tk.Button(zona_enemigos,
          text="Orco (medio)",
          command=lambda: iniciar_combate("Orco", 3, 2),
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=14, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=6)

# El Dragon tiene fondo rojo para que destaque como jefe final
tk.Button(zona_enemigos,
          text="Dragon (FINAL)",
          command=lambda: iniciar_combate("Dragon", 4, 5),
          bg=ROJO, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=14, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=6)

tk.Button(zona_acciones,
          text="Atacar",
          command=accion_atacar,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=10, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=5)

tk.Button(zona_acciones,
          text="Descansar",
          command=accion_descansar,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=10, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=5)

tk.Button(zona_acciones,
          text="Inventario",
          command=accion_inventario,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=10, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=5)

tk.Button(zona_acciones,
          text="Huir",
          command=accion_huir,
          bg=BOTON, 
          fg=TEXTO, 
          font=F_NORMAL,
          width=10, 
          relief="flat",
          cursor="hand2").pack(side="left", padx=5)
