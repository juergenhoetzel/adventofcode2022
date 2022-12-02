from pathlib import Path


INPUT_FILE = "input1.txt"
elf_foods = [
    sum([int(line) for line in section.splitlines() if line])
    for section in Path(INPUT_FILE).read_text().split("\n\n")
]
part1 = max(elf_foods)
part2 = sum(sorted(elf_foods, reverse=True)[:3])
print(f"Part1: {part1}")
print(f"Part2: {part2}")
