#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np
import pygame

# Pygameの初期化
pygame.init()

# ウィンドウサイズとセルサイズの設定
WIDTH, HEIGHT = 500, 500
CELL_SIZE = 10
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE

# 色の定義
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# スクリーンの初期化
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Game of Life')

# パターンの定義
STATIC = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,1,1,0,0,0,0,1,1,0,0,0,1,1,0],
    [1,1,0,0,1,0,0,1,0,0,1,0,0,1,0,0,1,0,1],
    [0,0,0,0,0,1,1,0,0,0,0,1,0,1,0,0,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
])

OSCILLATOR = np.array([
    [1,0,0,0,0,1,0,0],
    [1,0,0,0,1,0,0,1],
    [1,0,0,0,1,0,0,1],
    [0,0,0,0,0,0,1,0]
])

GLIDER = np.array([
    [0,0,0,0],
    [0,0,1,0],
    [0,0,0,1],
    [0,1,1,1]
])

GLIDER_GUN = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,1,1,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
])

# 初期状態の設定
state = np.zeros((GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)
next_state = np.empty((GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)

# パターンの選択
def select_pattern():
    print("Select a pattern:")
    print("1: Random")
    print("2: STATIC")
    print("3: OSCILLATOR")
    print("4: GLIDER")
    print("5: GLIDER_GUN")
    choice = input("Enter the number of your choice: ")
    if choice == "1":
        return np.random.randint(2, size=(GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)
    elif choice == "2":
        state[2:2+STATIC.shape[0], 2:2+STATIC.shape[1]] = STATIC
        return state
    elif choice == "3":
        state[2:2+OSCILLATOR.shape[0], 2:2+OSCILLATOR.shape[1]] = OSCILLATOR
        return state
    elif choice == "4":
        state[2:2+GLIDER.shape[0], 2:2+GLIDER.shape[1]] = GLIDER
        return state
    elif choice == "5":
        state[2:2+GLIDER_GUN.shape[0], 2:2+GLIDER_GUN.shape[1]] = GLIDER_GUN
        return state
    else:
        print("Invalid choice, defaulting to random.")
        return np.random.randint(2, size=(GRID_HEIGHT, GRID_WIDTH), dtype=np.int8)

state = select_pattern()

# ゲームループ
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            nw = state[i-1,j-1]
            n  = state[i-1,j]
            ne = state[i-1,(j+1)%GRID_WIDTH]
            w  = state[i,j-1]
            c  = state[i,j]
            e  = state[i,(j+1)%GRID_WIDTH]
            sw = state[(i+1)%GRID_HEIGHT,j-1]
            s  = state[(i+1)%GRID_HEIGHT,j]
            se = state[(i+1)%GRID_HEIGHT,(j+1)%GRID_WIDTH]
            neighbor_cell_sum = nw + n + ne + w + e + sw + s + se
            if c == 0 and neighbor_cell_sum == 3:
                next_state[i,j] = 1
            elif c == 1 and neighbor_cell_sum in (2,3):
                next_state[i,j] = 1
            else:
                next_state[i,j] = 0

    state, next_state = next_state, state

    # スクリーンの更新
    screen.fill(WHITE)
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            if state[i, j] == 1:
                pygame.draw.rect(screen, BLACK, (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.display.flip()
    pygame.time.delay(100)

pygame.quit()
