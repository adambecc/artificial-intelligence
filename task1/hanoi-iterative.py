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


def solve_hanoi(n):
    if n < 1 or n > 10:
        print("Error: n must be between 1 and 10")
        return

    print(f"n = {n}")

    towers = {'A': Tower('A'), 'B': Tower('B'), 'C': Tower('C')}
    for i in range(n, 0, -1):
        towers['A'].add_disk(i)

    print(f"Initial state: {towers['A']}, {towers['B']}, {towers['C']}.")

    stack = [(n, towers['A'], towers['C'], towers['B'])]
    move_count = 0

    while stack:
        num_disks, source, dest, aux = stack.pop()

        if num_disks == 1:
            disk = source.peek()
            source.remove_top()
            dest.add_disk(disk)
            move_count += 1
            print(f"{str(move_count).zfill(4)}. Move disk {disk} from {source.name} to {dest.name}. "
                  f"{towers['A']}, {towers['B']}, {towers['C']}.")
        else:
            stack.append((num_disks - 1, aux, dest, source))
            stack.append((1, source, dest, aux))
            stack.append((num_disks - 1, source, aux, dest))


if __name__ == "__main__":
    n = int(input("Enter number of disks (1-10): "))
    solve_hanoi(n)