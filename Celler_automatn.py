import pygame
import numpy as np

# Initialize pygame
pygame.init()

# Constants
SPACE_SIZE = 150
CELL_SIZE = 5
SCREEN_SIZE = SPACE_SIZE * CELL_SIZE
RULE = 110
FPS = 60

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)  # Background color for better visibility
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
pygame.display.set_caption("Cellular Automaton")

# CA state space
state = np.zeros(SPACE_SIZE, dtype=np.int8)
next_state = np.empty(SPACE_SIZE, dtype=np.int8)

# Initialize first state
state[len(state)//2] = 1

def update_state(state, next_state, rule):
    for i in range(SPACE_SIZE):
        l = state[i-1]
        c = state[i]
        r = state[(i+1)%SPACE_SIZE]
        neighbor_cell_code = 2**2 * l + 2**1 * c + 2**0 * r
        next_state[i] = (rule >> neighbor_cell_code) & 1
    return next_state

def draw_state(screen, state, row):
    for i in range(SPACE_SIZE):
        color = BLACK if state[i] == 1 else GRAY  # Use GRAY as the background color
        pygame.draw.rect(screen, color, (i * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def main():
    clock = pygame.time.Clock()
    row = 0

    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update state
        draw_state(screen, state, row)
        global next_state
        next_state = update_state(state, next_state, RULE)
        state[:] = next_state

        # Update display
        pygame.display.flip()

        # Control the frame rate
        clock.tick(FPS)

        # Move to next row
        row += 1
        if row >= SCREEN_SIZE // CELL_SIZE:
            row = 0
            screen.fill(GRAY)  # Fill the screen with GRAY color

    pygame.quit()

if __name__ == "__main__":
    main()
