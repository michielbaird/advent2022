import re
import sys
from dataclasses import dataclass, replace, astuple
from typing import Tuple
from functools import reduce
import multiprocessing



@dataclass
class Blueprint:
    id: int
    ore_cost: int
    clay_cost: int
    obsidian_cost: Tuple[int, int]
    geode_cost: Tuple[int, int]

@dataclass
class DpState:
    ore: int
    clay: int
    obsidian: int
    robotOre: int
    robotClay: int
    robotObsidian: int
    robotGeode: int

TOTAL_TIME = 32

p = re.compile(r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.")
def decode_blueprint(raw):
    m = p.match(raw)
    return Blueprint(
        int(m.group(1)),
        int(m.group(2)),
        int(m.group(3)),
        (int(m.group(4)), int(m.group(5))),
        (int(m.group(6)), int(m.group(7)))
    )

def solve_blueprint2(blueprint: Blueprint, total_time):
    # State:
    # (ore, clay, obsidian, robotOre, robotClay, robotObsidian) -> max(robotGeode)
    max_ore = max(blueprint.clay_cost, blueprint.ore_cost, blueprint.obsidian_cost[0], blueprint.geode_cost[0])
    max_clay = blueprint.obsidian_cost[1]
    max_obsidian = blueprint.geode_cost[1]
    #rows = []
    dp = {(0, 0, 0, 1, 0, 0, 0): 0}
    for t in range(total_time):
        next_dp = {}
        max_spend_ore = (total_time - t - 1)*(max_ore)
        max_spend_clay = (total_time - t - 1)*(max_clay)
        max_spend_obsidian = (total_time - t -1)*(max_obsidian)
        print(str(t), end=", ", flush=True)

        for state, geodes in dp.items():
            state = DpState(*state)
            next_state = replace(state)

            next_state.ore = min(next_state.ore + state.robotOre, max_spend_ore)
            next_state.clay = min(next_state.clay + state.robotClay, max_spend_clay)
            next_state.obsidian = min(next_state.obsidian + state.robotObsidian, max_spend_obsidian)

            next_geodes = geodes + state.robotGeode
            next_key = astuple(next_state)
            next_dp[next_key] = max(next_dp.get(next_key, -1), next_geodes)
            
            if state.robotOre < max_ore and state.ore >= blueprint.ore_cost:
                build_ore = replace(next_state)
                build_ore.ore -= blueprint.ore_cost
                build_ore.robotOre += 1
                key_ore = astuple(build_ore)
                next_dp[key_ore] = max(next_dp.get(key_ore, -1), next_geodes)
            if state.robotClay < max_clay and state.ore >= blueprint.clay_cost:
                build_clay = replace(next_state)
                build_clay.ore -= blueprint.clay_cost
                build_clay.robotClay += 1
                key_clay = astuple(build_clay)
                next_dp[key_clay] = max(next_dp.get(key_clay, -1), next_geodes)
            if state.robotObsidian < max_obsidian and state.ore >= blueprint.obsidian_cost[0] and state.clay >= blueprint.obsidian_cost[1]:
                build_obsidian = replace(next_state)
                build_obsidian.ore -= blueprint.obsidian_cost[0]
                build_obsidian.clay -= blueprint.obsidian_cost[1]
                build_obsidian.robotObsidian += 1
                key_obsidian = astuple(build_obsidian)
                next_dp[key_obsidian] = max(next_dp.get(key_obsidian, -1), next_geodes)
            if state.ore >= blueprint.geode_cost[0] and state.obsidian >= blueprint.geode_cost[1]:
                build_geode = replace(next_state)
                build_geode.ore -= blueprint.geode_cost[0]
                build_geode.obsidian -= blueprint.geode_cost[1]
                build_geode.robotGeode += 1
                key_geode = astuple(build_geode)
                next_dp[key_geode] = max(next_dp.get(key_geode, -1), next_geodes)
        dp = next_dp
    #print(dp)
    #print(dp.values())
    print("")
    return max(dp.values())



def main():
    blueprints = [ decode_blueprint(line)  for line in sys.stdin.read().split("\n") ]
    scores = [solve_blueprint2(b, 24)*b.id for b in blueprints]
    print(scores)
    print(sum(scores))
    scores2 = [solve_blueprint2(b,32) for b in blueprints[:3]]
    print(scores2)
    print(reduce(lambda a, b: a*b, scores2))

if __name__ == "__main__":
    main()