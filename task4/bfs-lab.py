import argparse
from collections import deque
from typing import List, Tuple, Optional

LAB = []
CX = [-1, 0, 1, 0]  # West, South, East, North (R1, R2, R3, R4)
CY = [0, -1, 0, 1]
M, N = 0, 0
X, Y = 0, 0
L = 2
output_lines = []
trial_counter = 0

def add_output(line: str, to_console: bool = False):
    output_lines.append(line)
    if to_console:
        print(line)

def read_labyrinth_from_file(filename: str):
    global LAB, M, N, X, Y
    with open(filename, 'r') as f:
        M, N = map(int, f.readline().split())
        X, Y = map(int, f.readline().split())
        X -= 1
        Y = N - Y
        LAB = [list(map(int, f.readline().split())) for _ in range(N)][::-1]
    LAB[Y][X] = 2 

def print_labyrinth(to_console: bool = False):
    add_output("\nY, V", to_console)
    add_output("^", to_console)
    for j in reversed(range(N)):
        add_output(f"{j+1:2} | " + " ".join(f"{LAB[j][i]:2}" for i in range(M)), to_console)
    add_output("-------------------------------> X, U", to_console)
    add_output("    " + " ".join(f"{i+1:2}" for i in range(M)), to_console)

def bfs(start_x: int, start_y: int) -> Optional[Tuple[List[Tuple[int, int]], str]]:
    global trial_counter, LAB
    parent = [[None for _ in range(M)] for _ in range(N)]
    parent[start_y][start_x] = (-1, -1)
    current_wave = [(start_x, start_y)]
    wave_number = 0
    current_L = 2
    newn_counter = 1 
    found = False
    path = []
    rules = []

    add_output(f"WAVE {wave_number}, label L=\"{current_L}\". Initial position X={start_x+1}, Y={start_y+1}, NEWN=1")

    while current_wave and not found:
        next_wave = []
        if wave_number > 0:
            add_output(f"\nWAVE {wave_number}, label L=\"{current_L}\"")
            add_output(f"    NEWN={len(current_wave)}.")
        
        for close_idx, (x, y) in enumerate(current_wave, 1):
            add_output(f"    Close CLOSE={close_idx}, X={x+1}, Y={y+1}.")
            for k in range(4):
                rule = k + 1
                nx = x + CX[k]
                ny = y + CY[k]

                if nx < 0 or nx >= M or ny < 0 or ny >= N:
                    add_output(f"        R{rule}. X={nx+1}, Y={ny+1}. Wall.")
                    continue
               
                if LAB[ny][nx] == 1:
                    add_output(f"        R{rule}. X={nx+1}, Y={ny+1}. Wall.")
                    continue
               
                if LAB[ny][nx] != 0:
                    add_output(f"        R{rule}. X={nx+1}, Y={ny+1}. CLOSED or OPEN")
                    continue

                if nx == 0 or nx == M-1 or ny == 0 or ny == N-1:
                    LAB[ny][nx] = current_L + 1
                    parent[ny][nx] = (x, y)
                    newn_counter += 1
                    add_output(f"        R{rule}. X={nx+1}, Y={ny+1}. Free. NEWN={newn_counter}")

                    path = []
                    rules = []
                    cx, cy = nx, ny
                    while (cx, cy) != (-1, -1):
                        path.append((cx, cy))
                        px, py = parent[cy][cx]
                        if (px, py) != (-1, -1):
                            dx = cx - px
                            dy = cy - py
                            for dir in range(4):
                                if dx == CX[dir] and dy == CY[dir]:
                                    rules.insert(0, f"R{dir+1}")
                        cx, cy = px, py
                    
                    path = path[:-1]
                    found = True
                    break
                else:
                    LAB[ny][nx] = current_L + 1
                    parent[ny][nx] = (x, y)
                    next_wave.append((nx, ny))
                    newn_counter += 1
                    add_output(f"        R{rule}. X={nx+1}, Y={ny+1}. Free. NEWN={newn_counter}")
            if found:
                break

        if not found:
            current_wave = next_wave
            wave_number += 1
            current_L += 1

    if found:
        return path, ' '.join(rules)
    else:
        return None

def main():
    global LAB, M, N, X, Y, output_lines, trial_counter

    parser = argparse.ArgumentParser(description="Labyrinth solver with BFS")
    parser.add_argument("--file", type=str, required=True, help="Input file")
    parser.add_argument("--output", type=str, default="output_bfs.txt", help="Output file")
    args = parser.parse_args()

    read_labyrinth_from_file(args.file)

    add_output("PART 1. Data", True)
    add_output("1.1. Labyrinth", True)
    print_labyrinth(True)
    add_output(f"1.2. Initial position X={X+1}, Y={Y+1}. L={L}.", True)

    add_output("\nPART 2. Trace \n", True)
    trial_counter = 0
    result = bfs(X, Y)

    add_output("\nPART 3. Results", True)
    if result:
        path, rules = result
        add_output("3.1. Path is found.", True)
        add_output("3.2. Path graphically:", True)
        print_labyrinth(True)
        add_output(f"3.3. Rules: {rules}.", True)
        path_str = "3.4. Nodes: " + ", ".join([f"[X={x+1},Y={y+1}]" for x, y in path])
        max_line_length = 80
        while len(path_str) > max_line_length:
            split_pos = path_str[:max_line_length].rfind(', ')
            if split_pos == -1:
                split_pos = max_line_length
            add_output(path_str[:split_pos], True)
            path_str = "        " + path_str[split_pos+2:]
        add_output(path_str, True)
    else:
        add_output("3.1. No path exists", True)

    with open(args.output, 'w') as f:
        f.write("\n".join(output_lines))

if __name__ == "__main__":
    main()