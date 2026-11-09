await fetch(url, {
  // signal: an unrelated comment must not quiet the candidate
  method: "POST",
});
await Promise.all(inputs.map(send));
const pool = new pg.Pool({});
