def label(payload):
    return "Active" if payload["active"] else "Paused"
