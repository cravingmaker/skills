#!/usr/bin/env python3
"""Check logical-model references, not the truth of the modeled semantics.

Python 3.12+ standard library. Read-only; no database or network access.
Usage: check-model.py MODEL.json
Output: JSON summary on stdout; field-path diagnostics on stderr.
Exit: 0 references pass (unresolved questions counted), 1 findings, 2 usage/input.
"""

import argparse
import json
import sys
from pathlib import Path


def check(model):
    errors, seen = [], set()

    def require(condition, path, fix):
        if not condition:
            errors.append(f"{path}: {fix}")

    def entries(parent, key, path):
        value = parent.get(key)
        if not isinstance(value, list) or any(not isinstance(x, dict) for x in value):
            errors.append(f"{path}.{key}: supply an array of objects")
            return []
        return value

    def strings(value):
        return (isinstance(value, list) and bool(value)
                and all(isinstance(x, str) and x.strip() for x in value)
                and len(value) == len(set(value)))

    def identity(item, path):
        value = item.get("id")
        valid = isinstance(value, str) and bool(value.strip())
        require(valid, path, "supply a stable nonempty id")
        if valid:
            require(value not in seen, path, "make ids unique across the model")
            seen.add(value)
        return value if valid else None

    if not isinstance(model, dict):
        return ["model: supply a JSON object"]
    questions = set()
    for i, question in enumerate(entries(model, "questions", "model")):
        path = f"questions[{i}]"
        qid = identity(question, path)
        if qid:
            questions.add(qid)
        for field in ("question", "consumer", "input_grain", "output_grain"):
            require(isinstance(question.get(field), str) and bool(question[field].strip()),
                    path + "." + field, "name the consumer question and its input/output grain")
    require(bool(questions), "questions", "supply at least one consumer question")
    entities, keys = {}, {}
    for i, entity in enumerate(entries(model, "entities", "model")):
        path = f"entities[{i}]"
        eid = identity(entity, path)
        serves = entity.get("serves")
        require(strings(serves) and all(x in questions for x in serves), path + ".serves",
                "reference the consumer questions this entity answers")
        fields = entity.get("fields")
        require(strings(fields), path + ".fields", "supply distinct field names")
        fields = fields if strings(fields) else []
        grain = entity.get("grain")
        require(strings(grain) and all(x in fields for x in grain), path + ".grain",
                "name the fields defining one row")
        require(isinstance(entity.get("lifecycle"), str) and bool(entity["lifecycle"].strip()),
                path + ".lifecycle", "state creation, correction and retirement semantics")
        entity_keys = entries(entity, "keys", path)
        require(bool(entity_keys), path + ".keys", "supply an identity key")
        for j, key in enumerate(entity_keys):
            kpath = f"{path}.keys[{j}]"
            kid = identity(key, kpath)
            kfields = key.get("fields")
            valid = strings(kfields) and all(x in fields for x in kfields)
            require(valid, kpath, "reference distinct fields of this entity")
            if kid:
                keys[kid] = (eid, kfields if valid else [])
        if eid:
            entities[eid] = fields
    require(bool(entities), "entities", "supply at least one entity")
    for i, relation in enumerate(entries(model, "relationships", "model")):
        path = f"relationships[{i}]"
        identity(relation, path)
        origin, target = relation.get("from"), relation.get("to_key")
        valid_origin = isinstance(origin, str) and origin in entities
        valid_target = isinstance(target, str) and target in keys
        require(valid_origin, path + ".from", "reference an existing entity id")
        require(valid_target, path + ".to_key", "reference an existing key id")
        fields = relation.get("fields")
        valid_fields = strings(fields) and valid_origin and all(x in entities[origin] for x in fields)
        require(valid_fields, path + ".fields", "reference the originating entity fields")
        if valid_fields and valid_target:
            require(len(fields) == len(keys[target][1]), path, "match the target key width")
        require(relation.get("cardinality") in ("one-to-one", "one-to-many", "many-to-one", "many-to-many"),
                path + ".cardinality", "state the relationship cardinality")
        require(type(relation.get("optional")) is bool, path + ".optional", "state whether the link is optional")
    mapped = set()
    for i, mapping in enumerate(entries(model, "mappings", "model")):
        path = f"mappings[{i}]"
        identity(mapping, path)
        entity = mapping.get("entity")
        valid_entity = isinstance(entity, str) and entity in entities
        require(valid_entity, path + ".entity", "reference an existing entity id")
        if valid_entity:
            mapped.add(entity)
        status = mapping.get("status")
        require(status in ("mapped", "unbuilt", "unresolved"), path + ".status", "use mapped, unbuilt or unresolved")
        for field in ("source", "identity_rule", "grain"):
            require(isinstance(mapping.get(field), str) and bool(mapping[field].strip()),
                    path + "." + field, "supply the source, identity rule and destination grain")
        if status == "mapped":
            require(isinstance(mapping.get("target"), str) and bool(mapping["target"].strip()),
                    path + ".target", "name the physical destination")
            field_map = mapping.get("fields")
            require(isinstance(field_map, dict) and bool(field_map) and valid_entity
                    and all(isinstance(k, str) and k.strip() and v in entities[entity]
                            for k, v in field_map.items() if isinstance(v, str))
                    and all(isinstance(v, str) for v in field_map.values()),
                    path + ".fields", "map source fields to existing logical fields")
        else:
            require(isinstance(mapping.get("reason"), str) and bool(mapping["reason"].strip()),
                    path + ".reason", "explain the missing or unresolved mapping")
    require(mapped == set(entities), "mappings", "map every entity or mark it unbuilt/unresolved")
    for i, item in enumerate(entries(model, "unresolved", "model")):
        path = f"unresolved[{i}]"
        identity(item, path)
        for field in ("question", "owner"):
            require(isinstance(item.get(field), str) and bool(item[field].strip()),
                    path + "." + field, "name the open question and accountable owner")
    return errors


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON member")
        result[key] = value
    return result


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "error: supply the documented local file arguments; see --help\n")


def main():
    parser = Parser(description=__doc__)
    parser.add_argument("model", type=Path)
    args = parser.parse_args()
    try:
        model = json.loads(args.model.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    except (OSError, UnicodeError, ValueError):
        print("error: supply a readable UTF-8 JSON model; input contents withheld", file=sys.stderr)
        return 2
    errors = check(model)
    for error in errors:
        print(error, file=sys.stderr)
    print(json.dumps({"ok": not errors, "findings": len(errors),
                      "unresolved": len(model.get("unresolved", [])) if isinstance(model, dict) and isinstance(model.get("unresolved"), list) else 0}))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
