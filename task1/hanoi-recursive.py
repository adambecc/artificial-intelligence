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


def move_disks(n, source, destination, auxiliary, move_count, towers):
    if n == 1:
        disk = source.peek()
        source.remove_top()
        destination.add_disk(disk)
        move_count[0] += 1
        print(f"{str(move_count[0]).zfill(4)}. Move disk {disk} from {source.name} to {destination.name}. "
              f"{towers['A']}, {towers['B']}, {towers['C']}.")
        return

    move_disks(n - 1, source, auxiliary, destination, move_count, towers)
    move_disks(1, source, destination, auxiliary, move_count, towers)
    move_disks(n - 1, auxiliary, destination, source, move_count, towers)


def solve_hanoi(n):
    if n < 1 or n > 10:
        print("Error: n must be between 1 and 10")
        return

    print(f"n = {n}")

    towers = {'A': Tower('A'), 'B': Tower('B'), 'C': Tower('C')}
    for i in range(n, 0, -1):
        towers['A'].add_disk(i)

    print(f"Initial state: {towers['A']}, {towers['B']}, {towers['C']}.")

    move_count = [0]  
    move_disks(n, towers['A'], towers['C'], towers['B'], move_count, towers)


if __name__ == "__main__":
    n = int(input("Enter number of disks (1-10): "))
    solve_hanoi(n)