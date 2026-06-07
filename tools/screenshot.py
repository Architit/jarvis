# Copyright (c) 2026-06-07 RADRILONIUMA / TRIANIUMA Kingdom. All rights reserved.
from langchain.tools import tool
import os
import mss
import mss.tools

@tool("capture_screenshot", return_direct=True)
def take_screenshot() -> str:
    """
    Captures the current screen and saves it to '~/path/to/example.png' using the 'mss' library.
    
    Use this tool when the user says:
    - "Take a screenshot"
    - "Capture the screen"
    - "Save a screenshot"
    """
    try:
        image_path = os.path.expanduser("~/path/to/example.png")
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        with mss.mss() as sct:
            monitor = sct.monitors[1]  # [1] = main monitor; [0] = all monitors
            screenshot = sct.grab(monitor)
            mss.tools.to_png(screenshot.rgb, screenshot.size, output=image_path)

        return f"Screenshot captured and saved sir."
    except Exception as e:
        return f"Failed to capture screenshot: {str(e)}"
