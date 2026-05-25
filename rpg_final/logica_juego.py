from abc import ABC, abstractmethod
import random
import json
from typing import Optional


class Arma:

    rarezas = {
        "Comun": 3,
        "Raro": 6,
        "Epico": 10,
        "Legendario": 15
    }

    def __init__(self, nombre: str, daño: int, rareza: str) -> None:
        self.nombre = nombre
        self.daño = daño
        self.rareza = rareza

    # METODO MAGICO __str__
    def __str__(self) -> str:
        return f"{self.nombre} | {self.rareza} | Daño: {self.daño}"

    # METODO MAGICO __repr__
    def __repr__(self) -> str:
        return self.__str__()

    # METODO ESTATICO
    @staticmethod
    def generar_rareza() -> str:

        numero = random.randint(1, 100)

        if numero <= 50:
            return "Comun"

        elif numero <= 80:
            return "Raro"

        elif numero <= 95:
            return "Epico"

        return "Legendario"

    # METODO DE CLASE
    @classmethod
    def crear_arma_random(cls, nombre: str) -> "Arma":

        rareza = cls.generar_rareza()

        daño_base = cls.rarezas[rareza]

        daño = random.randint(daño_base, daño_base + 8)

        return cls(nombre, daño, rareza)


class Inventario:

    def __init__(self) -> None:
        self.items: list[Arma] = []

    def agregar_item(self, item: Arma) -> None:
        self.items.append(item)

    def mostrar_items(self) -> None:

        if not self.items:
            print("Inventario vacío")
            return

        print("\nINVENTARIO")

        for i, item in enumerate(self.items):
            print(f"{i+1}. {item}")

    def obtener_item(self, indice: int) -> Optional[Arma]:

        if 0 <= indice < len(self.items):
            return self.items[indice]

        return None

    # METODO MAGICO __str__
    def __str__(self) -> str:
        return f"Inventario con {len(self.items)} items"

    # METODO MAGICO __repr__
    def __repr__(self) -> str:
        return self.__str__()


# CLASE ABSTRACTA
class Personaje(ABC):

    def __init__(self, nombre: str, fuerza: int, defensa: int, vida: int) -> None:

        self.__nombre = nombre
        self.fuerza = fuerza
        self.defensa = defensa
        self.__vida = vida
        self.vida_max = vida
        self.puntos = 0

        # COMPOSICION -> Personaje tiene un Inventario
        self.inventario = Inventario()

    # ENCAPSULAMIENTO -> getter
    @property
    def nombre(self) -> str:
        return self.__nombre

    @property
    def vida(self) -> int:
        return self.__vida

    # ENCAPSULAMIENTO -> setter
    @vida.setter
    def vida(self, valor: int) -> None:

        if valor < 0:
            valor = 0

        if valor > self.vida_max:
            valor = self.vida_max

        self.__vida = valor

    def esta_vivo(self) -> bool:
        return self.__vida > 0

    def calcular_daño(self, poder: int, enemigo: "Personaje") -> int:

        daño = poder - enemigo.defensa

        return max(0, daño)

    def equipar_arma(self) -> None:

        self.inventario.mostrar_items()

        if not self.inventario.items:
            return

        opcion = int(input("Elige arma: ")) - 1

        arma = self.inventario.obtener_item(opcion)

        if arma:
            self.arma = arma
            print("Ahora usas:", arma.nombre)

    # METODO ABSTRACTO
    @abstractmethod
    def atacar(self, enemigo: "Personaje") -> None:
        pass

    # METODO ABSTRACTO
    @abstractmethod
    def accion(self) -> None:
        pass

    # METODO MAGICO __str__
    def __str__(self) -> str:
        return f"{self.nombre} | Vida: {self.vida}"

    # METODO MAGICO __repr__
    def __repr__(self) -> str:
        return self.__str__()


# HERENCIA Y POLIMORFISMO
class Guerrero(Personaje):

    def __init__(self, nombre: str) -> None:

        super().__init__(
            nombre,
            random.randint(8, 15),
            random.randint(4, 8),
            random.randint(90, 120)
        )

        self.stamina = 10
        self.stamina_max = 10

        self.arma = Arma.crear_arma_random("Espada")

    def atacar(self, enemigo: Personaje) -> None:

        if self.stamina < 2:
            print("Sin stamina")
            return

        daño_base = self.fuerza + self.arma.daño

        # PASIVA
        if self.vida <= 10:
            daño_base *= 3
            print(self.nombre, "golpea con fuerza bruta")

        daño = self.calcular_daño(daño_base, enemigo)

        self.stamina -= 2
        enemigo.vida -= daño

        print(self.nombre, "usa", self.arma.nombre)
        print("Daño:", daño)

    def accion(self) -> None:
        print(self.nombre, "golpea con fuerza")


# HERENCIA Y POLIMORFISMO
class Mago(Personaje):

    def __init__(self, nombre: str) -> None:

        super().__init__(
            nombre,
            2,
            random.randint(2, 5),
            random.randint(70, 90)
        )

        self.inteligencia = random.randint(10, 18)

        self.mana = 10
        self.mana_max = 10

        self.arma = Arma.crear_arma_random("Baston")

    def atacar(self, enemigo: Personaje) -> None:

        if self.mana < 2:
            print("Sin mana")
            return

        daño_base = self.inteligencia + self.arma.daño

        if self.vida <= 10:
            daño_base *= 4
            print(self.nombre, "ACTIVA HECHIZO PROHIBIDO")

        daño = self.calcular_daño(daño_base, enemigo)

        self.mana -= 2
        enemigo.vida -= daño

        print(self.nombre, "lanza un hechizo")
        print("Daño:", daño)

    def accion(self) -> None:
        print(self.nombre, "lanza magia")


# HERENCIA Y POLIMORFISMO
class Arquero(Personaje):

    def __init__(self, nombre: str) -> None:

        super().__init__(
            nombre,
            random.randint(7, 12),
            random.randint(3, 6),
            random.randint(80, 100)
        )

        self.stamina = 10
        self.stamina_max = 10

        self.arma = Arma.crear_arma_random("Arco")

    def atacar(self, enemigo: Personaje) -> None:

        if self.stamina < 2:
            print("Sin stamina")
            return

        daño_base = self.fuerza + self.arma.daño

        if self.vida <= 10:
            daño_base *= 3
            print(self.nombre, "ACTIVA LLUVIA DE FLECHAS")

        daño = self.calcular_daño(daño_base, enemigo)

        self.stamina -= 2
        enemigo.vida -= daño

        print(self.nombre, "dispara una flecha")
        print("Daño:", daño)

    def accion(self) -> None:
        print(self.nombre, "dispara")


# HERENCIA Y POLIMORFISMO
class Asesino(Personaje):

    def __init__(self, nombre: str) -> None:

        super().__init__(
            nombre,
            random.randint(9, 14),
            random.randint(2, 5),
            random.randint(75, 95)
        )

        self.stamina = 10
        self.stamina_max = 10

        self.arma = Arma.crear_arma_random("Dagas")

    def atacar(self, enemigo: Personaje) -> None:

        if self.stamina < 2:
            print("Sin stamina")
            return

        daño_base = self.fuerza + self.arma.daño

        if self.vida <= 10:
            daño_base *= 5
            print(self.nombre, "ACTIVA SOMBRA MORTAL")

        daño = self.calcular_daño(daño_base, enemigo)

        self.stamina -= 2
        enemigo.vida -= daño

        print(self.nombre, "ataca desde las sombras")
        print("Daño:", daño)

    def accion(self) -> None:
        print(self.nombre, "ataca rápidamente")


class Enemigo(Personaje):

    def __init__(self, nombre: str, multiplicador: int) -> None:

        if nombre == "Goblin":
            fuerza = random.randint(4, 7)
            defensa = random.randint(1, 3)
            vida = random.randint(50, 70)
        elif nombre == "Orco":
            fuerza = random.randint(7, 10)
            defensa = random.randint(2, 5)
            vida = random.randint(70, 90)
        else:
            fuerza = random.randint(10, 15)
            defensa = random.randint(4, 7)
            vida = random.randint(110, 140)
        super().__init__(nombre, fuerza, defensa, vida)
        self.multiplicador = multiplicador

    def atacar(self, enemigo: Personaje) -> None:

        daño = self.calcular_daño(
            self.fuerza * self.multiplicador,
            enemigo
        )
        
        enemigo.vida -= daño
        print(self.nombre, "realizó", daño, "de daño")
    def accion(self) -> None:
        print(self.nombre, "ataca")


def mostrar_recurso(jugador: Personaje) -> None:

    if isinstance(jugador, Mago):
        print("Mana:", jugador.mana, "/", jugador.mana_max)

    else:
        print("Stamina:", jugador.stamina, "/", jugador.stamina_max)


def mostrar_stats(jugador: Personaje) -> None:

    print("\nJugador:", jugador.nombre)
    print("Clase:", jugador.__class__.__name__)
    print("Vida:", jugador.vida, "/", jugador.vida_max)
    print("Fuerza:", jugador.fuerza)
    print("Defensa:", jugador.defensa)

    if isinstance(jugador, Mago):
        print("Inteligencia:", jugador.inteligencia)

    mostrar_recurso(jugador)

    print("Arma:", jugador.arma)


def guardar_ranking(jugador: Personaje) -> None:

    try:

        with open("ranking.json", "r") as archivo:
            ranking = json.load(archivo)

    except:
        ranking = []

    ranking.append({
        "nombre": jugador.nombre,
        "puntos": jugador.puntos
    })

    ranking.sort(key=lambda x: x["puntos"], reverse=True)

    ranking = ranking[:5]

    with open("ranking.json", "w") as archivo:
        json.dump(ranking, archivo, indent=4)


def mostrar_ranking() -> None:

    try:

        with open("ranking.json", "r") as archivo:
            ranking = json.load(archivo)

    except:
        print("No hay ranking")
        return

    print("\nTOP 5")

    for i, jugador in enumerate(ranking):
        print(i + 1, "-", jugador["nombre"], "| Puntos:", jugador["puntos"])


def demostracion_polimorfismo() -> None:

    print("\nDEMOSTRACIÓN DE POLIMORFISMO")

    personajes = [
        Guerrero("Leonidas"),
        Mago("Baltazar"),
        Arquero("Robin"),
        Asesino("Ezio")
    ]

    # POLIMORFISMO -> diferentes clases ejecutan accion() de forma distinta
    for personaje in personajes:
        personaje.accion()


def elegir_clase() -> Personaje:

    nombre = input("Pon tu nombre: ")

    print("\n1. Guerrero")
    print("2. Mago")
    print("3. Arquero")
    print("4. Asesino")

    opcion = input("Elige: ")

    while opcion not in ["1", "2", "3", "4"]:
        print("Opción inválida")
        opcion = input("Elige: ")

    if opcion == "1":
        return Guerrero(nombre)

    elif opcion == "2":
        return Mago(nombre)

    elif opcion == "3":
        return Arquero(nombre)

    return Asesino(nombre)


def combate(jugador: Personaje, enemigo: Personaje) -> bool:

    print("\nCOMBATE CONTRA", enemigo.nombre)

    while jugador.esta_vivo() and enemigo.esta_vivo():

        mostrar_stats(jugador)

        print("1. Atacar")

        print("2. Descansar")
        print("3. Equipar arma")
        print("4. Huir")

        opcion = input("Elige: ")

        while opcion not in ["1", "2", "3", "4"]:
            print("Opción inválida")
            opcion = input("Elige: ")

        if opcion == "1":
            jugador.atacar(enemigo)
        elif opcion == "2":
            if isinstance(jugador, Mago):
                jugador.mana = min(jugador.mana + 3, jugador.mana_max)
                print("Recuperaste mana")
            else:
                jugador.stamina = min(jugador.stamina + 3, jugador.stamina_max)
                print("Recuperaste stamina")
        elif opcion == "3":
            jugador.equipar_arma()
        elif opcion == "4":
            print("Huiste")
            return False
        if enemigo.esta_vivo():
            enemigo.atacar(jugador)
        print(jugador.nombre, "vida:", jugador.vida)
        print(enemigo.nombre, "vida:", enemigo.vida)

    return jugador.esta_vivo()


def recompensa(jugador: Personaje, puntos: int) -> None:

    print("\n1. Recuperar vida")
    print("2. Mejorar stats")

    opcion = input("Elige: ")

    while opcion not in ["1", "2"]:
        print("Opción inválida")
        opcion = input("Elige: ")
    if opcion == "1":
        jugador.vida += 30
        print("Te curaste")
    else:
        jugador.fuerza += puntos
        jugador.defensa += puntos
        if isinstance(jugador, Mago):
            jugador.inteligencia += puntos
        print("Subiste stats")


def juego() -> None:

    mostrar_ranking()

    jugador = elegir_clase()

    while True:

        print("\n1. Goblin")
        print("2. Orco")
        print("3. Dragon FINAL")
        opcion = input("Elige enemigo: ")
        while opcion not in ["1", "2", "3"]:
            print("Opción inválida")
            opcion = input("Elige enemigo: ")
        if opcion == "1":
            enemigo = Enemigo("Goblin", 2)
            puntos = 1
        elif opcion == "2":
            enemigo = Enemigo("Orco", 3)
            puntos = 2
        else:
            enemigo = Enemigo("Dragon", 4)
            puntos = 5
        if combate(jugador, enemigo):
            jugador.puntos += puntos
            
            print("\nGANASTE")
            
            loot = Arma.crear_arma_random("Loot")
            print("Encontraste:")
            print(loot)
            jugador.inventario.agregar_item(loot)
            
            if opcion == "3":
                print("\nDERROTASTE AL DRAGON")
                print("GANASTE EL JUEGO")
                guardar_ranking(jugador)
                break
            recompensa(jugador, puntos)
            
        else:
            print("\nGAME OVER")
            guardar_ranking(jugador)
            break


def main() -> None:

    demostracion_polimorfismo()

    juego()


if __name__ == "__main__":
    main()