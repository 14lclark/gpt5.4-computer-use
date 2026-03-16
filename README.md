# gpt5.4-computer-use

Two environment variables that need to be set:
 - CLICKS_OPENAI_API_KEY
  - self explanatory
 - CLICKS_SCREENSHOT_OUTPUT_DIR
  - This is the directory that the screenshot will be placed after every call. In this code, the screenshots are created with [`screengrab`](https://github.com/lxqt/screengrab). `screengrab` uses the home directory of the user taking the screenshot as the default location, so set this variable to your home directory.
These environment variables can be set in a `.env` file. 
```dotenv
CLICKS_OPENAI_API_KEY=...
CLICKS_SCREENSHOT_OUTPUT_DIR=...
```

To run locally:

Make sure you have `xdotool` and `screengrab` installed and install the Python requirements globally or in a virtual environment. Then run `python3 main.py --prompt "Your instructions go here."`

To build and run in webtop:

Inside the project directory, run 
```
docker build . -f Dockerfile.webtop -t computer-use-test:latest
docker run -p 3000:3000 --volume .:/config/agent computer-use-test:latest 
```
In a browser, navigate to `localhost:3000`. Inside the host, open a terminal and setup your Python environment -- that is, install the `requirements.txt` file either globally or in a virtual environment. Then, run the script as in the local case: `python main.py --prompt "Your instructions go here."`

If you experience issues while attempting to run inside the webtop container, you may need to run instead as `DISPLAY=":1" python main.py --prompt "Your instructions go here."`.