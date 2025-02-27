N = 5 
NN = N * N 

CX = [2, 1, -1, -2, -2, -1, 1, 2]
CY = [1, 2, 2, 1, -1, -2, -2, -1]

BOARD = [[0] * N for _ in range(N)]


def print_trace(move, u, v, level, status):
    indent = "-" * level
    print(f"{indent}R{move + 1}. U={u + 1}, V={v + 1}. L={level}. {status}.")


def try_knight(l, x, y, yes, trials):
    """ Backtracking para resolver el Knight's Tour """
    k = 0
    while k < 8 and not yes[0]:
        u, v = x + CX[k], y + CY[k]
        if 0 <= u < N and 0 <= v < N and BOARD[u][v] == 0:
            BOARD[u][v] = l
            trials[0] += 1
            print_trace(k, u, v, l, "Free")
            
            if l < NN:
                try_knight(l + 1, u, v, yes, trials)
                if not yes[0]:
                    BOARD[u][v] = 0  # Retroceso
                    print_trace(k, u, v, l, "Backtrack")
            else:
                yes[0] = True
        k += 1


def solve_knights_tour():
    """ Resolver el Knight's Tour """
    global BOARD
    BOARD = [[0] * N for _ in range(N)]
    BOARD[0][0] = 1
    yes = [False]
    trials = [0]

    print("PART 1. Data")
    print(f"1) Board: {N}x{N}.")
    print("2) Initial position: X=1, Y=1. L=1.")
    print("\nPART 2. Trace")
    
    try_knight(2, 0, 0, yes, trials)
    
    print("\nPART 3. Results")
    if yes[0]:
        print(f"1) Path is found. Trials={trials[0]}.")
        print("2) Path graphically:")
        for row in reversed(BOARD):
            print(" ".join(f"{num:2}" for num in row))
    else:
        print("Path does not exist.")


if __name__ == "__main__":
    solve_knights_tour()