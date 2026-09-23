import screen_brightness_control as sbc

print("Current Brightness:", sbc.get_brightness())

sbc.set_brightness(30)

print("Brightness changed to 30%")