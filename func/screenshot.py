import pyautogui
import time

def capture_screenshot():
    time.sleep(2)  # Wait for 2 seconds to allow the user to switch to the desired window
    screenshot = pyautogui.screenshot()
    img_path = 'screenshot.png'
    screenshot.save(img_path)
    return img_path