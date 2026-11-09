#!/usr/bin/env python3
"""Check resolved workspace crate edges against an explicit layer policy.

Usage: check-cargo-boundaries.py METADATA.json POLICY.json
Generate metadata using: cargo metadata --format-version 1 --locked
Python 3.12+ standard library; reads files only, never runs Cargo or writes.
Stdout: JSON edge counts and findings with package, layer, kind and target.
Stderr: diagnostics. Exits: 0 pass, 1 forbidden/unclassified/empty scan,
2 usage or malformed/incomplete input. Does not infer feature/target coverage.
The policy must classify every workspace crate and explicitly allow destinations
for every layer and each of normal, build, and dev dependencies.
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

KINDS = {"normal", "build", "dev"}


def require(condition, fix):
    if not condition:
        raise ValueError(fix)


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "remove duplicate JSON object keys")
        result[key] = value
    return result


def string_list(value):
    return isinstance(value, list) and all(isinstance(item, str) and item for item in value) and len(value) == len(set(value))


def check(metadata, policy):
    require(isinstance(policy, dict) and set(policy) == {"layers", "allow"},
            "policy needs only layers and allow objects; use the shipped policy example")
    layers, allowed = policy["layers"], policy["allow"]
    require(isinstance(layers, dict) and layers and all(isinstance(key, str) and key for key in layers),
            "give each policy layer a non-empty name")
    require(all(string_list(names) and names for names in layers.values()),
            "assign non-empty, unique package-name lists to layers")
    classified = {}
    for layer, names in layers.items():
        for name in names:
            require(name not in classified, "assign each package to exactly one layer")
            classified[name] = layer
    require(isinstance(allowed, dict) and set(allowed) == KINDS,
            "declare normal, build, and dev policies separately")
    for rules in allowed.values():
        require(isinstance(rules, dict) and set(rules) == set(layers),
                "declare allowed destination layers for every source layer and dependency kind")
        require(all(string_list(destinations) and set(destinations) <= set(layers) for destinations in rules.values()),
                "allow only unique known destination layer names")
    require(isinstance(metadata, dict) and type(metadata.get("version")) is int and metadata["version"] == 1,
            "generate cargo metadata --format-version 1, with resolved dependencies")
    packages, members, resolve = metadata.get("packages"), metadata.get("workspace_members"), metadata.get("resolve")
    require(isinstance(packages, list) and packages and string_list(members) and members,
            "supply non-empty packages and workspace_members from Cargo")
    ids = {}
    for package in packages:
        require(isinstance(package, dict) and isinstance(package.get("id"), str) and package["id"]
                and isinstance(package.get("name"), str) and package["name"], "keep each Cargo package id and name")
        require(package["id"] not in ids, "keep Cargo package ids unique")
        ids[package["id"]] = package["name"]
    require(set(members) <= set(ids), "include package records for every workspace member")
    require(len({ids[member] for member in members}) == len(members),
            "use unambiguous workspace package names for this layer policy")
    require(isinstance(resolve, dict) and isinstance(resolve.get("nodes"), list) and resolve["nodes"],
            "include resolve.nodes; rerun Cargo without --no-deps")
    nodes = {}
    for node in resolve["nodes"]:
        require(isinstance(node, dict) and isinstance(node.get("id"), str) and node["id"] in ids
                and isinstance(node.get("deps"), list), "keep node ids and resolved deps arrays from Cargo")
        require(node["id"] not in nodes, "keep resolved node ids unique")
        nodes[node["id"]] = node
    require(set(members) <= set(nodes), "include a resolved node for every workspace member")
    names = {ids[member] for member in members}
    findings = [f"{name}: classify this workspace package in exactly one layer"
                for name in sorted(names - set(classified))]
    findings += [f"{name}: policy package absent from this workspace; fix the name or input scope"
                 for name in sorted(set(classified) - names)]
    counts, scanned, external = Counter({kind: 0 for kind in KINDS}), 0, 0
    for source in members:
        for dependency in nodes[source]["deps"]:
            require(isinstance(dependency, dict) and isinstance(dependency.get("pkg"), str)
                    and dependency["pkg"] in ids, "include resolved package ids, including external dependencies")
            kinds = dependency.get("dep_kinds")
            require(isinstance(kinds, list) and kinds, "include non-empty dep_kinds; use the resolved Cargo format")
            for edge in kinds:
                require(isinstance(edge, dict) and "kind" in edge and "target" in edge,
                        "keep kind and target on each resolved dependency")
                kind = "normal" if edge["kind"] is None else edge["kind"]
                require(isinstance(kind, str) and kind in KINDS, "support the new Cargo dependency kind before scanning it")
                require(edge["target"] is None or isinstance(edge["target"], str), "keep target as a string or null")
                destination = dependency["pkg"]
                if destination not in members:
                    external += 1
                    continue
                scanned += 1
                counts[kind] += 1
                source_name, destination_name = ids[source], ids[destination]
                left, right = classified.get(source_name), classified.get(destination_name)
                if left and right and right not in allowed[kind][left]:
                    findings.append(f"{source_name} ({left}) -> {destination_name} ({right}): forbidden {kind} edge"
                                    + (f" for {edge['target']}" if edge["target"] else "")
                                    + "; remove the dependency or approve an explicit policy change")
    if not scanned:
        findings.append("empty workspace-edge scan; supply a resolved graph with a real inter-crate edge")
    return {"workspace_packages": len(members), "workspace_edges": scanned, "edges_by_kind": dict(sorted(counts.items())),
            "external_edges_out_of_scope": external, "findings": sorted(set(findings))}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("metadata", type=Path)
    parser.add_argument("policy", type=Path)
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        parser.error("use Python 3.12 or later")
    try:
        values = [json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
                  for path in (args.metadata, args.policy)]
        result = check(*values)
    except (OSError, UnicodeError, ValueError) as error:
        print(f"error: {error}; correct the inputs and rerun", file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=True))
    return 1 if result["findings"] else 0


if __name__ == "__main__":
    sys.exit(main())
