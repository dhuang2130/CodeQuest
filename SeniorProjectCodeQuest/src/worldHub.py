import pygame
import sys
import subprocess
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 500
FPS = 60

# Set up the game clock
clock = pygame.time.Clock()

# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("World Hub")

# Button class definition
class Button:
    def __init__(self, text, rect):
        self.text = text
        self.rect = rect
        self.font = pygame.font.Font(None, 36)
        self.is_hovered = False

    def draw(self, screen):
        color = (200, 200, 200) if not self.is_hovered else (150, 150, 150)
        pygame.draw.rect(screen, color, self.rect)
        text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

# Function to run external scripts
def run_external_script(script_name):
    script_directory = os.path.dirname(os.path.realpath(__file__))
    script_path = os.path.join(script_directory, f"{script_name}.py")

    print(f"Running {script_name} Section. Script Path: {script_path}")
    subprocess.run([sys.executable, script_path])

# Function to handle the tutorial section
def handle_tutorial():
    run_external_script("tutorial")

# Function to handle the data structures section
def handle_data_structures():
    run_external_script("data_structures")

# Function to handle the algorithms section
def handle_algorithms():
    run_external_script("algorithms")

# Function to handle the logic section
def handle_logic():
    run_external_script("logic")

# Function to handle the artificial intelligence section
def handle_artificial_intelligence():
    run_external_script("artificial_intelligence")

# Function to handle the machine learning section
def handle_machine_learning():
    run_external_script("machine_learning")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.size
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)

    # Button definitions
    tutorial_button = Button("Tutorial", pygame.Rect(50, 50, 300, 50))
    data_structures_button = Button("Data Structures", pygame.Rect(50, 150, 300, 50))
    algorithms_button = Button("Algorithms", pygame.Rect(50, 250, 300, 50))
    logic_button = Button("Logic", pygame.Rect(50, 350, 300, 50))
    ai_button = Button("Artificial Intelligence", pygame.Rect(50, 450, 300, 50))
    ml_button = Button("Machine Learning", pygame.Rect(50, 550, 300, 50))

    # Draw buttons
    for button in [tutorial_button, data_structures_button, algorithms_button, logic_button, ai_button, ml_button]:
        button.draw(screen)

        # Check if the mouse is hovering over the button
        mouse_pos = pygame.mouse.get_pos()
        button.is_hovered = button.rect.collidepoint(mouse_pos)

        # Check for button click
        if button.is_hovered and event.type == pygame.MOUSEBUTTONDOWN:
            if button == tutorial_button:
                handle_tutorial()
            elif button == data_structures_button:
                handle_data_structures()
            elif button == algorithms_button:
                handle_algorithms()
            elif button == logic_button:
                handle_logic()
            elif button == ai_button:
                handle_artificial_intelligence()
            elif button == ml_button:
                handle_machine_learning()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
