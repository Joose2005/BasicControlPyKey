import pygame
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Controller as MouseController

# Initialize Pygame and joystick
pygame.init()
pygame.joystick.init()

# Create controllers
keyboard = KeyboardController()
mouse = MouseController()

# Dictionary to map joystick buttons to keyboard keys
button_to_key = {
    0: Key.space,  # Example: A button to Space key
    1: Key.enter,  # Example: B button to Enter key
    2: Key.esc,    # Example: X button to Escape key
    3: Key.tab,    # Example: Y button to Tab key
    # Add more button mappings here
}

# Sensitivity for joystick to mouse movement
sensitivity = 10

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

    # Make sure a joystick is connected
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

        # Get the state of the joystick axes
        if joystick.get_numaxes() >= 4:
            # Right joystick usually corresponds to axes 2 (horizontal) and 3 (vertical)
            x_axis = joystick.get_axis(2)
            y_axis = joystick.get_axis(3)
            move_mouse(int(x_axis * sensitivity), int(y_axis * sensitivity))

        # Cap the frame rate
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
