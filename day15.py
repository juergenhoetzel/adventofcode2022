from pathlib import Path
from dataclasses import dataclass
from functools import reduce
import re

SB_PATTERN = re.compile(
    r"^Sensor at x=(-?[0-9]+), y=(-?[0-9]+): closest beacon is at x=(-?[0-9]+), y=(-?[0-9]+)$"
)


@dataclass(frozen=True)
class Sensor:
    x: int
    y: int
    distance: int


@dataclass(frozen=True)
class Beacon:
    x: int
    y: int


beacons: set[Beacon] = set()
sensors: set[Sensor] = set()


def merge_ranges(ranges):
    ret = [ranges[0]]
    for low, up in ranges[1:]:
        if low - 1 <= ret[-1][1]:
            ret[-1] = ret[-1][0], max(ret[-1][1], up)
        else:
            ret.append((low, up))
    return ret


for line in Path("input15.txt").read_text().splitlines():
    sx, sy, bx, by = [int(x) for x in SB_PATTERN.match(line).groups()]
    distance = abs(sx - bx) + abs(sy - by)
    sensors.add(Sensor(sx, sy, distance))
    beacons.add(Beacon(bx, by))

Y = 2000000


def get_ranges(sensors, y=Y):
    ranges = []
    for sensor in sensors:
        x_len = sensor.distance - abs(sensor.y - y)
        if x_len > 0:
            if sensor.y == y:
                ranges.append((sensor.x - x_len, sensor.x - 1))
                ranges.append((sensor.x + 1, sensor.x + x_len))
            else:
                ranges.append((sensor.x - x_len, sensor.x + x_len))
    ranges.sort()
    ranges = merge_ranges(ranges)
    return ranges


ranges = get_ranges(sensors, Y)
free = reduce(lambda acc, r: acc + r[1] - r[0], ranges, 0)
print(f"Part1: {free}")

MAX_Y = 4000000

# Brute Force :-(
def get_positions(sensors, max_y=MAX_Y):
    for y in range(0, max_y):
        ranges = get_ranges(sensors, y)
        if len(ranges):
            for r1, r2 in zip(ranges, ranges[1:]):
                for x in range(r1[1] + 1, r2[0]):
                    if (
                        x >= 0
                        and x < max_y
                        and x not in (sensor.x for sensor in sensors if sensor.y == y)
                        and x not in (beacon.x for beacon in beacons if beacon.y == y)
                    ):
                        yield (y, x)


(y, x) = next(get_positions(sensors, MAX_Y))
frequency = y + x * 4000000
print(f"Part2: {frequency}")
