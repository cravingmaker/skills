def run(cur):
    cur.execute("SET TIME ZONE 'UTC'")
    cur.execute("LOAD 'auto_explain'")
