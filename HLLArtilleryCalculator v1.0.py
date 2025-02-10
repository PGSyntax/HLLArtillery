import pyautogui
import easyocr
import time
import os
import re

user_home = os.path.expanduser("~")
capture_dir = os.path.join(user_home, "Pictures", "Screenshots", "area") #adjust if needed

if not os.path.exists(capture_dir):
    os.makedirs(capture_dir)

def get_screenshot():
    capture_path = os.path.join(capture_dir, "captured_area.jpg")

    screenshot = pyautogui.screenshot(region=(1625, 800, 250, 250))
    screenshot.save(capture_path)
    return capture_path

def calculate_mil_to_dist(mil):
    m = -4.213
    b = 4222.4
    distance = m * mil + b

    if 100 <= distance <= 1600:
        return round(distance)
    else:
        return None

def extract_mil_from_text(text):
    match = re.search(r'(\d+)\s*MIL', text)
    if match:
        return int(match.group(1))
    return None

def main():
    reader = easyocr.Reader(['en'])

    while True:
        try:
            capture_path = get_screenshot()

            if not os.path.exists(capture_path):
                raise FileNotFoundError("path missing")

            result = reader.readtext(capture_path)

            mil_value = None
            for (_, text, _) in result:
                mil_value = extract_mil_from_text(text)
                if mil_value is not None:
                    break

            if mil_value is not None:
                dist = calculate_mil_to_dist(mil_value)
                if dist is not None:
                    print(f"{mil_value} MIL - Distance: {dist}m")
                else:
                    print(f"{mil_value} MIL - Distance: out of range")
            else:
                print("-")

            if os.path.exists(capture_path):
                os.remove(capture_path)

            time.sleep(0.5)

        except Exception as ex:
            print("err:", ex)

if __name__ == "__main__":
    main()
