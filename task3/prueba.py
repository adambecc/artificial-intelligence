import os
import numpy as np
import argparse
from collections import deque

# Movimientos en las 4 direcciones: izquierda, abajo, derecha, arriba
CX = [-1, 0, 1, 0]
CY = [0, -1, 0, 1]

# Variables globales
trial_count = 0
L = 0


def rotate_right(matrix):
    """Rota la matriz 90 grados a la derecha."""
    return np.rot90(matrix, k=-1)


def rotate_left(matrix):
    """Rota la matriz 90 grados a la izquierda."""
    return np.rot90(matrix, k=1)


def load_maze(file_path):
    """Carga el laberinto desde un archivo dado."""
    with open(file_path, 'r') as file:
        maze = []
        for line in file:
            row = list(map(int, line.split()))
            maze.append(row)
        return np.array(maze)


def dbf_search(x, y, yes, variant):
    """Función recursiva para resolver el laberinto."""
    global Board, trial_count, L, n, m, Rules

    # Si el agente está en la frontera del laberinto
    if x == 0 or y == 0 or x == m - 1 or y == n - 1:
        yes = True
        return yes

    # Probar las 4 direcciones posibles
    for k in range(4):
        u = x + CX[k]
        v = y + CY[k]
        trial_count += 1  # Incrementa el conteo de intentos aquí, para todos los intentos

        # Define el estado de la celda
        if Board[u][v] == 0:
            cell_status = "Free"
        elif Board[u][v] == 1:
            cell_status = "Wall"
        else:
            cell_status = "Thread"

        # Imprime el intento actual con el formato deseado
        print(
            f"{trial_count}), {'-' * (L - 2)}R{k + 1} - U={u + 1}, V={v + 1}. {cell_status}. L:{L}+1={L + 1}. LAB[{u + 1},{v + 1}]={L + 1}.")

        if Board[u][v] == 0:  # Si la celda es libre
            L += 1
            Board[u][v] = L
            Rules.append(k + 1)
            Nodes.append((u+1, v+1))

            yes = dbf_search(u, v, yes, variant)
            if yes:
                return yes

            # Imprime el backtrack
            print(
                f"{trial_count}), {'-' * (L - 2)}Backtrack from X={u + 1}, Y={v + 1}, L={L}. LAB[{u + 1},{v + 1}]=-1. L:{L}={L - 1}.")

            L -= 1
            Rules.pop()
            Nodes.pop()
            if variant == 'V1':
                Board[u][v] = -1
            elif variant == 'V2':
                Board[u][v] = 0

    return yes

from collections import deque

def bfs_search(x, y, yes):
    """Implementación de la búsqueda en anchura (BFS) para resolver el laberinto con trazas detalladas."""
    global Board, L, n, m, Rules, Nodes

    # Cola para la búsqueda en anchura
    queue = deque([(x, y)])
    distances = np.full((m, n), -1)  # Matriz de distancias inicializadas en -1
    distances[x][y] = L  # Marcamos la posición inicial con L
    wave_count = 0  # Contador de ondas
    L = 2  # Inicializar L en 2
    path_found = False  # Para verificar si se encontró la salida
    parent_map = {}  # Mapa para rastrear los padres de cada nodo
    newn = 1  # Contador de nuevos nodos

    print("\nPART 2. Trace")
    print("----------------------")

    # Imprimir la posición inicial
    print(f"\nWAVE {wave_count}, label L=\"{L}\". Initial position X={x + 1}, Y={y + 1}. NEWN = 1.")

    while queue and not path_found:
        wave_count += 1
        L += 1
        step_count = 0  # Contador de pasos para cada onda
        current_level_size = len(queue)

        print(f"\nWAVE {wave_count}, label L=\"{L}\"")

        for _ in range(current_level_size):
            current_x, current_y = queue.popleft()
            step_count += 1

            print(f"  Close CLOSE={step_count}, X={current_x + 1}, Y={current_y + 1}.")

            # Probar las 4 direcciones posibles
            for k in range(4):
                u = current_x + CX[k]
                v = current_y + CY[k]

                # Verifica si la celda está dentro del laberinto y es libre
                if 0 <= u < m and 0 <= v < n:
                    if Board[u][v] == 0:  # Si la celda es libre
                        newn += 1
                        Board[u][v] = L
                        distances[u][v] = distances[current_x][current_y] + 1
                        parent_map[(u, v)] = (current_x, current_y)  # Guardar el nodo padre
                        queue.append((u, v))

                        # Imprime el intento actual con el formato deseado
                        print(f"    R{k + 1}: X={u + 1}, Y={v + 1}. Free. NEWN={newn}.")

                        # Si alcanzamos la frontera del laberinto, hemos encontrado una salida
                        if u == 0 or v == 0 or u == m - 1 or v == n - 1:
                            yes = True
                            path_found = True
                            reconstruct_path((u, v), parent_map)
                            return yes
                    else:
                        # Celda no libre (pared o ya visitada)
                        cell_status = "Wall" if Board[u][v] == 1 else "Closed or Open"
                        print(f"    R{k + 1}: X={u + 1}, Y={v + 1}. {cell_status}.")

    return yes


def reconstruct_path(end_node, parent_map):
    """Reconstruye la ruta desde el nodo final hasta el inicial usando el mapa de padres."""
    global Nodes, Rules
    path = []
    current = end_node

    # Reconstruir la ruta desde el nodo final hacia atrás usando parent_map
    while current in parent_map:
        path.append(current)
        current = parent_map[current]

    path.append(current)  # Agregar el nodo inicial al final
    path.reverse()  # Invertir la ruta para ir desde el inicio hasta el final

    # Convertir la ruta reconstruida en los datos esperados (nodos y reglas)
    for idx in range(len(path) - 1):
        u, v = path[idx]
        next_u, next_v = path[idx + 1]

        # Determinar la dirección basada en la diferencia entre las coordenadas
        if next_u == u - 1 and next_v == v:  # West
            Rules.append('R1')
        elif next_u == u + 1 and next_v == v:  # East
            Rules.append('R3')
        elif next_u == u and next_v == v - 1:  # South
            Rules.append('R2')
        elif next_u == u and next_v == v + 1:  # North
            Rules.append('R4')

        Nodes.append((u + 1, v + 1))  # Agregar a los nodos la coordenada ajustada a 1-based

    # Agregar el nodo final a la lista de nodos (último paso de la ruta)
    final_u, final_v = path[-1]
    Nodes.append((final_u + 1, final_v + 1))

def backtrack_path(u, v, distances):
    """Recoge el camino desde la salida hasta el inicio usando la matriz de distancias."""
    global Board, Rules, Nodes

    path = []
    while distances[u][v] != 2:
        path.append((u + 1, v + 1))
        for k in range(4):
            prev_u = u - CX[k]
            prev_v = v - CY[k]
            if (0 <= prev_u < m and 0 <= prev_v < n and
                    distances[prev_u][prev_v] == distances[u][v] - 1):
                u, v = prev_u, prev_v
                break

    # Invertir el camino encontrado para que vaya de inicio a fin
    path.reverse()
    for step in path:
        Rules.append('Backtrack')
        Nodes.append(step)


def print_board():
    """Imprime el tablero de juego con espaciado adicional."""
    global Board, n, m
    rotated_board = rotate_left(Board)  # Rota 90 grados a la izquierda antes de imprimir
    print("    Y, V")
    for y in range(n, 0, -1):  # Invertir para que la Y vaya de n a 1
        print(f"{y:2}   |", end="   ")  # Tres espacios adicionales para la separación vertical
        for x in range(m):  # Valores del laberinto
            num = rotated_board[n - y][x]
            if num >= 100:  # Si el número tiene tres dígitos
                print(f"{num:3}", end="  ")  # Dos espacios después de un número de tres dígitos
            else:
                print(f"{num:2}", end="   ")  # Tres espacios para números de uno o dos dígitos
        print("\n")  # Nueva línea para la siguiente fila con una línea vacía extra para mayor separación vertical
    print("    ", "-" * (5 * m))  # Ajustar longitud de la línea horizontal según el espaciado
    print("      ", end="")
    for x in range(1, m + 1):
        print(f"{x:2}", end="   ")  # Tres espacios adicionales para los números del eje X
    print(" -> X, U")






def main():
    """Función principal."""
    parser = argparse.ArgumentParser(description='Maze solver')
    parser.add_argument('--file', type=str, required=True, help='Path to the maze file')
    parser.add_argument('--start', type=int, nargs=2, help='Starting position as x y')
    parser.add_argument('--variant', type=str, choices=['V1', 'V2', 'V3'], required=True,
                        help='Backtracking variant to use')
    parser.add_argument('--method', type=str, choices=['DFS', 'BFS'], required=True,)
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("The maze file does not exist.")
        return

    global Board, n, m, trial_count, L, Rules, Nodes
    if args.start:
        start_x, start_y = args.start
        start_x = start_x - 1
        start_y = start_y - 1
    else:
        start_x, start_y = 1, 1
    Board = load_maze(args.file)

    n = len(Board)
    print("N= ", n)
    m = len(Board[0])
    print("M= ", m)
    trial_count = 0
    L = 2
    yes = False

    Board = rotate_right(Board)  # Rota 90 grados a la derecha al cargar la matriz

    Board[start_x][start_y] = L
    Rules = []
    Nodes =[]
    Nodes.append((start_x+1, start_y+1))

    print("PART 1. Data")
    print("----------------------")
    print(" 1.1 Labyrinth")
    print_board()
    print(" 1.2 Starting position   X =", start_x + 1, "Y =", start_y + 1, "L =", L)
    print(" 1.3 Backtracking variant", args.variant)

    if args.method == 'DFS':
        print(" 1.4 Method: Depth First Search")
        yes = dbf_search(start_x, start_y, yes, args.variant)
    elif args.method == 'BFS':
        print(" 1.4 Method: Breadth First Search")
        yes = bfs_search(start_x, start_y, yes)

    print("\nPART 3. Results")
    print("----------------------")
    if yes:
        print("3.1. Path exists!")
        print("3.2. Path graphically:")
        print_board()
        print(Board[1][0])
        print("3.3. Rules= ", Rules)
        print("3.4. Nodes= ", Nodes)
    else:
        print("3.1. No path exists.")


if __name__ == '__main__':
    main()