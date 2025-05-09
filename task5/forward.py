import argparse
import os

def read_data(file_path):
    rules = []
    facts = set()
    goal = None

    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            section = None

            for line in lines:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue

                if line.startswith("1) Rules"):
                    section = "rules"
                    continue
                elif line.startswith("2) Facts"):
                    section = "facts"
                    continue
                elif line.startswith("3) Goal"):
                    section = "goal"
                    continue

                if section == "rules" and line and not line.startswith("//"):
                    line = line.split("//")[0].strip()
                    if ',' in line:
                        result, conditions = map(str.strip, line.split(','))
                        rule = (set(conditions.split()), result)
                        rules.append(rule)

                elif section == "facts" and line:
                    facts.update(line.split())

                elif section == "goal" and line:
                    goal = line.strip()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None, None
    global initial_facts
    initial_facts = set(facts)

    return rules, facts, goal

def forward_chaining_with_trace(rules, facts, goal):
    if goal in facts:
        print("\nPART 3. Results")
        print(f"1) Goal {goal} is already present in the initial facts.")
        print("2) No rules were applied.")
        return True

    inferred_facts = set(facts)
    temp_path = []
    iteration = 1
    applied_rules = set()
    flag2_raised = {}

    print("PART 2. Trace\n")

    while True:
        print(f"ITERATION {iteration}")
        new_fact_added = False

        for i, (conditions, result) in enumerate(rules, start=1):
            rule_name = f"R{i}"

            if not conditions.issubset(inferred_facts):
                missing_conditions = conditions - inferred_facts
                print(f"{rule_name}: not applied, because of lacking {', '.join(missing_conditions)}.")
                continue

            if result not in inferred_facts:
                global initial_facts
                inferred_facts.add(result)
                temp_path.append(rule_name)
                new_fact_added = True
                applied_rules.add(rule_name)
                new_facts = inferred_facts - initial_facts
                print(f"{rule_name}: apply. Raise flag1. Facts: {', '.join(initial_facts)} and {', '.join(new_facts)} .")

                if result == goal:
                    print("\nPART 3. Results")
                    print(f"1) Goal {goal} achieved.")
                    print(f"2) Path {', '.join(temp_path)}.")
                    return True

                break
            else:
                if rule_name in applied_rules:
                    print(f"{rule_name}: skip, because flag1 already rised.")
                else:
                    if rule_name in flag2_raised:
                        print(f"{rule_name}: skip, because flag2 already raised.")
                    else:
                        print(f"{rule_name}: not applied, because RHS is in facts. Raise flag2.")
                        flag2_raised[rule_name] = True
                continue

        if not new_fact_added:
            print("\nPART 3. Results")
            print(f"1) Goal {goal} could not be achieved.")
            print("2) No rules were applied.")
            return False

        print(f"Facts: {', '.join(inferred_facts)}.\n")
        iteration += 1

def print_data(rules, facts, goal):
    print("PART 1. Data\n")
    print("1) Rules")
    for i, rule in enumerate(rules, start=1):
        conditions, result = rule
        conditions_str = ', '.join(conditions)
        print(f"R{i}: {conditions_str} -> {result}")
    print("\n2) Facts", ', '.join(facts) + '.')
    print("\n3) Goal", goal + '.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Forward Chaining Algorithm with Trace Output")
    parser.add_argument('-f', '--file', type=str, required=True, help="Name of the text file containing the data")
    parser.add_argument('-p', '--path', type=str, default="", help="Optional path to the directory containing the file")

    args = parser.parse_args()

    if args.path:
        file_path = os.path.join(args.path, args.file)
    else:
        file_path = args.file

    rules, facts, goal = read_data(file_path)
    if rules is not None and facts is not None and goal is not None:
        print_data(rules, facts, goal)
        forward_chaining_with_trace(rules, facts, goal)

# python3 forward.py -f test1.txt