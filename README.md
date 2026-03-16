# gpt5.4-computer-use

Two environment variables that need to be set:
 - CLICKS_OPENAI_API_KEY
  - self explanatory
 - CLICKS_SCREENSHOT_OUTPUT_DIR
  - This is the directory that the screenshot will be placed after every call. In this code, the screenshots are created with [`screengrab`](https://github.com/lxqt/screengrab). `screengrab` uses the home directory of the user taking the screenshot as the default location, so set this variable to your home directory.
