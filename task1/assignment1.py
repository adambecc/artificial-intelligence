class Tower:
    def __init__(self, name):
        self.name = name
        self.disks = []
    
    def add_disk(self, disk):
        self.disks.append(disk)
    
    def peek(self):
        return -1 if not self.disks else self.disks[-1]
    
    def remove_top(self):
        if not self.disks:
            return False
        self.disks.pop()
        return True
    
    def is_empty(self):
        return not bool(self.disks)
    
    def __str__(self):
        return f"{self.name}=({','.join(map(str, self.disks))})"

def solve_hanoi(n):
    if not isinstance(n, int) or n < 1 or n > 10:
        print("Error: n must be between 1 and 10")
        return

    print(f"n = {n}")

    # Initialize towers
    a, b, c = Tower('A'), Tower('B'), Tower('C')
    for i in range(n, 0, -1):
        a.add_disk(i)

    towers = [a, b, c]
    names = ['A', 'B', 'C']

    # Print initial state
    print(f"Initial state: {a}, {b}, {c}.")

    total_moves = (1 << n) - 1  # 2^n - 1
    move_count = 0
    clockwise = (n % 2 == 0)
    prev_source = None

    while move_count < total_moves:
        moved = False

        # Try each tower as source
        for i in range(3):
            source_name = names[i]
            source = towers[i]

            if source.is_empty() or source_name == prev_source:
                continue

            disk = source.peek()

            # Try moving in the specified direction
            for j in range(1, 3):
                dest_idx = (i + j) % 3 if clockwise else (i - j + 3) % 3
                dest = towers[dest_idx]
                dest_name = names[dest_idx]

                # Check if move is legal
                if dest.is_empty() or dest.peek() > disk:
                    move_count += 1
                    source.remove_top()
                    dest.add_disk(disk)
                    
                    print(f"{move_count}. Move disk {disk} from {source_name} to {dest_name}. "
                          f"{a}, {b}, {c}.")

                    prev_source = dest_name
                    moved = True
                    break
            
            if moved:
                break

if __name__ == "__main__":
    try:
        n = int(input("Enter number of disks (1-10): "))
        solve_hanoi(n)
    except ValueError:
        print("Please enter a valid integer.")