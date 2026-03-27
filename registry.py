from agents.ppt_agent.agent import run as ppt_run
from agents.web_agent.agent import run as web_run
from agents.data_agent.agent import run as data_run
from agents.matlab_agent.agent import run as matlab_run

TOOLS = {
    "generate_ppt": ppt_run,
    "launch_web": web_run,
    "analyze_data": data_run,
    "run_matlab": matlab_run,
}