#!/usr/bin/env python3
"""Run scoped read-only catalog checks through psql and libpq's environment.

Usage: audit-schema.py --schema NAME [--tenant-column NAME]
Requires Python 3.12+ stdlib and a PostgreSQL psql client compatible with the server.
Use authorized read-only access; credentials belong in protected libpq configuration.
No connection string or password arguments. The SQL reads metadata only, with
bounded lock/statement timeouts. Catalog rows are review leads, not domain verdicts.
Output: one JSON document on stdout; value-free diagnostics on stderr.
Exit: 0 no leads, 1 leads or empty scope, 2 usage/setup/query failure.
--help has no host inspection, connection or write effects.
"""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, "error: use --schema NAME and optional --tenant-column NAME; see --help\n")


def main():
    parser = Parser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--schema", required=True)
    parser.add_argument("--tenant-column", default="tenant_id")
    args = parser.parse_args()
    if not args.schema.strip() or not args.tenant_column.strip():
        print("error: supply nonempty schema and tenant-column names", file=sys.stderr)
        return 2
    if shutil.which("psql") is None:
        print("error: install the PostgreSQL client compatible with the target server", file=sys.stderr)
        return 2
    sql = Path(__file__).resolve().parent.parent / "references/catalog-audit.sql"
    env = dict(os.environ)
    env.setdefault("PGCONNECT_TIMEOUT", "10")
    try:
        result = subprocess.run(["psql", "-X", "-w", "-q", "-A", "-t", "-v", "ON_ERROR_STOP=1",
                                 "-v", "schema=" + args.schema, "-v", "tenant_column=" + args.tenant_column,
                                 "-f", str(sql)], env=env, capture_output=True, text=True, timeout=30)
        if result.returncode:
            raise ValueError("query failed")
        data = json.loads(result.stdout)
        if (not isinstance(data, dict) or type(data.get("objects_scanned")) is not int
                or data["objects_scanned"] < 0 or not isinstance(data.get("findings"), list)):
            raise ValueError("bad result shape")
    except (OSError, UnicodeError, ValueError, subprocess.TimeoutExpired):
        print("error: catalog query could not complete; verify target access and supported catalogs; native output withheld", file=sys.stderr)
        return 2
    if data["objects_scanned"] == 0:
        data["findings"].append({"check": "empty-scope", "reason": "verify the explicit schema and table inventory"})
    print(json.dumps(data))
    if data["findings"]:
        print("error: review each catalog lead against the invariant crosswalk and record any intended exception", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
