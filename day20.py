from pathlib import Path

xs = [int(line) for line in Path("input20.txt").read_text().splitlines()]


def decrypt(cs: list[int]):
    n = len(cs)
    ret = [(c, False) for c in cs]
    count = 0
    while count < n:
        for i in range(n):
            c, visited = ret[i]
            if not visited:
                if c == 0:
                    ret[i] = (c, True)
                    count += 1
                    break
                target = (i + c) % (n - 1)
                ret.pop(i)
                if target == 0:  # wrap arround
                    ret.append((c, True))
                else:
                    ret.insert(target, (c, True))
                count += 1
                break
    return [x for x, _ in ret]


plain = decrypt(xs)
i = plain.index(0)
coord_sum = sum([plain[(i + offset) % len(plain)] for offset in (1000, 2000, 3000)])

print(f"Part1: {coord_sum}")
