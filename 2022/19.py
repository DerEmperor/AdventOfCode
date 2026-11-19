#!/usr/bin/env python
import os
import re
import sys
import time
from collections import defaultdict
from typing import NamedTuple

original_stdout = sys.stdout


class WrongAnswer(Exception):
    pass


class Blueprint(NamedTuple):
    id: int
    ore_bot: int
    clay_bot: int
    obsidian_bot: tuple[int, int]
    geode_bot: tuple[int, int]


def get_input(test: bool) -> list[Blueprint]:
    blueprints = []
    filename = 'inputs/19_test.txt' if test else 'inputs/19.txt'
    re_blueprint = re.compile(
        r"Blueprint (\d+): "
        r"Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. "
        r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
        r"Each geode robot costs (\d+) ore and (\d+) obsidian.\n"
    )
    with open(filename, 'r') as file:
        input_ = file.readlines()
        for line in input_:
            g = [int(x) for x in re_blueprint.fullmatch(line).groups()]
            id_, ore_ore, clay_ore, obsidian_ore, obsidian_clay, geode_ore, geode_obsidian = g
            blueprint = Blueprint(
                id=id_,
                ore_bot=ore_ore,
                clay_bot=clay_ore,
                obsidian_bot=(obsidian_ore, obsidian_clay),
                geode_bot=(geode_ore, geode_obsidian),
            )
            blueprints.append(blueprint)

    return blueprints


def solve(bp: Blueprint, max_time: int) -> int:
    bots = (1, 0, 0, 0)
    resources = (0, 0, 0, 0)
    minute = 0
    todo = [(bots, resources, minute)]
    max_ore_bots = max(bp.ore_bot, bp.clay_bot, bp.obsidian_bot[0], bp.geode_bot[0])
    max_clay_bots = bp.obsidian_bot[1]
    # there is never a reason to stockpile more than the most expensive single purchase,
    # except to bank for later minutes (the real cap is scaled by minutes left)
    max_ore = max_ore_bots
    max_clay = max_clay_bots
    max_obsidian = bp.geode_bot[1]
    # dominance memo: per bot set, the Pareto frontier of expanded (minute, resources)
    frontier: dict[tuple[int, int, int, int], list] = defaultdict(list)
    res = 0
    while todo:
        state = todo.pop()
        bots, resources, minute = state
        ore, clay, obsidian, geode = resources

        if minute >= max_time:
            res = max(res, geode)
            continue

        # dominance: prune if, for the same bot set, we already expanded a state that
        # arrived no later and holds at least as many of every resource.
        states = frontier[bots]
        if any(
                seen_minute <= minute and all(seen >= new for seen, new in zip(seen_res, resources))
                for seen_minute, seen_res in states
        ):
            continue
        # drop states this one dominates, then record it
        states[:] = [
            (seen_minute, seen_res) for seen_minute, seen_res in states
            if not (minute <= seen_minute
                    and all(new >= seen for new, seen in zip(resources, seen_res)))
        ]
        states.append((minute, resources))

        # even if we build a geode bot each minute, are we still on track for the best?
        remaining = max_time - minute
        potential = geode + remaining * bots[3] + remaining * (remaining - 1) // 2
        if potential <= res:
            continue

        options = []
        # build bots
        # geode
        if ore >= bp.geode_bot[0] and obsidian >= bp.geode_bot[1]:
            options.append((
                (ore - bp.geode_bot[0], clay, obsidian - bp.geode_bot[1], geode),
                (bots[0], bots[1], bots[2], bots[3] + 1),
            ))
        else:
            # always build the geode bot
            # ore
            if ore >= bp.ore_bot and bots[0] <= max_ore_bots:
                options.append((
                    (ore - bp.ore_bot, clay, obsidian, geode),
                    (bots[0] + 1, bots[1], bots[2], bots[3]),
                ))
            # clay
            if ore >= bp.clay_bot and bots[1] <= max_clay_bots:
                options.append((
                    (ore - bp.clay_bot, clay, obsidian, geode),
                    (bots[0], bots[1] + 1, bots[2], bots[3]),
                ))
            # obsidian
            if ore >= bp.obsidian_bot[0] and clay >= bp.obsidian_bot[1]:
                options.append((
                    (ore - bp.obsidian_bot[0], clay - bp.obsidian_bot[1], obsidian, geode),
                    (bots[0], bots[1], bots[2] + 1, bots[3]),
                ))
            # no build
            options.append((resources, bots))

        # dfs
        next_minute = minute + 1
        # you may only buy once per minute, so nothing above
        # (max single cost) * (purchases left) can ever be spent
        minutes_left = max_time - next_minute
        cap_ore = max_ore * minutes_left
        cap_clay = max_clay * minutes_left
        cap_obsidian = max_obsidian * minutes_left
        for next_resources, next_bots in reversed(options):
            next_resources = (
                min(next_resources[0] + bots[0], cap_ore),
                min(next_resources[1] + bots[1], cap_clay),
                min(next_resources[2] + bots[2], cap_obsidian),
                next_resources[3] + bots[3],
            )
            todo.append((next_bots, next_resources, next_minute))
    return res


def main(test: bool):
    blueprints = get_input(test)

    sum1 = 0
    sum2 = 1
    for blueprint in blueprints:
        sum1 += blueprint.id * solve(blueprint, 24)

    for blueprint in blueprints[:3]:
        sum2 *= solve(blueprint, 32)

    sys.stdout = original_stdout  # enable print
    print('part1:', sum1)
    if sum1 not in [33, 1834]:
        raise WrongAnswer('part1')
    print('part2:', sum2)
    if sum2 not in [56 * 62, 2240]:
        raise WrongAnswer('part2')


if __name__ == '__main__':
    startTime = time.time()

    try:
        print('Test')
        main(True)
        print('real')
        sys.stdout = open(os.devnull, 'w')  # suppress test prints
        main(False)

    finally:
        executionTime = (time.time() - startTime)

        if executionTime < 60:
            print(f'Execution time: {round(executionTime * 1000, 3)}  ms')
        else:
            print(f'Execution time: {round(executionTime, 3)} s')
