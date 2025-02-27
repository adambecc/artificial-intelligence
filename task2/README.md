# 1. Run_test()
 
n: size of the chessboard(n x n)
start_x, start_y: the starting position of the knight
test_num: the number of the test (7 cases)
short_f: the file object where shorter output will be writter (out-short.txt)
long_f: the file object where more detailed output will be written (out-long.txt)
 
# 2. Setting up the board
 
board = [[0] * (n + 2) for _ in range(n + 2)]

this creates an n+2 by n+2 board
the board is initialized with all zeros

# 3. Movement directions

cx = [2, 1, -1, -2, -2, -1, 1, 2]
cy = [1, 2, 2, 1, -1, -2, -2, -1]

these arrays represent the 8 possible moves of a knight on a chessboard in terms of X and Y direction. Knowing that the night moves in L shape

# 4. Part 1 displays test information

- size of the board
- the initial position of the knight (start_x, start_y)

(this information is printed on the terminal and also displayed on both text files that are generated later)

# 5. Knights movement (try_move function)

- recursion: it tries all possible moves in 8 directions until it finds the valid path
- backtracking: if it cant find a valid move (the knight is stuck), it backtracks by marking the current square as unvisited
- terminating condition: if the knight has covered all n*n squares, the algorithm stops and reports success.

## The trace of each move is printer to long_f showing:

- whether the move is free (valid and unvisited)
- "thread" (already visited)
- "out" (out of bounds)
- "backtrack" (if the knight backtracks to previous positions)

# 6. Result

- if a valid path is found, it prints the total number of trials and the board with the knights path
- if no valid path exists, it prints a message indicating failure

# 7. Main function

- defines several test cases with different n, start_x, start_y
- clears the output files out-short.txt and out-long.txt before starting
- loops through each test case, calling run_test() for each one

# Conclusion:

- The program is designed to solve the knights tour problem for various board sizes (n x n), starting positions, and outputs the results in a structured format
- It handles file I/O, prints detailed traces of the knights moves, and writes the results to two files (out-short.txt and out-long.txt)
