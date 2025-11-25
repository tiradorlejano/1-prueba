"""
3 en raya: enfrentamiento entre dos inteligencias artificiales simples.
"""

import numpy as np
import random
import time

def inicializar_tablero():
	return np.zeros((3, 3), dtype=int)

def mostrar_tablero(tablero):
	simbolos = {0: " ", 1: "X", 2: "O"}
	print("\nTablero:")
	for fila in tablero:
		print("|" + "|".join([simbolos[c] for c in fila]) + "|")

def movimientos_posibles(tablero):
	return [(i, j) for i in range(3) for j in range(3) if tablero[i, j] == 0]

def verificar_ganador(tablero):
	for jugador in [1, 2]:
		# Filas y columnas
		for i in range(3):
			if all(tablero[i, :] == jugador) or all(tablero[:, i] == jugador):
				return jugador
		# Diagonales
		if all([tablero[i, i] == jugador for i in range(3)]) or all([tablero[i, 2 - i] == jugador for i in range(3)]):
			return jugador
	if not movimientos_posibles(tablero):
		return 0  # Empate
	return -1  # No terminado

def ia_aleatoria(tablero, jugador):

	posibles = movimientos_posibles(tablero)
	return random.choice(posibles)

def ia_secuencial(tablero, jugador):
	posibles = movimientos_posibles(tablero)
	return posibles[0]

def ia_bloqueadora(tablero, jugador):
	rival = 2 if jugador == 1 else 1
	posibles = movimientos_posibles(tablero)
	for i, j in posibles:
		copia = tablero.copy()
		copia[i, j] = rival
		if verificar_ganador(copia) == rival:
			return (i, j)
	return random.choice(posibles)

def ia_perfecta(tablero, jugador):
    # Algoritmo minimax con poda alfa-beta para jugar perfectamente
    def minimax(tab, depth, is_max, player, alpha, beta):
        winner = verificar_ganador(tab)
        if winner == jugador:
            return 1
        elif winner == 0:
            return 0
        elif winner == 2 if jugador == 1 else 1:
            return -1
        if is_max:
            best = -float('inf')
            for i, j in movimientos_posibles(tab):
                tab[i, j] = player
                val = minimax(tab, depth+1, False, 2 if player == 1 else 1, alpha, beta)
                tab[i, j] = 0
                best = max(best, val)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float('inf')
            for i, j in movimientos_posibles(tab):
                tab[i, j] = player
                val = minimax(tab, depth+1, True, 2 if player == 1 else 1, alpha, beta)
                tab[i, j] = 0
                best = min(best, val)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best
    mejor_valor = -float('inf')
    mejor_mov = None
    for i, j in movimientos_posibles(tablero):
        tablero[i, j] = jugador
        valor = minimax(tablero, 0, False, 2 if jugador == 1 else 1, -float('inf'), float('inf'))
        tablero[i, j] = 0
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_mov = (i, j)
    return mejor_mov

def ia_mediocre(tablero, jugador):
    # Juega aleatorio el 80% de las veces, el resto juega como secuencial
    if random.random() < 0.8:
        return ia_aleatoria(tablero, jugador)
    else:
        return ia_secuencial(tablero, jugador)


def simular_enfrentamientos(n=100):
		resultados = {1: 0, 2: 0, 0: 0}
		ia_funcs = [ia_aleatoria, ia_secuencial, ia_bloqueadora, ia_perfecta, ia_mediocre]
		nombres = {ia_aleatoria: "Aleatoria", ia_secuencial: "Secuencial", ia_bloqueadora: "Bloqueadora", ia_perfecta: "Perfecta", ia_mediocre: "Mediocre"}
		enfrentamientos = []
		for i in range(n):
			ia1 = random.choice(ia_funcs)
			ia2 = random.choice(ia_funcs)
			tablero = inicializar_tablero()
			turno = 1
			while True:
				if turno == 1:
					x, y = ia1(tablero, 1)
					tablero[x, y] = 1
				else:
					x, y = ia2(tablero, 2)
					tablero[x, y] = 2
				ganador = verificar_ganador(tablero)
				if ganador != -1:
					enfrentamientos.append((nombres[ia1], nombres[ia2], ganador))
					resultados[ganador] += 1
					break
				turno = 3 - turno
		print(f"\nResumen de {n} partidas:")
		print(f"Gana X: {resultados[1]}")
		print(f"Gana O: {resultados[2]}")
		print(f"Empates: {resultados[0]}")
		print("\nRecuento total de victorias por jugador IA:")
		# Contar victorias y derrotas por tipo de IA
		victorias = {"Aleatoria": 0, "Secuencial": 0, "Bloqueadora": 0, "Perfecta": 0, "Mediocre": 0}
		derrotas = {"Aleatoria": [], "Secuencial": [], "Bloqueadora": [], "Perfecta": [], "Mediocre": []}
		for iax, iao, res in enfrentamientos:
			if res == 1:
				victorias[iax] += 1
				derrotas[iao].append(iax)
			elif res == 2:
				victorias[iao] += 1
				derrotas[iax].append(iao)
		for idx, (nombre, cant) in enumerate(sorted(victorias.items(), key=lambda x: x[1], reverse=True), 1):
			print(f"{idx}. {nombre}: {cant} victorias")
		print("\nDerrotas de cada jugador IA (contra quién perdieron):")
		for idx, (nombre, lista) in enumerate(derrotas.items(), 1):
			if lista:
				perdidas = ", ".join(lista)
				print(f"{idx}. {nombre} perdió contra: {perdidas}")
			else:
				print(f"{idx}. {nombre} no perdió ninguna partida.")
		print("\nResultados completos de las partidas:")
		for idx, (iax, iao, res) in enumerate(enfrentamientos, 1):
			res_str = "Empate" if res == 0 else ("X" if res == 1 else "O")
			print(f"{idx}. {iax} (X) vs {iao} (O) -> {res_str}")

if __name__ == "__main__":
    simular_enfrentamientos(100)
