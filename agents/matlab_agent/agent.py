import subprocess

def run(args):
    value = args.get("value", 4)

    script = f"""
    result = sqrt({value});
    disp(jsonencode(result));
    exit;
    """

    result = subprocess.run(
        ["matlab", "-batch", script],
        capture_output=True,
        text=True
    )

    output = result.stdout.strip()
    error = result.stderr.strip()

    if result.returncode != 0:
        return error or output or f"MATLAB exited with code {result.returncode}"

    return output or error or "MATLAB completed with no output"
