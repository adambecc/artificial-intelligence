import argparse
import os

def read_data(file_path):
    rules = []
    facts = []
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
                        result, conditions = map(str.strip, line.split(',', 1))
                        rule = (conditions.split(), result)
                        rules.append(rule)

                elif section == "facts" and line:
                    facts.extend(line.split())

                elif section == "goal" and line:
                    goal = line.strip()

    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None, None

    return rules, facts, goal

def backward_chaining(rules, facts, goal, depth=0, path=None, step_counter=0, visited_goals=None, inferred_facts=None):
    global initial_facts, first_step

    if path is None:
        path = []
    if visited_goals is None:
        visited_goals = set()
    if inferred_facts is None:
        inferred_facts = set()

    prefix = f"{step_counter + 1:>3}) " + "-" * depth

    if goal in visited_goals:
        step_counter += 1
        print(f"{prefix}Goal {goal}. Cycle detected. Back, FAIL.")
        return False, path, step_counter, facts

    visited_goals.add(goal)

    if goal in facts:
        step_counter += 1
        if step_counter == 1:
            first_step = True
        else:
            first_step = False
        inferred_only = [fact for fact in facts if fact not in initial_facts]
        if goal in initial_facts:
            print(f"{prefix}Goal {goal}. Fact (initial), as facts are {', '.join(initial_facts)} and {', '.join(inferred_only)}. Back, OK.")
        elif goal in inferred_facts:
            print(f"{prefix}Goal {goal}. Fact (earlier inferred), as facts are {', '.join(initial_facts)} and {', '.join(inferred_only)}. Back, OK.")
        else:
            print(f"{prefix}Goal {goal}. Fact (presently inferred), as facts are {', '.join(initial_facts)} and {', '.join(inferred_only)}. Back, OK.")
        visited_goals.remove(goal)
        return True, path, step_counter, facts

    applicable_rules = [(index + 1, rule) for index, rule in enumerate(rules) if rule[1] == goal]

    if not applicable_rules:
        step_counter += 1
        print(f"{prefix}-Goal {goal}. No rules. Back, FAIL.")
        visited_goals.remove(goal)
        return False, path, step_counter, facts

    goal_inferred = False
    best_path = None
    for rule_index, (conditions, result) in applicable_rules:
        step_counter += 1
        print(f"{step_counter:>3}) {'-' * depth}Goal {goal} Find R{rule_index}: {', '.join(conditions)} -> {result}. New goals {', '.join(conditions)}.")

        temp_facts = facts.copy()
        temp_path = path.copy()

        all_conditions_met = True
        for condition in conditions:
            success, condition_path, step_counter, temp_facts = backward_chaining(
                rules, temp_facts, condition, depth + 1, temp_path, step_counter, visited_goals, inferred_facts
            )
            if not success:
                all_conditions_met = False
                break
            temp_path = condition_path

        if all_conditions_met:
            temp_path.append(f"R{rule_index}")
            if best_path is None or len(temp_path) < len(best_path):
                best_path = temp_path.copy()
            inferred_facts.add(goal)
            temp_facts.append(goal)
            inferred_only = [fact for fact in temp_facts if fact not in initial_facts]
            step_counter += 1
            print(f"{step_counter:>3}) {'-' * depth}Goal {goal}. Fact (presently inferred). Facts {', '.join(initial_facts)} and {', '.join(inferred_only)}. OK.")
            goal_inferred = True
            facts = temp_facts
            break

    if not goal_inferred:
        step_counter += 1
        print(f"{step_counter:>3}) {'-' * depth}-Goal {goal}. Back, FAIL.")

    visited_goals.remove(goal)
    return goal_inferred, best_path if best_path else path, step_counter, facts

def run_backward_chaining(rules, facts, goal):
    global first_step
    path = []
    print("\nPART 2. Trace\n")

    success, path, _, facts = backward_chaining(rules, facts, goal)

    print("\nPART 3. Results")
    if success:
        if first_step == False:
            print(f"1) Goal {goal} achieved.")
            print(f"2) Path: {', '.join(path)}.")
        else:
            print(f"Goal {goal} among facts. Empty path.")
    else:
        print(f"1) Goal {goal} not achieved.")
        print("2) Path: None.")

def print_data(rules, facts, goal):
    print("PART 1. Data\n")
    print("1) Rules")
    for i, rule in enumerate(rules, start=1):
        conditions, result = rule
        conditions_str = ', '.join(conditions)
        print(f"R{i:>3}: {conditions_str} -> {result}")
    print("\n2) Facts", ', '.join(facts) + '.')
    print("\n3) Goal", goal + '.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Backward Chaining Algorithm with Trace Output")
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
        global initial_facts
        initial_facts = facts.copy()
        run_backward_chaining(rules, facts, goal)
