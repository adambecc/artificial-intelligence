class Tower:
    def __init__(self, name):
        self.name = name
        self.disks = []

    def add_disk(self, disk):
        self.disks.append(disk)

    def peek(self):
        return self.disks[-1] if self.disks else -1

    def remove_top(self):
        if not self.disks:
            return False
        self.disks.pop()
        return True

    def empty(self):
        return len(self.disks) == 0

    def __str__(self):
        return f"{self.name}=({','.join(map(str, self.disks))})"


def move_disks(n, source, destination, auxiliary, move_count):
    if n == 1:
        disk = source.peek()
        source.remove_top()
        destination.add_disk(disk)
        move_count[0] += 1
        print(f"{move_count[0]}. Move disk {disk} from {source.name} to {destination.name}. "
              f"{source}, {auxiliary}, {destination}.")
        return

    move_disks(n - 1, source, auxiliary, destination, move_count)
    move_disks(1, source, destination, auxiliary, move_count)
    move_disks(n - 1, auxiliary, destination, source, move_count)


def solve_hanoi(n):
    if n < 1 or n > 10:
        print("Error: n must be between 1 and 10")
        return

    print(f"n = {n}")

    a, b, c = Tower('A'), Tower('B'), Tower('C')
    for i in range(n, 0, -1):
        a.add_disk(i)

    print(f"Initial state: {a}, {b}, {c}.")

    move_count = [0]  # Using a list to pass by reference
    move_disks(n, a, c, b, move_count)


if __name__ == "__main__":
    n = int(input("Enter number of disks (1-10): "))
    solve_hanoi(n)
