import argparse
import sys
from typing import List, Tuple

LAB = []
CX = [-1, 0, 1, 0]  #West, South, East, North
CY = [0, -1, 0, 1]
M, N = 0, 0
X, Y = 0, 0
L = 2
TRIAL = 0
MarkOnBacktrack = -1
Depth = 0
found = False
output_lines = []
trial_counter = 0

def add_output(line: str, to_console: bool = False):
    """Add line to output and optionally print to console"""
    output_lines.append(line)
    if to_console:
        print(line)

def read_labyrinth_from_terminal():
    """Read labyrinth from terminal input"""
    global LAB, M, N, X, Y
    print("Enter labyrinth dimensions M (columns) and N (rows):")
    M, N = map(int, input().split())
    print("Enter starting position X Y (1-based coordinates):")
    X, Y = map(int, input().split())
    X -= 1
    Y -= 1
    
    print(f"Enter {N} rows (bottom to top), each with {M} numbers (space separated):")
    LAB = []
    for _ in range(N):
        row = list(map(int, input().split()))
        if len(row) != M:
            raise ValueError("Row length doesn't match columns")
        LAB.insert(0, row)
    
    if LAB[Y][X] != 2:
        print("Warning: Starting position not marked with 2")

def read_labyrinth_from_file(filename: str):
    global LAB, M, N, X, Y
    with open(filename, 'r') as f:
        dimensions = f.readline().strip().split()
        M, N = int(dimensions[0]), int(dimensions[1])
        
        start_pos = f.readline().strip().split()
        X, Y = int(start_pos[0])-1, int(start_pos[1])-1 
        
        rows = []
        for _ in range(N):
            row = list(map(int, f.readline().strip().split()))
            if len(row) != M:
                raise ValueError(f"Row length mismatch in {filename}")
            rows.append(row)
        
        LAB = rows[::-1]
        
        if LAB[Y][X] != 2:
            print(f"Warning: Starting position at ({X+1},{Y+1}) not marked with 2")

def print_labyrinth(to_console: bool = False):
    """Print the labyrinth with current state"""
    add_output("\nY, V", to_console)
    add_output("^", to_console)
    for j in reversed(range(N)):
        add_output(f"{j+1:2} | " + " ".join(f"{LAB[j][i]:2}" for i in range(M)), to_console)
    add_output("-------------------------------> X, U", to_console)
    add_output("    " + " ".join(f"{i+1:2}" for i in range(M)), to_console)

def get_indentation() -> str:
    return "-" * (Depth - 1)

def format_trial_number(num: int) -> str:
    """Format trial number with 3 characters width"""
    return f"{num:3}"

def dfs(x: int, y: int) -> bool:
    global LAB, L, TRIAL, found, Depth, trial_counter
    
    if found:
        return True
    
    Depth += 1
    current_indent = get_indentation()
    
    if x == 0 or x == M-1 or y == 0 or y == N-1:
        trial_counter += 1
        add_output(f"{format_trial_number(trial_counter)}) {current_indent}R1. U={x+1}, V={y+1}. Terminal.")
        found = True
        Depth -= 1
        return True
    
    for k in range(4):
        dx, dy = CX[k], CY[k]
        nx, ny = x + dx, y + dy
        trial_counter += 1
        formatted_num = format_trial_number(trial_counter)
        rule_output = f"{formatted_num}) {current_indent}R{k+1}. U={nx+1}, V={ny+1}"
        
        if nx < 0 or nx >= M or ny < 0 or ny >= N:
            add_output(f"{formatted_num}) {current_indent}R{k+1}. U={nx+1}, V={ny+1}. Out of bounds")
            trial_counter -= 1 
            continue
        
        if LAB[ny][nx] == 0:
            L += 1
            LAB[ny][nx] = L
            add_output(f"{formatted_num}) {current_indent}R{k+1}. U={nx+1}, V={ny+1}. Free. L:=L+1={L}. LAB[{ny+1},{nx+1}]:={L}.")
            
            if dfs(nx, ny):
                Depth -= 1
                return True
            
            add_output(f"{' ' * 5}{current_indent}Backtrack from X={nx+1}, Y={ny+1}, L={L}. LAB[{ny+1},{nx+1}]:={MarkOnBacktrack}. L:=L-1={L-1}")
            LAB[ny][nx] = MarkOnBacktrack
            L -= 1
        elif LAB[ny][nx] == 1:
            add_output(f"{formatted_num}) {current_indent}R{k+1}. U={nx+1}, V={ny+1}. Wall")
        else:
            add_output(f"{formatted_num}) {current_indent}R{k+1}. U={nx+1}, V={ny+1}. Thread")

    Depth -= 1
    return False

def reconstruct_path() -> Tuple[List[Tuple[int, int]], str]:
    """Reconstruct the found path and rules"""
    path = []
    max_l = max(max(row) for row in LAB)
    
    for l in range(2, max_l + 1):
        for y in range(N):
            for x in range(M):
                if LAB[y][x] == l:
                    path.append((x, y))
                    break
    
    rules = []
    for i in range(1, len(path)):
        px, py = path[i-1]
        cx, cy = path[i]
        dx = cx - px
        dy = cy - py
        
        for k in range(4):
            if dx == CX[k] and dy == CY[k]:
                rules.append(f"R{k+1}")
                break
    
    return path, " ".join(rules)

def write_output_to_file(filename: str):
    """Write all output to file"""
    with open(filename, 'w') as f:
        f.write("\n".join(output_lines))

def main():
    global MarkOnBacktrack, found, output_lines, trial_counter
    
    parser = argparse.ArgumentParser(description="Labyrinth solver with depth-first search")
    parser.add_argument("--variant", type=int, choices=[1, 2], required=True,
                       help="Algorithm variant: 1=V1 (-1 marks), 2=V2 (0 marks)")
    parser.add_argument("--file", type=str,
                       help="Input file (if not provided, read from terminal)")
    parser.add_argument("--output", type=str, default="output.txt",
                       help="Output file name (default: output.txt)")
    
    args = parser.parse_args()

    MarkOnBacktrack = -1 if args.variant == 1 else 0

    if args.file:
        try:
            read_labyrinth_from_file(args.file)
        except Exception as e:
            print(f"Error reading labyrinth file: {e}")
            sys.exit(1)
    else:
        try:
            read_labyrinth_from_terminal()
        except Exception as e:
            print(f"Error reading labyrinth: {e}")
            sys.exit(1)

    if LAB[Y][X] != 2:
        print(f"Marking starting position at ({X+1},{Y+1}) with 2")
        LAB[Y][X] = 2

    sys.setrecursionlimit(10000)

    add_output("PART 1. Data", True)
    add_output("1.1. Labyrinth", True)
    print_labyrinth(True)
    add_output(f"1.2. Initial position X={X+1}, Y={Y+1}. L={L}.", True)

    add_output("\nPART 2. Trace")
    add_output(f"Starting search (Variant {args.variant})...", False)
    success = dfs(X, Y)

    add_output("\nPART 3. Results", True)
    if success:
        add_output("3.1. Path is found.", True)
        add_output("3.2. Path graphically:", True)
        print_labyrinth(True)
        
        path, rules = reconstruct_path()
        add_output(f"3.3. Rules: {rules}.", True)
        
        path_str = "3.4. Nodes: " + ", ".join([f"[X={x+1},Y={y+1}]" for x, y in path])
        
        max_line_length = 80
        while len(path_str) > max_line_length:
            split_pos = path_str[:max_line_length].rfind(',')
            if split_pos == -1:
                break
            add_output(path_str[:split_pos + 1], True)
            path_str = "        " + path_str[split_pos + 1:].lstrip()
        add_output(path_str, True)
    else:
        add_output("3.1. No path exists", True)

    write_output_to_file(args.output)

if __name__ == "__main__":
    main()

# python3 dfs-lab.py --variant 1 --file maze1.txt --output trace1.txt