from pathlib import Path
import copy
from operator import attrgetter
from dataclasses import dataclass
from functools import reduce
import re


def zero_cost():
    return 0


ROBOTS_RE = re.compile(
    r"Blueprint ([0-9]+): +Each ore robot costs ([0-9]+) ore\. +Each clay robot costs ([0-9]+) ore. +Each obsidian robot costs ([0-9]+) ore and ([0-9]+) clay\. +Each geode robot costs ([0-9]+) ore and ([0-9]+) obsidian\."
)

ROBOT_TYPES = ["geode", "obsidian", "clay", "ore"]


def build_robot(inventory, blueprint, robottype) -> bool:
    if robottype not in ROBOT_TYPES:
        raise ValueError(f"Invalid type: {robottype}")
    requirements = blueprint.get(robottype)
    new_inventory = {i: inventory.get(i, 0) - n for i, n in requirements.items()}
    if all(v >= 0 for v in new_inventory.values()):
        inventory.update(new_inventory)
        return True
    return False


def harvest(inventory, robots):
    for robot, n in robots.items():
        inventory[robot] = inventory.get(robot, 0) + n


def max_inventory_required(blueprint) -> dict[str, int]:
    ret = {}
    for _, m in blueprint.items():
        for k, v in m.items():
            ret[k] = max(ret.get(k, 0), v)
    return ret


blueprints = {}
for line in Path("input.txt").read_text().strip().splitlines():
    (
        blueprint_no,
        ore_ore,
        clay_ore,
        obsidian_ore,
        obsidian_clay,
        geode_ore,
        geode_obsidian,
    ) = map(int, ROBOTS_RE.match(line).groups())
    ore = {"ore": ore_ore}
    clay = {"ore": clay_ore}
    obsidian = {"ore": obsidian_ore, "clay": obsidian_clay}
    geode = {"ore": geode_ore, "obsidian": geode_obsidian}
    blueprints[blueprint_no] = {
        "ore": ore,
        "clay": clay,
        "obsidian": obsidian,
        "geode": geode,
    }


@dataclass
class State:
    inventory: dict[str, int]
    robots: dict[str, int]
    time: int


def get_max_geodest(blueprint):
    max_map = max_inventory_required(blueprint)
    bfs_queue = [State({}, {"ore": 1}, 1)]
    ret = 0
    while len(bfs_queue):
        state = bfs_queue.pop(0)
        if state.time == 23:
            ret = max(state.inventory.get("geode", 0), ret)
            continue
        new_inventory = copy.deepcopy(state.inventory)
        harvest(state.inventory, state.robots)
        for robot_type in ROBOT_TYPES:
            if robot_type != "geode" and state.inventory.get(
                robot_type, 0
            ) >= max_map.get(robot_type, 0):
                continue  # already enough of this type

            if build_robot(
                new_inventory, blueprint, robot_type
            ):  # dont build in last round
                new_robots = copy.deepcopy(state.robots)

                new_robots[robot_type] = new_robots.get(robot_type, 0) + 1
                bfs_queue.append(State(new_inventory, new_robots, state.time + 1))
                # If a geode machine can be built, it must be built
                break
        harvest(state.inventory, state.robots)
        bfs_queue.append(State(state.inventory, state.robots, state.time + 1))
    print("Finished blueprint", ret)
    return ret


results = [i * get_max_geodest(blueprint) for i, blueprint in blueprints.items()]
print(f"Part1 {sum(results)}")
