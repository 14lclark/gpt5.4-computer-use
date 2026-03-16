from dotenv import load_dotenv

load_dotenv()

from logging import getLogger
from argparse import ArgumentParser

from openai import OpenAI

from computer_use.computer_use import ComputerUseAgent
from computer_use.settings import llm_settings

log = getLogger("computer-use-logger")

client = OpenAI(api_key=llm_settings.openai_api_key)


parser = ArgumentParser(
    prog="Clicks Computer Use Agent -- GPT 5.4",
    description="Run the agent with an instruction from the command line.",
)

parser.add_argument(
    "-p",
    "--prompt",
    type=str,
    help="string containing the prompt; should contain the task for the agent to accomplish.",
)
parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    help="print verbose messages; warnings and errors.",
)

if __name__ == "__main__":
    import sys

    args = parser.parse_args()
    log.debug(args)
    log.debug("API Key: " + llm_settings.openai_api_key)

    agent = ComputerUseAgent(client, args.prompt)
