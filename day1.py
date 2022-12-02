from pathlib import Path


INPUT_FILE = "input1.txt"
elf_foods = [
    sum([int(line) for line in section.splitlines() if line])
    for section in Path(INPUT_FILE).read_text().split("\n\n")
]
print(max(elf_foods))
