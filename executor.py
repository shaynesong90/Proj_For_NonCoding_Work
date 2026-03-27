from registry import TOOLS

def execute(task_json):
    tool_name = task_json.get("tool")
    args = task_json.get("args", {})

    if tool_name not in TOOLS:
        raise Exception(f"Tool {tool_name} not found")

    print(f"[Executor] Running: {tool_name}")
    return TOOLS[tool_name](args)