"""

def run_test(n, start_x, start_y, test_num):
    short_filename = f"out-short-{test_num}.txt"
    long_filename = f"out-long-{test_num}.txt"

    with open(short_filename, "w") as short_f, open(long_filename, "w") as long_f:
        board = [[0] * (n + 2) for _ in range(n + 2)]  # 1-based to n
        cx = [2, 1, -1, -2, -2, -1, 1, 2]
        cy = [1, 2, 2, 1, -1, -2, -2, -1]
        trials = 0
        success = False
        max_moves = n * n

        part1 = [
            f"PART 1. Data",
            f"1) Board: {n}x{n}.",
            f"2) Initial position: X={start_x}, Y={start_y}. L=1."
        ]
        print("\n".join(part1))
        print("\n".join(part1), file=short_f)
        print("\n".join(part1), file=long_f)
        long_f.write("PART 2. Trace\n")

        board[start_x][start_y] = 1

        def try_move(L, x, y, depth):
            nonlocal trials, success
            for k in range(8):
                trials += 1
                rule = k + 1
                u = x + cx[k]
                v = y + cy[k]
                hyphens = '-' * (depth - 1)
                trace_line = f"{hyphens}R{rule}. U={u}, V={v}. L={L}."

                if 1 <= u <= n and 1 <= v <= n:
                    if board[u][v] == 0:
                        board[u][v] = L
                        trace_line += f" Free. BOARD[{u},{v}]:={L}."
                        if L < max_moves:
                            try_move(L + 1, u, v, depth + 1)
                            if not success:
                                board[u][v] = 0
                                trace_line += " Backtrack."
                        else:
                            success = True
                    else:
                        trace_line += " Thread."
                else:
                    trace_line += " Out."
                print(trace_line, file=long_f)
                if success:
                    break

        if n >= 1 and 1 <= start_x <= n and 1 <= start_y <= n:
            try_move(2, start_x, start_y, 1)

        print("PART 3. Results")
        part3 = []
        if success:
            part3.append(f"1) Path is found. Trials={trials}.")
            part3.append("2) Path graphically:")
            part3.append("Y, V ^")
            for v in range(n, 0, -1):
                row = [f"{board[u][v]:2}" for u in range(1, n + 1)]
                part3.append(f"{v} | " + " ".join(row))
            part3.append("  " + "-" * (4 * n) + "> X, U")
            x_axis = "    " + "   ".join(str(u) for u in range(1, n + 1))
            part3.append(x_axis)
        else:
            part3.append(f"Path does not exist. Trials={trials}.")

        part3_str = "\n".join(part3)
        print(part3_str)
        print(part3_str, file=short_f)
        print(part3_str, file=long_f)

        print(" ")

def main():
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

if __name__ == "__main__":
    main()

"""