import subprocess
import os
import tempfile

def run_selected_ranges(filename, ranges):
    # read all lines
    with open(filename, "r") as f:
        lines = f.readlines()

    selected = []

    for start, end in ranges:
        s = 0 if start is None else start
        e = len(lines) if end is None else end
        selected.extend(lines[s:e])

    # create temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as tmp:
        tmp.writelines(selected)
        temp_name = tmp.name

    try:
        # run temp file
        result = subprocess.run(
            ["python", temp_name],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        print(result.stderr)
    finally:
        os.remove(temp_name)  # delete temp file