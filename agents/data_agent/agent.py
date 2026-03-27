import pandas as pd

def run(args):
    df = pd.DataFrame(args.get("data", []))
    summary = df.describe().to_string()
    print(summary)
    return summary