import pygame

WALL = 0
PATH = 1

WALL_COLOR = (0, 0, 255)
PATH_COLOR = (0, 255, 0)

def create_maze1():
    return [
        #0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [0, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0], #1
        [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0], #2
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0], #3
        [0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], #4
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0], #5
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], #6
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0], #7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    ]

def create_maze2():
    return [
        #0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #1
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #2
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #3
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], #4
        [0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 0], #5
        [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0], #6
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #7
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    ]

def create_maze3():
    return [
        #0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10, 11
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #0
        [0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0], #1
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], #2
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0], #3
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0], #4
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0], #5
        [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0], #6
        [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0], #7
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0], #8
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], #9
    ]


def draw_maze(display_surface, maze_array, tile_size, x_offset=0, text_input_width=0):
    maze_width = display_surface.get_width() - text_input_width - x_offset

    for row in range(len(maze_array)):
        for col in range(len(maze_array[row])):
            tile_type = maze_array[row][col]

            if tile_type == WALL:
                draw_wall(display_surface, col, row, tile_size, x_offset)
            elif tile_type == PATH:
                draw_path(display_surface, col, row, tile_size, x_offset)

def draw_wall(display_surface, col, row, tile_size, x_offset):
    pygame.draw.rect(display_surface, WALL_COLOR, (col * tile_size + x_offset, row * tile_size, tile_size, tile_size))

def draw_path(display_surface, col, row, tile_size, x_offset):
    pygame.draw.rect(display_surface, PATH_COLOR, (col * tile_size + x_offset, row * tile_size, tile_size, tile_size))
