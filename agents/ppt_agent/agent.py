from .tools import create_ppt

def run(args):
    return create_ppt(args["title"], args["slides"])