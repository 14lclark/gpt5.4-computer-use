from logging import getLogger
import time
import subprocess
import base64

from openai import OpenAI

from .settings import filesystem_settings

log = getLogger("computer-use-logger")


def run_cmd(cmd: str | list[str]):
    """
    Run the commands for the agent to do stuff.
    This should ideally have input sanitization to prevent MITM attacks.
    """
    if isinstance(cmd, list):
        result = subprocess.run(cmd, capture_output=True)
    elif isinstance(cmd, str):
        result = subprocess.run(cmd.split(" "), capture_output=True)
    else:
        raise TypeError("run_cmd only accepts str or list[str] arguments")
    return result


class ComputerUseActions:
    button_map = {"left": 1, "middle": 2, "right": 3}

    def __init__(self):
        self.action_map = {
            "click": self.click,
            "double_click": self.double_click,
            "scroll": self.scroll,
            "keypress": self.keypress,
            "type": self.type,
            "wait": self.wait,
            "screenshot": self.screenshot,
        }

    def move(self, action):
        run_cmd(f"xdotool mousemove {action.x} {action.y}")

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

    def drag(self, action):
        paths = zip(action.path[0:-1], action.path[1:])
        cmd = ""
        for p1, p2 in paths:
            cmd += f"xdotool mousemove {p1.x} {p2.y} && "
            cmd += "xdotool mousedown 1 && "
            cmd += f"xdotool mousemove {p2.x} {p2.y} && "
            cmd += "xdotool mouseup 1 && "
        cmd += "true"
        run_cmd(cmd)

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
        # I'm implicitly assuming here that every sequence of keys is actually a
        # shortcut that needs to be pressed simultaneously.
        keys = [key if key != "SPACE" else "space" for key in action.keys]
        run_cmd("xdotool key " + "+".join(keys))

    def type(self, action):
        cmd = ["xdotool", "type", "--delay", "0", f"{action.text}"]
        print("TEXT: ", cmd)
        result = run_cmd(cmd)

    def wait(self, action):
        time.sleep(2)

    def screenshot(self, action=None):
        run_cmd("screengrab -n")
        ss_path = filesystem_settings.screenshot_output_dir / "screen.png"
        with open(ss_path, "rb") as screenshot:
            b64_image = base64.b64encode(screenshot.read()).decode("utf-8")
        run_cmd(f"rm {ss_path}")
        return b64_image

    def __call__(self, action):
        try:
            getattr(self, action.type)(action)
        except ValueError as e:
            print(f"Unsupported action: {action.type}")
        # Sleep after every call to give the OS time to breathe!
        # It couldn't keep up.
        time.sleep(0.5)


class ComputerUseAgent:
    def __init__(self, api_client: OpenAI, prompt: str):
        self.counter = 0
        self.computer_actions = ComputerUseActions()
        self.client = api_client
        self.response = self.client.responses.create(
            model="gpt-5.4", tools=[{"type": "computer"}], input=prompt
        )
        self.original_prompt = prompt
        print("Initial Call:\n")
        print(self.response)
        print()
        self.agent_loop()

    def agent_loop(self):
        while True:
            print("Call:\n")
            screenshot_b64 = self.computer_actions.screenshot()
            self.response = self.client.responses.create(
                model="gpt-5.4",
                tools=[{"type": "computer"}],
                previous_response_id=self.response.id,
                input=[
                    {
                        "type": "computer_call_output",
                        "call_id": self.response.output[0].call_id,
                        "output": {
                            "type": "computer_screenshot",
                            "image_url": f"data:image/png;base64,{screenshot_b64}",
                            "detail": "original",
                        },
                    }
                ],
            )
            print(self.response)
            print()
            next_call = self.response.output[0].type

            if next_call != "computer_call":
                break

            action_list = self.response.output[0].actions
            for action in action_list:
                self.computer_actions(action)
