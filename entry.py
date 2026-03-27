import json
import re
import sys

from executor import execute


PPT_KEYWORDS = ("ppt", "powerpoint", "幻灯片", "演示文稿", "演示稿", "汇报", "报告")
MATLAB_KEYWORDS = ("matlab", "计算", "求值", "开方", "平方根", "数值", "矩阵", "函数")


def detect_task_type(text):
    lowered = text.lower()
    if any(keyword in lowered for keyword in PPT_KEYWORDS):
        return "generate_ppt"
    if any(keyword in lowered for keyword in MATLAB_KEYWORDS):
        return "run_matlab"
    raise ValueError("unsupported task type")


def extract_slide_count(text):
    match = re.search(r"(\d+)\s*[页张Pp][Tt]?", text)
    if match:
        return max(1, int(match.group(1)))

    match = re.search(r"(\d+)\s*[页张]", text)
    if match:
        return max(1, int(match.group(1)))

    return 3


def extract_ppt_title(text):
    explicit = re.search(r"(?:标题|主题)[:：]\s*([^\n]+)", text)
    if explicit:
        return explicit.group(1).strip()

    cleaned = re.sub(r"(帮我|做一个|做个|生成|制作|关于|一份|一个)", " ", text)
    cleaned = re.sub(r"(ppt|PPT|powerpoint|幻灯片|演示文稿|演示稿)", " ", cleaned)
    cleaned = re.sub(r"(包含|共)\s*\d+\s*[页张]", " ", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned).strip(" ：:，,。.!！?")
    return cleaned[:40] if cleaned else "自动生成PPT"


def build_ppt_slides(text, count):
    topic = extract_ppt_title(text)
    defaults = [
        ("背景与定义", f"{topic}的核心概念、发展背景与主要应用场景。"),
        ("关键趋势", f"{topic}当前的关键趋势、代表性技术与行业变化。"),
        ("总结与展望", f"{topic}的落地价值、挑战以及后续发展方向。"),
    ]

    slides = []
    for index in range(count):
        if index < len(defaults):
            title, content = defaults[index]
        else:
            title = f"扩展内容 {index + 1}"
            content = f"{topic}相关补充内容，第{index + 1}页。"
        slides.append({"title": title, "content": content})
    return slides


def extract_numeric_value(text):
    match = re.search(r"-?\d+(?:\.\d+)?", text)
    if not match:
        return 4
    value = float(match.group(0))
    return int(value) if value.is_integer() else value


def build_task(text):
    task_type = detect_task_type(text)

    if task_type == "generate_ppt":
        title = extract_ppt_title(text)
        slide_count = extract_slide_count(text)
        return {
            "tool": "generate_ppt",
            "args": {
                "title": title,
                "slides": build_ppt_slides(text, slide_count),
            },
        }

    return {
        "tool": "run_matlab",
        "args": {
            "value": extract_numeric_value(text),
        },
    }


def main():
    user_input = " ".join(sys.argv[1:]).strip()
    if not user_input:
        user_input = input("请输入自然语言任务: ").strip()

    task = build_task(user_input)
    result = execute(task)
    print(json.dumps({"task": task, "result": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
