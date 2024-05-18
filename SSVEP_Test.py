import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SSVEP Blinking Object with Frequency Control")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (200, 200, 200)

# Slider properties
slider_rect = pygame.Rect(100, 550, 600, 20)
slider_handle_rect = pygame.Rect(100, 545, 10, 30)
slider_min, slider_max = 1, 500  # Frequency range in Hz
slider_value = slider_min

# Object properties
obj_rect = pygame.Rect(width // 2 - 50, height // 2 - 50, 100, 100)

# Timing
clock = pygame.time.Clock()
blink_time = 0
blink_state = True


def draw_slider(screen, rect, handle_rect, value):
    pygame.draw.rect(screen, gray, rect)
    handle_rect.x = rect.x + (value - slider_min) / (slider_max - slider_min) * (rect.width - handle_rect.width)
    pygame.draw.rect(screen, red, handle_rect)


def main():
    global blink_time, blink_state, slider_value

    dragging = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if slider_handle_rect.collidepoint(event.pos):
                    dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if dragging:
                    new_x = max(slider_rect.x, min(event.pos[0], slider_rect.x + slider_rect.width))
                    slider_value = slider_min + (new_x - slider_rect.x) / slider_rect.width * (slider_max - slider_min)

        screen.fill(white)

        # Update blink state based on frequency
        current_time = pygame.time.get_ticks()
        interval = 1000 / (slider_value * 2)  # Blinking interval in milliseconds
        if current_time - blink_time >= interval:
            blink_state = not blink_state
            blink_time = current_time

        # Draw the blinking object
        if blink_state:
            pygame.draw.rect(screen, black, obj_rect)

        # Draw the slider
        draw_slider(screen, slider_rect, slider_handle_rect, slider_value)

        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()
