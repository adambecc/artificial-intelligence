import os

#os.makedirs("knight", exist_ok=True)

#knights moves (x, y)
cx = [2, 1, -1, -2, -2, -1, 1, 2]
cy = [1, 2, 2, 1, -1, -2, -2, -1]

test_num = 0

def run_test(n, start_x, start_y ): #, test_num
    #convert start positions to 0-based
    startX = start_x - 1
    startY = start_y - 1
    N = n
    board = [[0] * N for _ in range(N)]
    board[startX][startY] = 1
    traceCount = 0

    #output
    #short_filename = f"out-short-{test_num}.txt"
    #long_filename = f"out-long-{test_num}.txt"

    short_filename = f"out-short-.txt"
    long_filename = f"out-long-.txt"

    with open(short_filename, "w") as short_f, open(long_filename, "w") as long_f:
        #PART 1: Data
        part1 = [
            f"PART 1. Data",
            f"1) Board: {n}x{n}.",
            f"2) Initial position: X={start_x}, Y={start_y}. L=1."
        ]
        print("\n".join(part1))
        print("\n".join(part1), file=short_f)
        print("\n".join(part1), file=long_f)
        long_f.write("PART 2. Trace\n")

        #personal 
        """
        def print_trace(L, direction, u, v, action):
            nonlocal traceCount
            if action != "Backtrack":
                traceCount += 1
            line = f"   {traceCount}) " + "-" * (L-2) + f"R{direction}. U={u+1}, V={v+1}. L={L}. {action}."
            if action == "Free":
                line += f" BOARD[{u+1},{v+1}] := {L}."
            if action == "Backtrack":
                line += " Backtrack."
            line += "\n"
            long_f.write(line)
        """
        #class version
        def print_trace(L, direction, u, v, action):
            nonlocal traceCount
            if action != "Backtrack":
                traceCount += 1
            line = f"   {traceCount:>10}) " + "-" * (L-2) + f"R{direction}. U={u+1}, V={v+1}. L={L}. {action}."
            if action == "Free":
                line += f" BOARD[{u+1},{v+1}] := {L}."
            if action == "Backtrack":
                line += " Backtrack."
            line += "\n"
            long_f.write(line)

        #recursive backtracking function
        def try_move(L, x, y):
            for k in range(8):
                newX = x + cx[k]
                newY = y + cy[k]
                direction = k + 1

                if newX < 0 or newX >= N or newY < 0 or newY >= N:
                    print_trace(L, direction, newX, newY, "Out")
                    continue

                if board[newX][newY] != 0:
                    print_trace(L, direction, newX, newY, "Thread")
                    continue

                board[newX][newY] = L
                print_trace(L, direction, newX, newY, "Free")

                if L == N * N or try_move(L + 1, newX, newY):
                    return True

                board[newX][newY] = 0
                print_trace(L, direction, newX, newY, "Backtrack")

            return False

        success = try_move(2, startX, startY)

        #PART 3: Results
        part3 = []
        trials = traceCount  #line count

        if success:
            part3.append(f"1) Path is found. Trials={trials}.")
            part3.append("2) Path graphically:")
            part3.append(" Y, V ^")
            for i in range(N - 1, -1, -1):
                row = " ".join(f"{board[j][i]:3}" for j in range(N))
                part3.append(f"   {i+1} | " + row)
            part3.append(" " * 6 + "-" * (4 * N + 5) + "> X, U")
            x_axis = " " * 8 + " ".join(f"{j+1:3}" for j in range(N))
            part3.append(x_axis)
        else:
            part3.append(f"Path does not exist. Trials={trials}.")
            #part3.append(f"Path does not exist. Trials={str(trials).zfill(3)}.")


        part3_str = "\n".join(part3)
        print(part3_str)
        print(part3_str, file=short_f)
        print(part3_str, file=long_f)
        print(" ")

def main():

    #asking for the test number is way better
    

    """
    tests = [
        (5, 1, 1),
        (5, 5, 1),
        (5, 1, 5),
        (5, 2, 1),
        (6, 1, 1),
        (7, 1, 1),
        (4, 1, 1)
    ]

    for i, (n, x, y) in enumerate(tests, 1):
        run_test(n, x, y, i)
    """

    #run test by test:
    #test_n = int(input("Enter the number of the test: "))
    n = int(input("Enter the size of the board (NxN): "))
    start_x = int(input("Enter the starting X position (1-N): "))
    start_y = int(input("Enter the starting Y position (1-N): "))
    run_test(n, start_x, start_y) #, test_n

if __name__ == "__main__":
    main()