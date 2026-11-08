#!/usr/bin/env python3
"""Read a JSON work plan, or the single fenced JSON block in PLAN.md.

Requires Python 3.12 or later, standard library only. No writes or network.
Exit: 0 pass, 1 findings, 2 usage or unreadable input.
"""

import argparse
import json
import re
import sys
from pathlib import Path

REASONS = {
    "direct",
    "context-isolation",
    "independent-parallel-work",
    "independent-verification",
    "different-capability",
}


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate key {key!r}; keep one authoritative value")
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError(f"non-finite number {value}; use a finite integer")


def parse_plan(text):
    if not text.lstrip().startswith("{"):
        blocks = re.findall(r"^```json[ \t]*\n(.*?)^```[ \t]*$", text, re.M | re.S)
        if len(blocks) != 1:
            raise ValueError("provide JSON or exactly one fenced json block in PLAN.md")
        text = blocks[0]
    return json.loads(text, object_pairs_hook=unique_object, parse_constant=reject_constant)


def placeholders(value, path):
    """Yield every unresolved placeholder, including nested extension fields."""
    if isinstance(value, dict):
        for key, item in value.items():
            label = f"{path}.{key}" if path else key
            if "{{" in key:
                yield label, key
            yield from placeholders(item, label)
    elif isinstance(value, list):
        for index, item in enumerate(value):
            task = path == "tasks" and isinstance(item, dict) and populated(item.get("id"))
            yield from placeholders(item, item["id"] if task else f"{path}[{index}]")
    elif isinstance(value, str) and "{{" in value:
        yield path, value


def populated(value):
    return isinstance(value, str) and bool(value.strip()) and "{{" not in value


def natural(value):
    return type(value) is int and value >= 0


def check_plan(plan):
    errors = []
    if not isinstance(plan, dict):
        return ["plan must be an object; use the documented work-plan format"]
    for path, text in placeholders(plan, ""):
        errors.append(f"{path}: replace the placeholder {text!r}")
    for field in ("run_id", "integration_owner", "workspace"):
        if not populated(plan.get(field)):
            errors.append(f"{field}: supply one non-empty value")
    workspace = plan.get("workspace")
    if populated(workspace) and not Path(workspace).is_absolute():
        errors.append("workspace: use an absolute path in the checking environment")
    root = Path(workspace).resolve() if populated(workspace) else Path.cwd()
    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        errors.append("tasks: declare a non-empty list, including direct work")
        tasks = []
    by_id = {}
    writes = {}
    delegated = 0
    graph_valid = True
    for index, task in enumerate(tasks):
        label = f"tasks[{index}]"
        if not isinstance(task, dict):
            errors.append(f"{label}: supply a task object")
            graph_valid = False
            continue
        task_id = task.get("id")
        if not populated(task_id):
            errors.append(f"{label}.id: give the task a unique ID")
            graph_valid = False
            task_id = label
        elif task_id in by_id:
            errors.append(f"{task_id}: duplicate task ID; rename it and its references")
            graph_valid = False
        by_id[task_id] = task
        if not populated(task.get("owner")):
            errors.append(f"{task_id}.owner: assign one owner")
        if not populated(task.get("proof")):
            errors.append(f"{task_id}.proof: name the surface to drive and the result to observe")
        reason = task.get("execution")
        if not isinstance(reason, str) or reason not in REASONS:
            errors.append(f"{task_id}.execution: use direct or one documented delegation reason")
        elif reason != "direct":
            delegated += 1
            if not populated(task.get("reason")):
                errors.append(f"{task_id}.reason: explain the value of this delegation")
        dependencies = task.get("depends_on")
        if not isinstance(dependencies, list) or any(not populated(d) for d in dependencies):
            errors.append(f"{task_id}.depends_on: declare task IDs, or [] for no dependencies")
            graph_valid = False
        elif len(set(dependencies)) != len(dependencies):
            errors.append(f"{task_id}.depends_on: remove duplicate dependencies")
            graph_valid = False
        paths = task.get("write_paths")
        writes[task_id] = []
        if not isinstance(paths, list):
            errors.append(f"{task_id}.write_paths: declare literal paths, or [] for no writes")
            continue
        for path in paths:
            if not populated(path) or any(c in path for c in "*?[]\\\n\r"):
                errors.append(f"{task_id}.write_paths: replace {path!r} with a literal POSIX path")
                continue
            if ".." in Path(path).parts:
                errors.append(f"{task_id}.write_paths: replace {path!r} with a path without '..'")
                continue
            try:
                writes[task_id].append((root / path).resolve())
            except (OSError, RuntimeError, ValueError) as error:
                errors.append(f"{task_id}.write_paths: resolve {path!r} before dispatch: {error}")
    for task_id, task in by_id.items():
        dependencies = task.get("depends_on")
        if isinstance(dependencies, list):
            for dependency in dependencies:
                if populated(dependency) and dependency not in by_id:
                    errors.append(f"{task_id}.depends_on: unknown {dependency}; declare the task")
                    graph_valid = False

    # A path conflict is safe only when a dependency orders the two tasks.
    # The same owner name and separate checkouts do not establish ordering.
    if graph_valid:
        ancestors = {}
        visiting = set()

        def visit(task_id):
            if task_id in visiting:
                raise ValueError(f"dependency cycle at {task_id}; break the cycle")
            if task_id not in ancestors:
                visiting.add(task_id)
                found = set()
                for dependency in by_id[task_id]["depends_on"]:
                    found.add(dependency)
                    found.update(visit(dependency))
                visiting.remove(task_id)
                ancestors[task_id] = found
            return ancestors[task_id]

        try:
            for task_id in by_id:
                visit(task_id)
            ids = list(by_id)
            for index, left in enumerate(ids):
                for right in ids[index + 1:]:
                    if left in ancestors[right] or right in ancestors[left]:
                        continue
                    for a in writes[left]:
                        for b in writes[right]:
                            if a == b or a in b.parents or b in a.parents:
                                errors.append(
                                    f"parallel writers {left} and {right} overlap: {a} / {b}; "
                                    "split ownership or add a real dependency"
                                )
        except (ValueError, RecursionError) as error:
            errors.append(f"tasks: {error}; simplify the dependency graph")

    budget = plan.get("budget")
    if not isinstance(budget, dict):
        errors.append("budget: declare worker_starts, retries, review_rounds, concurrency, and reserve")
        return errors
    if not populated(budget.get("coordinator")):
        errors.append("budget.coordinator: name the single accountant for all runs")
    counters = {}
    for name in ("worker_starts", "retries", "review_rounds"):
        counter = budget.get(name)
        if not isinstance(counter, dict):
            errors.append(f"budget.{name}: declare finite integer limit and used fields")
            continue
        if any(not natural(counter.get(key)) for key in ("limit", "used")):
            errors.append(f"budget.{name}: use non-negative integer limit and used fields")
            continue
        counters[name] = counter
        if counter["used"] > counter["limit"]:
            errors.append(f"budget.{name}: used exceeds limit; stop and record unresolved work")
    concurrency = budget.get("concurrency")
    if not isinstance(concurrency, dict):
        errors.append("budget.concurrency: declare ceiling (1..8) and active count")
    elif type(concurrency.get("ceiling")) is not int or not 1 <= concurrency["ceiling"] <= 8:
        errors.append("budget.concurrency.ceiling: set 1..8, reduced to the user and host limits")
    elif not natural(concurrency.get("active")):
        errors.append("budget.concurrency.active: count active and uncertain runs with an integer")
    else:
        active = concurrency["active"]
        if active > concurrency["ceiling"]:
            errors.append("budget.concurrency: active exceeds ceiling; queue work before dispatch")
        if "worker_starts" in counters and active > counters["worker_starts"]["used"]:
            errors.append("budget.worker_starts: charge every active run, including descendants and evals")
    reserve = budget.get("reserve")
    if not isinstance(reserve, dict) or not natural(reserve.get("worker_starts")) or not populated(reserve.get("plan")):
        errors.append("budget.reserve: declare worker_starts and an integration/verification plan")
    elif "worker_starts" in counters:
        starts = counters["worker_starts"]
        if starts["used"] + reserve["worker_starts"] > starts["limit"]:
            errors.append("budget.reserve: starts consumed the reserve; stop discretionary launches")
        if delegated + reserve["worker_starts"] > starts["limit"]:
            errors.append("budget.worker_starts: task allocations exceed limit after reserve; reduce fan-out")
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        print("error: install Python 3.12 or later and rerun check-plan.py", file=sys.stderr)
        return 2
    try:
        source = args.plan.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        print(f"error: read an existing UTF-8 plan file: {error}", file=sys.stderr)
        return 2
    try:
        errors = check_plan(parse_plan(source))
    except (ValueError, OSError, RuntimeError) as error:
        errors = [f"plan: {error}; fix the input and rerun"]
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: owners, proofs, delegation reasons, dependency ordering, write paths, and recorded budget")
    return 0


if __name__ == "__main__":
    sys.exit(main())
