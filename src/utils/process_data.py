import subprocess
import os

scripts = [
    '../src/data/clean.py',
    '../src/data/merge.py',
    '../src/data/feature.py'
]

for script in scripts:
    script_path = os.path.abspath(script)
    script_dir = os.path.dirname(script_path)
    script_name = os.path.basename(script_path)

    print(f"Running {script_name} in {script_dir}")

    result = subprocess.run(
        ['python3', script_name],
        cwd=script_dir,
        capture_output=True,
        text=True
    )

    print(result.stdout)
    if result.returncode != 0:
        print(f"Error in {script_name}:\n{result.stderr}")