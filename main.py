import pyautogui
import screen_brightness_control as sbc
from PIL import Image
import math

def calculate_intensity(r, g, b):
    return (0.2126 * r + 0.7152 * g + 0.0722 * b)

def get_dominant_color(img):
    image = img.copy()
    image = image.convert("RGBA")
    image = image.resize((1, 1), resample=0)
    dominant_color = image.getpixel((0, 0))

    return dominant_color

initial_brightness = None
initial_intensity = None

previous_brightness = None
previous_intensity = None
previous_percentage_decreased = None


while True:
    current_brightness = sbc.get_brightness()
    pyautogui.screenshot("./screenshot/screenshot.png")

    image = Image.open("./screenshot/screenshot.png")
    dominant_color = get_dominant_color(image)
    current_intensity = calculate_intensity(dominant_color[0], dominant_color[1], dominant_color[2])

    if(previous_brightness!=None and abs(current_intensity - initial_intensity) < 2):
        current_brightness = initial_brightness
        previous_brightness = current_brightness


    if(previous_brightness == None):
        previous_brightness = current_brightness
        previous_intensity = current_intensity
        initial_brightness = current_brightness
        initial_intensity = current_intensity
        continue

    if(current_intensity > previous_intensity):
        increase_percentage = (current_intensity - previous_intensity) / previous_intensity * 100
        increase_percentage = math.ceil(increase_percentage / 64)
        print("------------------------------------------------------------------------")
        print("Percentage Increase: ", increase_percentage)
        new_brightness = current_brightness[0] - increase_percentage

        sbc.fade_brightness(new_brightness)
        current_brightness = new_brightness
        previous_intensity = current_intensity
        previous_brightness = current_brightness
    elif(current_intensity < previous_intensity):
        
        decrease_percentage = (previous_intensity - current_intensity) / current_intensity * 100
        decrease_percentage = math.ceil(decrease_percentage / 64)
        print("------------------------------------------------------------------------")
        print("Percentage Decrease: ", decrease_percentage)
        new_brightness = current_brightness[0] + decrease_percentage

        sbc.fade_brightness(new_brightness)
        current_brightness = new_brightness
        previous_intensity = current_intensity
        previous_brightness = current_brightness