import pygame
import sys
import os
from player_controller import collides_with_walls, move_player
from maze import create_maze1, draw_maze, create_maze2, create_maze3
from text_input import TextInputManager
import textwrap

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 1000, 500
TEXT_EDITOR_WIDTH = 200
INSTRUCTIONS_WIDTH = 200
INSTRUCTIONS_MARGIN = 10
GAME_SCENE_WIDTH = WINDOW_WIDTH - TEXT_EDITOR_WIDTH
PLAYER_SIZE = 50
FPS = 60
TILE_SIZE = 50
player_width = 50
player_height = 50
player_pos1 = [1, 1]
player_pos2 = [4,1]
player_pos3 = [1, 2]
GOAL_POS_LEVEL1 = [3, 8]
GOAL_POS_LEVEL2 = [4, 10]
GOAL_POS_LEVEL3 = [3, 9]
STAR_POS_LEVEL3 = [6, 4]
star_count = 0  # Variable to store the number of stars collected
level = 1
font_color = (0, 0, 0) 


code_processed = False
is_transitioning = False

maze = create_maze1()
maze_level2 = create_maze2()
maze_level3 = create_maze3()

level1Instructions = textwrap.dedent("""Level 1: By using moveLeft(int), you are able to move your character a certain amount of spaces based on the integer you place in the function. This is known as a function. This function has already been coded in the back - you're able to use them one after another. """).strip()
level2Instructions = textwrap.dedent("""Level 2: For loops are a very important part of Computer Science. By using a for loop you're able to constantly loop until the requirements have been met. In Python the syntax is: for i in range(int). This would loop 'int' amount of times. With this knowledge you should be able to loop through each of the circles. """).strip()
level3Instructions = textwrap.dedent("""Level 3: If else statements are another very important aspect of Computer Science. Logic is very important - we would want to only do certain tasks when a condition is met. Therefore, we would use an if, elif, and else statement in python. The syntax is if statement==true, do something. In this instance, we can use a function called getStar() to pick up the star into your inventory, since the star is a part of your clear condition. """).strip()


# Create the game window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Tutorial")

# Get the path to the images folder
current_path = os.path.dirname(__file__)
images_path = os.path.join(current_path, "../images")

# Load player image
player_image = pygame.image.load(os.path.join(images_path, "character.png")).convert_alpha()
player_image = pygame.transform.scale(player_image, (PLAYER_SIZE, PLAYER_SIZE))

# Load goal image
goal_image = pygame.image.load(os.path.join(images_path, "goal.png")).convert_alpha()
goal_image = pygame.transform.scale(goal_image, (PLAYER_SIZE, PLAYER_SIZE))

win_image = pygame.image.load(os.path.join(images_path, "goal.jpg")).convert_alpha()
win_image = pygame.transform.scale(win_image, (600, 200))

star_image = pygame.image.load(os.path.join(images_path, "star.png")).convert_alpha()
star_image = pygame.transform.scale(star_image, (50, 50))

def process_code(code):
    global player_rect
    exec(code, globals())
    

command_processed = False

# Initialize player position
player_rect = pygame.Rect(
    GAME_SCENE_WIDTH // 2 - PLAYER_SIZE // 2 + TEXT_EDITOR_WIDTH,
    WINDOW_HEIGHT // 2 - PLAYER_SIZE // 2,
    PLAYER_SIZE,
    PLAYER_SIZE,
)

# Initialize timer variables
transition_timer = 0
transition_duration = 3000  # 3000 milliseconds (3 seconds)

# Set up the game clock
clock = pygame.time.Clock()

# Initialize the TextInputManager
TEXT_EDITOR_HEIGHT = WINDOW_HEIGHT
text_input_manager = TextInputManager(
    text_input_width=TEXT_EDITOR_WIDTH, text_input_height=TEXT_EDITOR_HEIGHT
)

# Set the initial player position
player_rect.topleft = (player_pos1[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, player_pos1[0] * TILE_SIZE)
player_pos = player_pos1

# Set the goal position
GOAL_POS = GOAL_POS_LEVEL1

# Set the star position only for level 3
if level == 3:
    STAR_POS = STAR_POS_LEVEL3
    STAR_POSITION = [6, 4]  # Update the position for the third level star
else:
    STAR_POS = None
    STAR_POSITION = None


ALLOWED_COMMANDS = {"moveRight", "moveLeft", "moveUp", "moveDown"}

def execute_command(command, distance=1):
    global player_rect
    if command == "moveUp":
        move_player(player_rect, "up", distance, maze, TILE_SIZE, screen, player_image, clock, FPS)
    elif command == "moveDown":
        move_player(player_rect, "down", distance, maze, TILE_SIZE, screen, player_image, clock, FPS)
    elif command == "moveLeft":
        move_player(player_rect, "left", distance, maze, TILE_SIZE, screen, player_image, clock, FPS)
    elif command == "moveRight":
        move_player(player_rect, "right", distance, maze, TILE_SIZE, screen, player_image, clock, FPS)

def check_on_star(player_rect, maze, tile_size, x_offset):
    player_row = (player_rect.y - x_offset) // tile_size
    player_col = player_rect.x // tile_size

    if (
        player_row < 0
        or player_col < 0
        or player_row >= len(maze)
        or player_col >= len(maze[0])
    ):
        return False  # Return False for out-of-bounds

    return maze[player_row][player_col] == STAR_POS

def get_star():
    global player_pos, maze, star_count
    # Assuming player_pos is the current position of the player in [row, col] format
    row, col = player_pos
    # Set the maze cell to 0 to remove the star
    maze[row][col] = 0
    star_count += 1  # Increment the star count

def process_user_input(user_input):
    global player_rect, command_processed, on_star
    commands = user_input.split("\n")

    for line in commands:
        # Skip empty lines
        if not line.strip():
            continue

        # Extract command and distance from the line
        command_parts = line.split("(")
        if len(command_parts) > 0:
            command = command_parts[0].strip()
            if command in ALLOWED_COMMANDS:
                # Extract distance (default to 1 if not specified)
                distance_parts = line.split("(")
                if len(distance_parts) > 1:
                    distance_value = distance_parts[1].split(")")
                    if distance_value and len(distance_value) > 0:
                        try:
                            distance = int(distance_value[0])
                        except ValueError:
                            distance = 1
                    else:
                        # Skip lines without a closing parenthesis
                        continue
                else:
                    # Skip lines without an opening parenthesis
                    continue

                # Check if the command is to check if on a star
                if command == "onStar":
                    # Check if the player is on the star
                    on_star = check_on_star(player_rect, maze, TILE_SIZE, TEXT_EDITOR_WIDTH)

                    # Check if the player picks up the star
                    if on_star and STAR_POS == [player_rect.y // TILE_SIZE, (player_rect.x - TEXT_EDITOR_WIDTH) // TILE_SIZE]:
                        print("Picking up Star!")
                        get_star()
                    else:
                        print("You need to pick up the star to clear Level 3!")
                else:
                    # Execute the command
                    execute_command(command, distance)
            else:
                # Handle invalid command
                print(f"Invalid command: {command}")
        else:
            # Handle lines without a command
            print("Invalid line: ", line)

    # Set the flag to indicate that commands have been processed
    command_processed = True



def reset_level():
    global player_pos, player_rect, transition_timer
    player_pos = player_pos1  # Reset player position to level 1 starting position
    player_rect.topleft = (player_pos[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, player_pos[0] * TILE_SIZE)
    text_input_manager.clear_user_input()
    transition_timer = 0

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.VIDEORESIZE:
            WINDOW_WIDTH, WINDOW_HEIGHT = event.size
            screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
            GAME_SCENE_WIDTH = WINDOW_WIDTH - TEXT_EDITOR_WIDTH

            # Recreate TextInputManager with updated dimensions
            text_input_manager = TextInputManager(
                text_input_width=TEXT_EDITOR_WIDTH, text_input_height=WINDOW_HEIGHT
            )

            # Update player position based on the new dimensions
            player_rect.topleft = (player_pos[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, player_pos[0] * TILE_SIZE)

        # Update the text input manager
        text_input_manager.update(event)

    # Check for trigger condition (e.g., pressing Enter)
    if text_input_manager.enter_pressed:
        # Insert a new line instead of running code
        text_input_manager.user_input += "\n"
        text_input_manager.enter_pressed = False

    elif text_input_manager.run_code_pressed and not command_processed:
        # Reset player position before processing new commands
        if level == 1:
            player_pos = player_pos1
        elif level == 2:
            player_pos = player_pos2
        elif level == 3:
            player_pos = player_pos3
        player_rect.topleft = (player_pos[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, player_pos[0] * TILE_SIZE)

        # Process the code here
        user_input = text_input_manager.get_user_input()
        process_user_input(user_input)

        # Reset the button state
        text_input_manager.run_code_pressed = False

    # Add this block to reset the flag when a new line of code is entered
    elif not text_input_manager.run_code_pressed:
        command_processed = False

    # Check if the player is on the star
    if STAR_POS:
        star_pos_x = STAR_POS[1] * TILE_SIZE + TEXT_EDITOR_WIDTH
        star_pos_y = STAR_POS[0] * TILE_SIZE
        screen.blit(star_image, (star_pos_x, star_pos_y))

    on_star = check_on_star(player_rect, maze, TILE_SIZE, TEXT_EDITOR_WIDTH)

    # Check if the player picks up the star
    if on_star and STAR_POS == [player_rect.y // TILE_SIZE, (player_rect.x - TEXT_EDITOR_WIDTH) // TILE_SIZE]:
        print("Picking up Star!")
        get_star()

    # Check if the player has reached the goal
    if [player_rect.y // TILE_SIZE, (player_rect.x - TEXT_EDITOR_WIDTH) // TILE_SIZE] == GOAL_POS:
        if level == 3:
            STAR_POS = STAR_POS_LEVEL3
            player_pos=player_pos3
            STAR_POSITION = [6, 4]  # Update the position for the third level star
        else:
            STAR_POS = None
            STAR_POSITION = None
        if level == 3 and STAR_POS is not None:
            star_pos_x = STAR_POS[1] * TILE_SIZE + TEXT_EDITOR_WIDTH
            star_pos_y = STAR_POS[0] * TILE_SIZE
            screen.blit(star_image, (star_pos_x, star_pos_y))
            # Check if the star has been picked up
            if on_star:
                screen.blit(win_image, (200, 100))  # Set the coordinates where you want to display the win screen
                pygame.display.flip()  # Update the display to show the win screen immediately
                pygame.time.delay(3000)  # Delay for 3000 milliseconds (3 seconds) to show the win screen
                # Perform actions for level transition
                text_input_manager.clear_user_input()
                is_transitioning = True
            else:
                print("You need to pick up the star to clear Level 3!")
                # Reset the level if the player reaches the goal without the star
                reset_level()
        elif level == 2:
            screen.blit(win_image, (200, 100))  # Set the coordinates where you want to display the win screen
            pygame.display.flip()  # Update the display to show the win screen immediately
            pygame.time.delay(3000)  # Delay for 3000 milliseconds (3 seconds) to show the win screen
            # Perform actions for level transition
            transition_timer = 0  # Reset the transition timer 
            text_input_manager.clear_user_input()
            is_transitioning = True
        elif level == 1:
            screen.blit(win_image, (200, 100))  # Set the coordinates where you want to display the win screen
            pygame.display.flip()  # Update the display to show the win screen immediately
            pygame.time.delay(3000)  # Delay for 3000 milliseconds (3 seconds) to show the win screen
            # Perform actions for level transition
            transition_timer = 0  # Reset the transition timer 
            text_input_manager.clear_user_input()
            is_transitioning = True

    # Draw the game scene with an offset to the right
    if is_transitioning:
        # Introduce a delay before updating player and goal position
        pygame.time.wait(500)  # Adjust the delay duration as needed
        level += 1
        # Update the player position        
        if level == 2:
            # Update the goal position
            GOAL_POS = GOAL_POS_LEVEL2
            
            # Switch to the second level maze
            maze = maze_level2 

            player_pos = player_pos2
            player_rect.topleft = (player_pos2[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, player_pos2[0] * TILE_SIZE)


        elif level == 3:
            # Update the goal position
            GOAL_POS = GOAL_POS_LEVEL3
            
            # Switch to the third level maze
            maze = maze_level3

            player_pos = player_pos3
            player_rect.topleft = (player_pos3[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, player_pos3[0] * TILE_SIZE)
            STAR_POSITION = [6, 4]  # Update the position for the third level star

        # Reset the transition flag
        is_transitioning = False

    draw_maze(screen, maze, TILE_SIZE, x_offset=TEXT_EDITOR_WIDTH, text_input_width=TEXT_EDITOR_WIDTH)

    # Draw the star image after drawing the game scene
    if level == 3 and STAR_POS_LEVEL3 is not None:
        screen.blit(star_image, (STAR_POS_LEVEL3[1] * TILE_SIZE + TEXT_EDITOR_WIDTH, STAR_POS_LEVEL3[0] * TILE_SIZE))


    # Draw the goal image
    goal_pos_x = GOAL_POS[1] * TILE_SIZE + TEXT_EDITOR_WIDTH
    goal_pos_y = GOAL_POS[0] * TILE_SIZE
    screen.blit(goal_image, (goal_pos_x, goal_pos_y))

    # Draw the player character using the loaded image
    screen.blit(player_image, (player_rect.x, player_rect.y))


    # Draw the instructions area (white background)
    instructions_area_rect = pygame.Rect(GAME_SCENE_WIDTH, 0, INSTRUCTIONS_WIDTH, WINDOW_HEIGHT)
    pygame.draw.rect(screen, (255, 255, 255), instructions_area_rect)

    # Draw instructions based on the current level
    if level == 1:
        instructions_text = level1Instructions
    elif level == 2:
        instructions_text = level2Instructions
    elif level == 3:
        instructions_text = level3Instructions

    # Adjust font size dynamically based on the length of instructions
    font_size = 20
    font = pygame.font.Font(None, font_size)
    wrapped_instructions = textwrap.fill(instructions_text, width=30)

    # Display instructions with word wrapping
    x = GAME_SCENE_WIDTH + INSTRUCTIONS_MARGIN
    y = INSTRUCTIONS_MARGIN  # Adjusted margin only on the top side
    for line in wrapped_instructions.splitlines():
        instructions_surface = font.render(line, True, (0, 0, 0))
        instructions_rect = instructions_surface.get_rect(topleft=(x, y))
        screen.blit(instructions_surface, instructions_rect)
        y += font.get_linesize()  # Move to the next line

    # Draw the text input window
    text_input_manager.draw(screen, pygame.Rect(0, 0, TEXT_EDITOR_WIDTH, WINDOW_HEIGHT))


    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)