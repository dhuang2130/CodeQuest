import pygame
from maze import draw_maze
TEXT_EDITOR_WIDTH = 200
WALL = 0

def collides_with_walls(player_rect, maze, tile_size, x_offset=0):
    player_row = (player_rect.y - x_offset) // tile_size
    player_col = player_rect.x // tile_size

    if (
        player_row < 0
        or player_col < 0
        or player_row >= len(maze)
        or player_col >= len(maze[0])
    ):
        return True  # Return True for out-of-bounds

    return maze[player_row][player_col] == WALL

def move_player(player_rect, direction, distance, maze, tile_size, screen, player_image, clock, FPS):
    # Get the player's current position
    speed = 20
    current_row = player_rect.y // tile_size
    current_col = (player_rect.x - TEXT_EDITOR_WIDTH) // tile_size

    # Calculate the target position based on the direction and distance
    if direction == "up":
        target_row = max(0, current_row - distance)
        target_col = current_col
    elif direction == "down":
        target_row = min(len(maze) - 1, current_row + distance)
        target_col = current_col
    elif direction == "left":
        target_row = current_row
        target_col = max(0, current_col - distance)
    elif direction == "right":
        target_row = current_row
        target_col = min(len(maze[0]) - 1, current_col + distance)
    else:
        # Handle other directions or invalid input
        return player_rect

    # Calculate the step size for smooth movement
    step_x = (target_col * tile_size + TEXT_EDITOR_WIDTH - player_rect.x) / speed
    step_y = (target_row * tile_size - player_rect.y) / speed

    # Move the player gradually toward the target position
    for _ in range(speed):
        player_rect.x += step_x
        player_rect.y += step_y

        # Draw the updated game scene
        draw_maze(screen, maze, tile_size, x_offset=TEXT_EDITOR_WIDTH, text_input_width=TEXT_EDITOR_WIDTH)
        screen.blit(player_image, (player_rect.x, player_rect.y))
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Set the player's final position
    player_rect.topleft = (target_col * tile_size + TEXT_EDITOR_WIDTH, target_row * tile_size)

    return player_rect