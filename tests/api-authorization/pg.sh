# Sourced test support. Creates only a disposable container; never reads a database URL.
# Requires an explicit PG_IMAGE naming an already-local PostgreSQL image; never pulls.
pg_container=
pg_tmp=
pg_cleanup() {
  if [ -n "$pg_container" ]; then docker rm -f "$pg_container" >/dev/null 2>&1 || true; fi
  if [ -n "$pg_tmp" ]; then rm -rf "$pg_tmp"; fi
}
pg_start() {
  if [ -z "${PG_IMAGE:-}" ] || ! command -v docker >/dev/null 2>&1; then
    echo 'skip: PostgreSQL asset checks need Docker and PG_IMAGE set to an already-local PostgreSQL image; no database URL is accepted'
    return 1
  fi
  if ! docker image inspect "$PG_IMAGE" >/dev/null 2>&1; then
    echo 'error: PG_IMAGE is not local; provide a local PostgreSQL image before running these offline tests' >&2
    return 2
  fi
  pg_tmp=$(mktemp -d "${TMPDIR:-/tmp}/skill-pg.XXXXXX")
  trap pg_cleanup 0
  trap 'exit 130' INT
  trap 'exit 143' TERM
  pg_container=$(docker run -d --rm --pull never --network none -e POSTGRES_HOST_AUTH_METHOD=trust "$PG_IMAGE") || return 2
  tries=0
  until docker exec "$pg_container" psql -X -q -h 127.0.0.1 -U postgres -d postgres -c 'SELECT 1' >/dev/null 2>&1; do
    tries=$((tries + 1))
    if [ "$tries" -ge 30 ]; then
      echo 'error: disposable PostgreSQL did not become ready; check that PG_IMAGE runs a PostgreSQL server' >&2
      return 2
    fi
    sleep 1
  done
}
pg_sql() {
  docker exec -i "$pg_container" psql -X -q -o /dev/null -v ON_ERROR_STOP=1 -h 127.0.0.1 -U "${1:-postgres}" -d postgres
}
pg_query() {
  docker exec -i "$pg_container" psql -X -q -At -v ON_ERROR_STOP=1 -h 127.0.0.1 -U "${1:-postgres}" -d postgres
}
