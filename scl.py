import sys
import numpy as np
import pygame
import random

# Constants
SPACE_SIZE = 16
CELL_SIZE = 40

# Colors
COLORS = {
    'HOLE': (255, 255, 255),          # White (same as the background)
    'SUBSTRATE': (0, 255, 255),   # Cyan
    'CATALYST': (255, 0, 255),    # Magenta
    'LINK': (0, 0, 255),        # Blue
    'LINK_SUBSTRATE': (255, 255, 0)  # Yellow
}

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SPACE_SIZE * CELL_SIZE, SPACE_SIZE * CELL_SIZE))
pygame.display.set_caption("SCL Simulation")

# Initial configuration
INITIAL_SUBSTRATE_DENSITY = 0.8
INITIAL_CATALYST_POSITIONS = [(8, 8)]

# Model parameters
MOBILITY_FACTOR = {
    'HOLE': 0.1,
    'SUBSTRATE': 0.1,
    'CATALYST': 0.0001,
    'LINK': 0.05,
    'LINK_SUBSTRATE': 0.05,
}
PRODUCTION_PROBABILITY = 0.95
DISINTEGRATION_PROBABILITY = 0.0005
BONDING_CHAIN_INITIATE_PROBABILITY = 0.1
BONDING_CHAIN_EXTEND_PROBABILITY = 0.6
BONDING_CHAIN_SPLICE_PROBABILITY = 0.9
BOND_DECAY_PROBABILITY = 0.0005
ABSORPTION_PROBABILITY = 0.5
EMISSION_PROBABILITY = 0.5

# Utility functions
def get_neumann_neighborhood(x, y, space_size):
    n = [((x + 1) % space_size, y), ((x - 1) % space_size, y), (x, (y + 1) % space_size), (x, (y - 1) % space_size)]
    return n

def get_random_neumann_neighborhood(x, y, space_size):
    neighborhood = get_neumann_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

def get_moore_neighborhood(x, y, space_size):
    n = [((x - 1) % space_size, (y - 1) % space_size), (x, (y - 1) % space_size), ((x + 1) % space_size, (y - 1) % space_size),
         ((x - 1) % space_size, y), ((x + 1) % space_size, y),
         ((x - 1) % space_size, (y + 1) % space_size), (x, (y + 1) % space_size), ((x + 1) % space_size, (y + 1) % space_size)]
    return n

def get_random_moore_neighborhood(x, y, space_size):
    neighborhood = get_moore_neighborhood(x, y, space_size)
    nx, ny = neighborhood[np.random.randint(len(neighborhood))]
    return nx, ny

def get_random_2_moore_neighborhood(x, y, space_size):
    n0_x, n0_y = get_random_moore_neighborhood(x, y, space_size)
    if x == n0_x:
        n1_x = np.random.choice([(n0_x + 1) % space_size, (n0_x - 1) % space_size])
        n1_y = n0_y
    elif y == n0_y:
        n1_x = n0_y
        n1_y = np.random.choice([(n0_y + 1) % space_size, (n0_y - 1) % space_size])
    else:
        n = [(x, n0_y), (n0_x, y)]
        n1_x, n1_y = n[np.random.randint(len(n))]
    return n0_x, n0_y, n1_x, n1_y

def get_adjacent_moore_neighborhood(x, y, n_x, n_y, space_size):
    if x == n_x:
        n0_x = (n_x - 1) % space_size
        n0_y = n_y
        n1_x = (n_x + 1) % space_size
        n1_y = n_y
    elif y == n_y:
        n0_x = n_x
        n0_y = (n_y - 1) % space_size
        n1_x = n_x
        n1_y = (n_y + 1) % space_size
    else:
        n0_x = x
        n0_y = n_y
        n1_x = n_x
        n1_y = y
    return n0_x, n0_y, n1_x, n1_y

def evaluate_probability(probability):
    return np.random.rand() < probability

def production(particles, x, y, probability):
    p = particles[x, y]
    n0_x, n0_y, n1_x, n1_y = get_random_2_moore_neighborhood(x, y, particles.shape[0])
    n0_p = particles[n0_x, n0_y]
    n1_p = particles[n1_x, n1_y]
    if p['type'] != 'CATALYST' or n0_p['type'] != 'SUBSTRATE' or n1_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        n0_p['type'] = 'HOLE'
        n1_p['type'] = 'LINK'

def disintegration(particles, x, y, probability):
    p = particles[x, y]
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
        p['disintegrating_flag'] = True
    if not p['disintegrating_flag']:
        return
    emission(particles, x, y, 1.0)
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] == 'LINK' and n_p['type'] == 'HOLE':
        bond_decay(particles, x, y, 1.0)
        p['type'] = 'SUBSTRATE'
        n_p['type'] = 'SUBSTRATE'
        p['disintegrating_flag'] = False

def bonding(particles, x, y, chain_initiate_probability, chain_splice_probability, chain_extend_probability, chain_inhibit_bond_flag=True, catalyst_inhibit_bond_flag=True):
    p = particles[x, y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] not in ('LINK', 'LINK_SUBSTRATE'):
        return
    if n_p['type'] not in ('LINK', 'LINK_SUBSTRATE'):
        return
    if (n_x, n_y) in p['bonds']:
        return
    if len(p['bonds']) >= 2 or len(n_p['bonds']) >= 2:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in p['bonds'] or (an1_x, an1_y) in p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(n_x, n_y, x, y, particles.shape[0])
    if (an0_x, an0_y) in n_p['bonds'] or (an1_x, an1_y) in n_p['bonds']:
        return
    an0_x, an0_y, an1_x, an1_y = get_adjacent_moore_neighborhood(x, y, n_x, n_y, particles.shape[0])
    if (an0_x, an0_y) in particles[an1_x, an1_y]['bonds']:
        return
    mn_list = get_moore_neighborhood(x, y, particles.shape[0]) + get_moore_neighborhood(n_x, n_y, particles.shape[0])
    if catalyst_inhibit_bond_flag:
        for mn_x, mn_y in mn_list:
            if particles[mn_x, mn_y]['type'] == 'CATALYST':
                return
    if chain_inhibit_bond_flag:
        for mn_x, mn_y in mn_list:
            if len(particles[mn_x, mn_y]['bonds']) >= 2:
                if (x, y) not in particles[mn_x, mn_y]['bonds'] and (n_x, n_y) not in particles[mn_x, mn_y]['bonds']:
                    return
    if len(p['bonds']) == 0 and len(n_p['bonds']) == 0:
        prob = chain_initiate_probability
    elif len(p['bonds']) == 1 and len(n_p['bonds']) == 1:
        prob = chain_splice_probability
    else:
        prob = chain_extend_probability
    if evaluate_probability(prob):
        p['bonds'].append((n_x, n_y))
        n_p['bonds'].append((x, y))

def bond_decay(particles, x, y, probability):
    p = particles[x, y]
    if p['type'] in ('LINK', 'LINK_SUBSTRATE') and evaluate_probability(probability):
        for b in p['bonds']:
            particles[b[0], b[1]]['bonds'].remove((x, y))
        p['bonds'] = []

def absorption(particles, x, y, probability):
    p = particles[x, y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK' or n_p['type'] != 'SUBSTRATE':
        return
    if evaluate_probability(probability):
        p['type'] = 'LINK_SUBSTRATE'
        n_p['type'] = 'HOLE'

def emission(particles, x, y, probability):
    p = particles[x, y]
    n_x, n_y = get_random_moore_neighborhood(x, y, particles.shape[0])
    n_p = particles[n_x, n_y]
    if p['type'] != 'LINK_SUBSTRATE' or n_p['type'] != 'HOLE':
        return
    if evaluate_probability(probability):
        p['type'] = 'LINK'
        n_p['type'] = 'SUBSTRATE'

# Initialize particles
particles = np.empty((SPACE_SIZE, SPACE_SIZE), dtype=object)
for x in range(SPACE_SIZE):
    for y in range(SPACE_SIZE):
        if evaluate_probability(INITIAL_SUBSTRATE_DENSITY):
            p = {'type': 'SUBSTRATE', 'disintegrating_flag': False, 'bonds': []}
        else:
            p = {'type': 'HOLE', 'disintegrating_flag': False, 'bonds': []}
        particles[x, y] = p

for x, y in INITIAL_CATALYST_POSITIONS:
    particles[x, y]['type'] = 'CATALYST'

def draw_particles():
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x, y]
            color = COLORS[p['type']]
            if p['type'] == 'SUBSTRATE':
                pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 4)
            elif p['type'] == 'CATALYST':
                pygame.draw.circle(screen, color, (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2)
            elif p['type'] in ('LINK', 'LINK_SUBSTRATE'):
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 2)
                for bond in p['bonds']:
                    bx, by = bond
                    pygame.draw.line(screen, COLORS['LINK'], (x * CELL_SIZE + CELL_SIZE // 2, y * CELL_SIZE + CELL_SIZE // 2),
                                     (bx * CELL_SIZE + CELL_SIZE // 2, by * CELL_SIZE + CELL_SIZE // 2), 2)
            else:
                pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def update_particles():
    moved = np.full(particles.shape, False, dtype=bool)
    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            p = particles[x, y]
            n_x, n_y = get_random_neumann_neighborhood(x, y, SPACE_SIZE)
            n_p = particles[n_x, n_y]
            mobility_factor = np.sqrt(MOBILITY_FACTOR[p['type']] * MOBILITY_FACTOR[n_p['type']])
            if not moved[x, y] and not moved[n_x, n_y] and len(p['bonds']) == 0 and len(n_p['bonds']) == 0 and evaluate_probability(mobility_factor):
                particles[x, y], particles[n_x, n_y] = n_p, p
                moved[x, y] = moved[n_x, n_y] = True

    for x in range(SPACE_SIZE):
        for y in range(SPACE_SIZE):
            production(particles, x, y, PRODUCTION_PROBABILITY)
            disintegration(particles, x, y, DISINTEGRATION_PROBABILITY)
            bonding(particles, x, y, BONDING_CHAIN_INITIATE_PROBABILITY,
                                     BONDING_CHAIN_SPLICE_PROBABILITY,
                                     BONDING_CHAIN_EXTEND_PROBABILITY)
            bond_decay(particles, x, y, BOND_DECAY_PROBABILITY)
            absorption(particles, x, y, ABSORPTION_PROBABILITY)
            emission(particles, x, y, EMISSION_PROBABILITY)

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((255, 255, 255))
    update_particles()
    draw_particles()
    pygame.display.flip()
    clock.tick(100)

pygame.quit()
