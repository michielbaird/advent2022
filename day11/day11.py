import sys
import re
from typing import Dict, List, Tuple

p_operation = re.compile(r"^new = (old|\-?\d+) ([\+\-\*]) (old|\-?\d+)$")


def parse_token(token, value):
    if token == "old":
        return value
    else:
        return int(token)

def eval(operation, value):
    m = p_operation.match(operation)
    operand = m.group(2)
    if operand == "+":
        f = lambda l, r: l + r
    elif operand == "-":
        f = lambda l, r: l - r
    elif operand == "*":
        f = lambda l, r: l * r
    return f(parse_token(m.group(1), value), parse_token(m.group(3), value))
        

class Monkey:
    def __init__(self, id, items, operation, test, pass_mon, fail_mon):
        self.id = id
        self.items = items
        self.operation = operation
        self.test = test
        self.pass_mon = pass_mon
        self.fail_mon = fail_mon
        self.inspections = 0
    
    def play_turn(self) -> List[Tuple[int, int]]:
        result = []
        for item in self.items:
            new = eval(self.operation, item) // 3
            self.inspections += 1
            if new % self.test == 0:
                n = self.pass_mon
            else:
                n = self.fail_mon
            result.append((n, new))
        self.items = []
        return result

    
    def __repr__(self) -> str:
        return \
f"""Monkey {self.id}:
    Items: {self.items}
    Operation: {self.operation}
    Test: {self.test}
        Pass: {self.pass_mon}
        Fail: {self.fail_mon}
    Inspections: {self.inspections}
"""

def monkey_builder(raw_monkey: str) -> 'Monkey':
    parts = raw_monkey.split("\n")
    id = int(parts[0].split(" ")[-1][:-1])
    raw_items = parts[1].split(": ")[1]
    if raw_items == "":
        items = []
    else:
        items = [int(x)  for x in raw_items.split(", ")]
    operation = parts[2].split(": ")[1]
    test = int(parts[3].split(" ")[-1])
    pass_mon = int(parts[4].split(" ")[-1])
    fail_mon = int(parts[5].split(" ")[-1])
    return Monkey(
        id,
        items,
        operation,
        test,
        pass_mon,
        fail_mon
    )

def parse_input(raw: str) -> Dict[int, 'Monkey']:
    result = {}
    for x in raw.split("\n\n"):
        monk = monkey_builder(x)
        result[monk.id] = monk
    return result

def main():
    monkeys = parse_input(sys.stdin.read())
    n = len(monkeys)
    for round in range(20):
        for i in range(n):
            to_move = monkeys[i].play_turn()
            for (monkey, val) in to_move:
                monkeys[monkey].items.append(val)
    l_monkeys = list(monkeys.values())
    l_monkeys.sort(key=lambda m: -m.inspections)
    print(monkeys)
    print(l_monkeys[0].inspections * l_monkeys[1].inspections)





if __name__ == "__main__":
    main()