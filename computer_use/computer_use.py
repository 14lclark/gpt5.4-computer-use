from logging import getLogger
import time
import os
import sys
import subprocess
from openai import OpenAI

log = getLogger("computer-use-logger")


def run_cmd(cmd: str):
    """
    Run the commands for the agent to do stuff.
    This should ideally have input sanitization to prevent MITM attacks.
    """
    log.info("Running command:")
    log.info(cmd)
    result = subprocess.run(cmd.split(" "), capture_output=True)
    log.info("stdout:")
    log.info(result)
    log.info("stderror:")
    log.info(result.stderr)


class ComputerUseActions:
    button_map = {"left": 1, "middle": 2, "right": 3}

    def __init__(self):
        pass

    def click(self, action):
        button = self.button_map.get(getattr(action, "button", "left"), 1)
        log.info(f"Received action to click at {action.x} {action.y}.")
        run_cmd(
            f"xdotool mousemove {action.x} {action.y} click {button}",
        )

    def double_click(self, action):
        button = self.button_map.get(getattr(action, "button", "left"), 1)
        log.info(f"Received action to double click at {action.x} {action.y}.")
        run_cmd(
            f"xdotool mousemove {action.x} {action.y} click --repeat 2 {button}",
        )

    def scroll(self, action):
        button = 4 if getattr(action, "scrollY", 0) < 0 else 5
        clicks = max(1, abs(round(getattr(action, "scrollY", 0) / 100)))
        run_cmd(
            f"xdotool mousemove {action.x} {action.y}",
        )
        for _ in range(clicks):
            run_cmd(
                f"xdotool click {button}",
            )

    def keypress(self, action):
        for key in action.keys:
            normalized = "space" if key == "SPACE" else key
            run_cmd(
                f"xdotool key '{normalized}'",
            )

    def type(self, action):
        run_cmd(
            f"xdotool type --delay 0 '{action.text}'",
        )

    def wait(self, action):
        time.sleep(2)

    def screenshot(self, action):
        pass

    # case _:
    # raise ValueError(f"Unsupported action: {action.type}")


class ComputerUseAgent:
    def __init__(self, api_client: OpenAI, prompt):
        self.actions = ComputerUseActions()
        self.client = api_client
        self.initial_response = self.client.responses.create(
            model="gpt-5.4", tools=[{"type": "computer"}], input=prompt
        )
        self.actions_list = self.initial_response.actions

    def agent_loop(self):
        response = self.client.responses.create()

        print(response)
        # for action in action_list:
