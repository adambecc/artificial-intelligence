import random
import time

def generar_laberinto(filas, columnas, porcentaje_paredes=0.3):
    laberinto = [[1 if random.random() < porcentaje_paredes else 0 for _ in range(columnas)] for _ in range(filas)]
    laberinto[0][0] = 0
    laberinto[filas-1][columnas-1] = 0
    return laberinto

def imprimir_laberinto(laberinto):
    for fila in laberinto:
        print(" ".join(str(c) for c in fila))
    print()

def dfs(laberinto, x, y, camino, visitado, variante):
    if (x, y) == (len(laberinto)-1, len(laberinto[0])-1):
        camino.append((x, y))
        return True
    
    if x < 0 or y < 0 or x >= len(laberinto) or y >= len(laberinto[0]) or laberinto[x][y] == 1 or (x, y) in visitado:
        return False
    
    visitado.add((x, y))
    camino.append((x, y))
    
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
        if dfs(laberinto, x+dx, y+dy, camino, visitado, variante):
            return True
    
    camino.pop()
    if variante == 1:
        laberinto[x][y] = -1  # Variante 1: marcar con -1
    else:
        laberinto[x][y] = 0   # Variante 2: restaurar a 0
    
    return False

def resolver_laberinto():
    filas = int(input("Introduce el número de filas: "))
    columnas = int(input("Introduce el número de columnas: "))
    porcentaje_paredes = float(input("Introduce el porcentaje de paredes (0.1 - 0.5): "))
    variante = int(input("Elige variante (1 para marcar -1, 2 para restaurar a 0): "))
    
    laberinto = generar_laberinto(filas, columnas, porcentaje_paredes)
    imprimir_laberinto(laberinto)
    
    camino = []
    visitado = set()
    if dfs(laberinto, 0, 0, camino, visitado, variante):
        print("Solución encontrada:")
        for x, y in camino:
            laberinto[x][y] = "X"
    else:
        print("No hay solución.")
    
    imprimir_laberinto(laberinto)

if __name__ == "__main__":
    resolver_laberinto()
