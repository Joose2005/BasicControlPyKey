import pygame
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController
import json

# Initialize Pygame and joystick
pygame.init()
pygame.joystick.init()

# Create controllers
keyboard = KeyboardController()
mouse = MouseController()

button_to_key = load_button_to_key_mapping('controlpykey.json')


# Dictionary to map joystick buttons to keyboard keys
button_to_key = {
    0: Key.space,  # Example: A button to Space key
    1: Key.enter,  # Example: B button to Enter key
    2: Key.esc,    # Example: X button to Escape key
    3: Key.e,    # Example: Y button to Tab key
    # Make some sort of dictionary file so I'm not doing this in code.
}

def adjust_sensitivity(value, base_sensitivity=10, max_sensitivity=75):
    # Dynamic sensitivity
    return base_sensitivity + (max_sensitivity - base_sensitivity) * abs(value)

def press_key(key):
    keyboard.press(key)
    keyboard.release(key)

def move_mouse(dx, dy):
    x, y = mouse.position
    mouse.position = (x + dx, y + dy)

# Main loop
def main():
    clock = pygame.time.Clock()
    running = True

    # Make sure a controller with a joystick is connected
    if pygame.joystick.get_count() == 0:
        print("No joystick connected.")
        return

    # Use the first joystick
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    print(f"Detected joystick: {joystick.get_name()}")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button in button_to_key:
                    press_key(button_to_key[event.button])
                    print(f"Button {event.button} pressed. Mapped to {button_to_key[event.button]}")

        # Get the value of the joystick axes
        if joystick.get_numaxes() >= 4:
            # Right joystick is usually axes 2 (horizontal) and 3 (vertical)
            x_axis = joystick.get_axis(2)
            y_axis = joystick.get_axis(3)
            
            x_sensitivity = adjust_sensitivity(x_axis)
            y_sensitivity = adjust_sensitivity(y_axis)

            # Right stick to move mouse might make this toggleable
            move_mouse(int(x_axis * x_sensitivity), int(y_axis * y_sensitivity))

        # Cap the frame rate might make a settings file to make editing this easier
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
