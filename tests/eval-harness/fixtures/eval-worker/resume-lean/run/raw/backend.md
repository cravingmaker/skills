COMPLETE: backend converted to status-v2.
Output: backend/service.py SHA256 1eafe4420e49f3fd553f8374ac4c6bdcdc0a5334b0c6b01959cca21ee00465d2.
Command: python3 -B -c 'from backend.service import label; assert label({"status":"active"})=="Active"' exited 0.
Input: contracts/status.json revision status-v2.
