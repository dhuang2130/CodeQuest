import pygame

class TextInputManager:
    def __init__(self, text_input_width, text_input_height):
        self.text_input_width = text_input_width
        self.text_input_height = text_input_height
        self.text_input_color = (255, 255, 255)
        self.text_surface = None
        self.font = pygame.font.Font('c:\WINDOWS\Fonts\ARIAL.TTF', 20)
        self.user_input = ""
        self.enter_pressed = False
        self.run_code_pressed = False
        self.max_lines = 20

        # Button properties
        self.button_rect = pygame.Rect(5, text_input_height - 30, 100, 25)
        self.button_color = (100, 100, 100)
        self.button_text = "Run Code"

    def update(self, event):
        # Handle text input logic
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if len(self.user_input.split('\n')) >= self.max_lines:
                    self.user_input = '\n'.join(self.user_input.split('\n')[1:])
                self.enter_pressed = True
            elif event.key == pygame.K_BACKSPACE:
                self.user_input = self.user_input[:-1]
            else:
                self.user_input += event.unicode

        # Handle button click
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.run_code_pressed = True

        # Update the text surface
        self.text_surface = self.font.render(self.user_input, True, (0, 0, 0))

    def draw(self, surface, rect):
        # Draw the background of the text input window
        pygame.draw.rect(surface, (255, 255, 255), rect)

        # Draw the border of the text input window
        pygame.draw.rect(surface, self.text_input_color, rect, 2)

        # Draw the text input content
        lines = self.user_input.split('\n')
        for i in range(min(len(lines), self.max_lines)):
            line_surface = self.font.render(lines[i], True, (0, 0, 0))
            surface.blit(line_surface, (rect.x + 5, rect.y + 5 + i * self.font.get_linesize()))

        # Draw the button
        pygame.draw.rect(surface, self.button_color, self.button_rect.move(rect.x, rect.y))  # Move the button
        button_text_surface = self.font.render(self.button_text, True, (255, 255, 255))
        surface.blit(button_text_surface, (self.button_rect.x + 5 + rect.x, self.button_rect.y + 5 + rect.y))

    def get_user_input(self):
        return self.user_input

    def clear_user_input(self):
        self.user_input = ""
        self.enter_pressed = False

    def set_run_code_pressed(self):
        self.run_code_pressed = True

    def clear_run_code_pressed(self):
        self.run_code_pressed = False

    def resize(self, text_input_width, text_input_height):
        self.text_input_width = text_input_width
        self.text_input_height = text_input_height
