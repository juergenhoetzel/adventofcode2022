from pathlib import Path
import re

SIZE_RE = re.compile("([0-9]+) (.*)$")
DIR_RE = re.compile("dir (.*)$")
COMMAND_RE = re.compile(r"(ls|cd )(.*)$")
size = 0
p = Path("/")
sizes = {}
current_command = None

s = Path("input7.txt").read_text()

cmd_outputs = re.split(r"\$ ", s, flags=re.MULTILINE)[1:]

dir_tree = {Path("/"): []}
cur_path = Path("/")

for cmd_output in cmd_outputs:
    cmd_s = cmd_output.splitlines()[0]
    output_lines = cmd_output.splitlines()[1:]
    m = COMMAND_RE.match(cmd_s)
    cmd, arg = m.groups()
    if cmd == "ls":
        if len(dir_tree.get(cur_path, [])):
            raise ValueError(f"{cur_path} entries already exist")
        dir_tree[cur_path] = []
        for output in output_lines:
            if m := SIZE_RE.match(output):
                size, name = int(m.group(1)), m.group(2)
                dir_tree[cur_path].append((size, name))
            elif m := DIR_RE.match(output):
                name = m.group(1)
                dir_tree[cur_path].append((0, name))
            else:
                raise ValueError("Invalid ls line {output}")
    elif cmd == "cd ":
        cur_path = (cur_path / arg).resolve()
        dir_tree[cur_path] = dir_tree.get(cur_path, [])
    else:
        raise ValueError(f"Invalid Command '{cmd}'")


def dir_size(p):
    acc = 0
    for size, name in dir_tree.get(p):
        if size:
            acc += size
        else:
            acc += dir_size(p / Path(name))
    return acc


sum1 = sum([x for p in dir_tree.keys() if (x := dir_size(p)) <= 100_000])

print(f"Part1: {sum1}")

DISK_SIZE = 70000000
used_space = dir_size(Path("/"))
free_space = DISK_SIZE - used_space
to_delete = 30000000 - free_space

min2 = min([x for p in dir_tree.keys() if (x := dir_size(p)) >= to_delete])
print(f"Part2: {min2}")
